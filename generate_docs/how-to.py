from typing import Optional

from generate_docs.markdown import MarkdownPage


def get_intro_text():
    return """Welcome to a collection of Jupyter Notebooks from the 
    [How to Python](https://therenegadecoder.com/series/how-to-python/) series on The Renegade Coder. For convenience, 
    you can access all of the articles, videos, challenges, and source code below. Alternatively, I keep 
    [an enormous article](https://therenegadecoder.com/code/python-code-snippets-for-everyday-problems/) up to date 
    with all these snippets as well.
    """


class HowTo:
    def __init__(self):
        self.page: Optional[MarkdownPage] = None
        self._build_readme()

    def _build_readme(self):
        self.page = MarkdownPage("README")

        self.page.add_content("# How to Python - Source Code")
        self.page.add_section_break()
        self.page.add_content(get_intro_text())
        self.page.add_section_break()

