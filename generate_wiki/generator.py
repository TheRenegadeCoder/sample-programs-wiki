import sys
from typing import Optional

from generate_wiki.readme import ReadMeCatalog
from generate_wiki.repo import Repo
from generate_wiki.wiki import Wiki


class Generator:
    """
    The top-level class used to generate wiki and README objects.
    """
    def __init__(self, source_dir):
        self.source_dir = source_dir
        self.repo: Optional[Repo] = None
        self.wiki: Optional[Wiki] = None
        self.readme_catalog: Optional[ReadMeCatalog] = None

    def build(self) -> None:
        """
        Builds the wiki and README objects.
        :return: None
        """
        self.repo = Repo(self.source_dir)
        self.repo.analyze_repo()
        self._build_wiki()
        self._build_readme_catalog()
        self._output_documents()

    def _build_wiki(self) -> None:
        """
        Builds the wiki object from the repo object.
        :return: None
        """
        self.wiki = Wiki(self.repo)
        self.wiki._build_alphabet_catalog()
        self.wiki._build_alphabet_pages()

    def _build_readme_catalog(self) -> None:
        """
        Builds the readme object from the repo object.
        :return:
        """
        self.readme_catalog = ReadMeCatalog(self.repo)

    def _output_documents(self) -> None:
        """
        Outputs all documents associated with the wiki and readme objects.
        :return: None
        """
        for page in self.wiki.pages:
            separator = "-"
            file_name = separator.join(page.name.split()) + ".md"
            page.output_page("wiki", file_name)


def main():
    if len(sys.argv) > 1:
        generator = Generator(sys.argv[1])
        generator.build()
    else:
        print("Please supply an input path")


if __name__ == '__main__':
    main()
