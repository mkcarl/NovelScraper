from bs4 import BeautifulSoup
from requests_html import HTMLSession, AsyncHTMLSession
import requests
import asyncio
import os
import pathlib

class Novel:
    def __init__(self, url, firstChapter, lastChapter):
        self.base_url = url
        self.url_chapter_formatter = 0
        self.content = {}
        self._content_id = None
        self._first_chapter = firstChapter
        self._last_chapter = lastChapter
        self._name = "Default_Name"

    @property
    def content_id(self):
        return self._content_id

    @content_id.setter
    def content_id(self, idName):
        self._content_id = idName

    @property
    def last_chapter(self):
        return self._last_chapter

    @last_chapter.setter
    def last_chapter(self, lastChapNum: int):
        self._last_chapter = lastChapNum

    @property
    def first_chapter(self):
        return self._first_chapter

    @first_chapter.setter
    def first_chapter(self, firstChapNum: int):
        self._first_chapter = firstChapNum

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, novel_name):
        self._name = novel_name

    def extract_content(self, start=None, end=None, asynchronous=False, ratelimit=None):
        if self._last_chapter is None:
            raise Exception("Please set the final chapter of the novel")
        if self._content_id is None:
            raise Exception("Please define the ID of the content div.")
        start_, end_ = start, end
        if start is None:
            start_ = self.first_chapter
        if end is None:
            end_ = self.last_chapter

        if not asynchronous:
            for chapterNumber in range(start_, end_ + 1):
                chapter_url = f"{self.base_url}{str(chapterNumber).zfill(self.url_chapter_formatter)}"
                session = HTMLSession()
                webpage = session.get(chapter_url)
                chapter_HTML = webpage.html.html
                soup = BeautifulSoup(chapter_HTML)
                chapter_content = soup.find(id=self.content_id)
                self.content[f"Chapter {str(chapterNumber)}"] = chapter_content
                print(f"Done chapter {chapterNumber}")

        elif asynchronous:
            async def getChap(url):
                aSession = AsyncHTMLSession()
                r = await aSession.get(url)
                return (url[len(self.base_url):],r.html.html)

            urls = [f"{self.base_url}{str(x).zfill(self.url_chapter_formatter)}" for x in range(start_, end_ + 1)]
            coros = [getChap(x) for x in urls]

            async def getContents(coros):
                contents = await asyncio.gather(*coros)
                for i, content in contents:
                    soup = BeautifulSoup(content)
                    chapter_content = soup.find(id=self.content_id)
                    self.content[f"Chapter_{str(i).zfill(len(str(self.last_chapter)))}"] = chapter_content

            if ratelimit is None:
                asyncio.run(getContents(coros))
            elif ratelimit != 0:
                chunks = [coros[i:i + ratelimit] for i in range(0, len(coros), ratelimit)]
                for chunk in chunks:
                    asyncio.run(getContents(chunk))
                    print(f"Fetched chunk {chunks.index(chunk)+1}/{len(chunks)}")

    def export(self, fmt):
        directory = f"chapters/{self.name}"
        if not os.path.exists(directory):
            pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
        for chap, cont in self.content.items():
            with open(f"{directory}/{chap}.{fmt}", "w", encoding="utf-8") as f:
                f.write(str(cont))

if __name__ == '__main__':
    loa = Novel("https://www.wuxiaworld.com/novel/life-once-again/loa-chapter-",
                0, 50)
    loa._content_id = "chapter-content"
    loa.name = "Life_Once_Again"
    loa.extract_content(asynchronous=True, ratelimit=30)
    loa.export("html")
    print(len(loa.content))