from typing import Optional
from bs4 import BeautifulSoup
import feedparser

from generate_docs.markdown import MarkdownPage


def get_intro_text():
    return """Welcome to a collection of Jupyter Notebooks from the 
    [How to Python](https://therenegadecoder.com/series/how-to-python/) series on The Renegade Coder. For convenience, 
    you can access all of the articles, videos, challenges, and source code below. Alternatively, I keep 
    [an enormous article](https://therenegadecoder.com/code/python-code-snippets-for-everyday-problems/) up to date 
    with all these snippets as well.
    """


def get_series_posts():
    index = 1
    base = "https://therenegadecoder.com/series/how-to-python/feed/?paged="
    feed = []
    while (rss := feedparser.parse(f"{base}{index}")).entries:
        feed.extend(rss.entries)
        index += 1
    return feed


def get_youtube_video(entry):
    content = entry.content[0].value
    soup = BeautifulSoup(content, "html.parser")
    target = soup.find("h2", text="Video Summary")
    if target:
        return target.find_next_sibling().find_all("a")[-1]["href"]


class HowTo:
    def __init__(self):
        self.page: Optional[MarkdownPage] = None
        self.feed: Optional[list] = None
        self._load_data()
        self._build_readme()

    def _load_data(self):
        self.feed = get_series_posts()

    def _build_readme(self):
        self.page = MarkdownPage("README")

        # Introduction
        self.page.add_content("# How to Python - Source Code")
        self.page.add_section_break()
        self.page.add_content(get_intro_text())
        self.page.add_section_break()

        # Article List
        self.page.add_table_header("Index", "Title", "Publish Date", "Article", "Video", "Challenge", "Notebook")
        self.build_table()

    def build_table(self):
        index = 1
        for entry in self.feed:
            if "Code Snippets" not in entry.title:
                article = f"[Article]({entry.link})"
                youtube_url = get_youtube_video(entry)
                youtube = f"[Video]({youtube_url})" if youtube_url else ""
                self.page.add_table_row(str(index), entry.title, entry.published, article, youtube, "", "")
                index += 1