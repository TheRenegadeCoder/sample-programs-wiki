import logging
import sys
from typing import Optional

from subete import Repo

from generate_docs.how_to import HowTo
from generate_docs.readme import ReadMeCatalog
from generate_docs.wiki import Wiki


class Generator:
    """
    The top-level class used to generate wiki and README objects.
    """

    def __init__(self, source_dir):
        self.source_dir = source_dir
        self.repo: Repo = Repo(source_dir=self.source_dir)

    def generate_wiki(self) -> None:
        """
        Builds and outputs the wiki.
        :return: None
        """
        wiki = Wiki(self.repo)
        for page in wiki.pages:
            page.output_page("wiki")

    def generate_readmes(self) -> None:
        """
        Builds and outputs the READMEs.
        :return:
        """
        readme_catalog = ReadMeCatalog(self.repo)
        for language, page in readme_catalog.pages.items():
            page.output_page(f"{self.source_dir}/{language[0]}/{language}")


def _create_generator() -> Optional[Generator]:
    """
    Creates the generator object from
    :return:
    """
    if len(sys.argv) > 1:
        generator = Generator(sys.argv[1])
        return generator
    else:
        print("Please supply an input path")
        exit(1)


def main_wiki():
    """
    Builds the wiki.
    :return: None
    """
    _create_generator().generate_wiki()


def main_readmes():
    """
    Builds the READMEs.
    :return: None
    """
    _create_generator().generate_readmes()


def main_how_to():
    how_to = HowTo()
    how_to.page.output_page("")


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main_wiki()
    main_readmes()
    main_how_to()
