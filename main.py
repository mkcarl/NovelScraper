import WebProcesses
from ebooklib import epub
import os
import time

def main():
    NOVEL_BASE_URL = "https://www.wuxiaworld.com/novel/rmji/rmji-chapter-"
    novel = WebProcesses.Novel(NOVEL_BASE_URL, 0, 2110) # Change me
    novel.content_id = "chapter-content" # Change me
    novel.name = "A Record of a Mortal's Journey to Immortality".replace(' ', '_') # Change me
    novel.extract_content(asynchronous=True, ratelimit=60)
    novel.export("html")

    book = epub.EpubBook()
    book.set_identifier("rmji") # Change me
    book.set_title(novel.name.replace('_', ' '))
    book.set_language("en")
    book.add_author("Default Author") # Change me

    book_chapters = []
    for chapter in os.listdir(f"chapters/{novel.name}"):
        with open(f"chapters/{novel.name}/{chapter}", "r", encoding="utf-8") as f:
            c = epub.EpubHtml(
                title=chapter,
                file_name=f"{chapter}.html"
                )
            c.set_content(f.read())
            book_chapters.append(c)

    for chapter in book_chapters:
        book.add_item(chapter)
    book_chapters_link = [epub.Link(x.file_name, x.title.split('.')[0], x.title.split('.')[0]) for x in book_chapters]
    book.toc = tuple(book_chapters_link)
    book.spine = book_chapters
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    epub.write_epub(f"{book.title}.epub", book, {})

def print_timer(func):
    t1 = time.time()
    func()
    print(f"Process took {time.time() - t1} seconds")



print_timer(main)

