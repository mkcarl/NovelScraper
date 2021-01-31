from bs4 import BeautifulSoup
from requests_html import HTMLSession
import requests


class Novel:
    def __init__(self, url):
        self.base_url = url
        self._content_id = None
        self._first_chapter = 1
        self._last_chapter = None

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

    def extract_content(self):
        if self._last_chapter == None:
            raise Exception("Plese set the final chapter of the novel")
        if self._content_id == None:
            raise Exception("Please define the ID of the content div.")

        contents = {}
        for chapterNumber in range(self.first_chapter, self.last_chapter + 1):
            chapter_url = self.base_url + str(chapterNumber)
            session = HTMLSession()
            webpage = session.get(chapter_url)
            chapter_HTML = webpage.html.html
            soup = BeautifulSoup(chapter_HTML)
            chapter_content = soup.find(id=self.content_id).find_all('p')
            contents[f"Chapter {str(chapterNumber)}"] = chapter_content
        return contents

# first, determine page type (static or dynamic)
# second, determine content id manually
#
#
#
#
#
#
#
#
#
#
#
#
#
# ;
