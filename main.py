import WebProcesses

NOVEL_BASE_URL = "https://www.wuxiaworld.com/novel/life-once-again/loa-chapter-"

def main(base_url):
    # do the actual pipeline of making it from web to epub
    LOA = WebProcesses.Novel(base_url)
    LOA.last_chapter = 10
    LOA.content_id = "chapter-content"
    print(LOA.extract_content().keys())

main(NOVEL_BASE_URL)