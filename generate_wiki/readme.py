from generate_wiki.markdown import MarkdownPage
from generate_wiki.repo import Repo


class ReadMeCatalog:
    def __init__(self, repo):
        self.repo: Repo = repo
        self.pages: list[MarkdownPage] = list()

    def build_readme(self, page: MarkdownPage):
        pass
