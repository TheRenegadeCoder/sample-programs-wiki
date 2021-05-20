from generate_wiki.markdown import MarkdownPage
from generate_wiki.repo import Repo, LanguageCollection


def _get_intro_text(language: LanguageCollection):
    # TODO: need to think about languages that don't exist in documentation
    return f"""Welcome to Sample Programs in {language.name.capitalize()}! To find 
    documentation related to the {language.name.capitalize()} code in this repo, look 
    [here]({language.sample_program_url})."""


def _get_sample_programs_text():
    return """Below, you'll find a list of code snippets in this collection.
    Code snippets preceded by :warning: link to an article request 
    issue while code snippets preceded by :white_check_mark: link
    to an existing article which provides further documentation.
    """


class ReadMeCatalog:
    def __init__(self, repo):
        self.repo: Repo = repo
        self.pages: list[MarkdownPage] = list()

    def build_readme(self, language: LanguageCollection):
        page = MarkdownPage(f"# Sample Programs in {language.name.capitalize()}")
        page.add_row(_get_intro_text(language))
        page.add_section_break()
        page.add_row("## Sample Programs")
        page.add_section_break()
        page.add_row(_get_sample_programs_text())
        self.pages.append(page)

