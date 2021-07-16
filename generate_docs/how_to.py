from typing import Optional
from bs4 import BeautifulSoup
import requests
import feedparser
from snake.md import Document


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


def get_slug(title: str, sep: str):
    return title.split(":")[0][:-10].lower().replace(" ", sep)


def get_challenge(title: str):
    slug = get_slug(title, "-")
    base = "https://github.com/TheRenegadeCoder/how-to-python-code/tree/main/challenges/"
    print(f"Trying {base}{slug}")
    request = requests.get(f"{base}{slug}")
    if request.status_code == 200:
        return f"{base}{slug}"


def get_notebook(title: str):
    slug = get_slug(title, "_")
    base = "https://github.com/TheRenegadeCoder/how-to-python-code/tree/main/notebooks/"
    print(f"Trying {base}{slug}.ipynb")
    request = requests.get(f"{base}{slug}.ipynb")
    if request.status_code == 200:
        return f"{base}{slug}.ipynb"


def get_test(title: str):
    slug = get_slug(title, "_")
    base = "https://github.com/TheRenegadeCoder/how-to-python-code/tree/main/testing/"
    print(f"Trying {base}{slug}.py")
    request = requests.get(f"{base}{slug}.py")
    if request.status_code == 200:
        return f"{base}{slug}.py"


class HowTo:
    def __init__(self):
        self.page: Optional[Document] = None
        self.feed: Optional[list] = None
        self._load_data()
        self._build_readme()

    def _load_data(self):
        self.feed = get_series_posts()

    def _build_readme(self):
        self.page = Document("README")

        # Introduction
        self.page.add_header("How to Python - Source Code")
        self.page.add_paragraph(get_intro_text())

        # Article List
        self.page.add_table_header(
            "Index", 
            "Title", 
            "Publish Date", 
            "Article", 
            "Video", 
            "Challenge", 
            "Notebook",
            "Testing"
        )
        self.build_table()

    def build_table(self):
        index = 1
        for entry in self.feed:
            if "Code Snippets" not in entry.title:
                article = f"[Article]({entry.link})"
                youtube_url = get_youtube_video(entry)
                youtube = f"[Video]({youtube_url})" if youtube_url else ""
                challenge_url = get_challenge(entry.title)
                challenge = f"[Challenge]({challenge_url})" if challenge_url else ""
                notebook_url = get_notebook(entry.title)
                notebook = f"[Notebook]({notebook_url})" if notebook_url else ""
                test_url = get_test(entry.title)
                test = f"[Test]({test_url})" if test_url else ""
                self.page.add_table_row(
                    str(index), 
                    entry.title, 
                    entry.published, 
                    article, 
                    youtube, 
                    challenge, 
                    notebook,
                    test
                )
                index += 1
