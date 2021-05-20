from generate_wiki.markdown import MarkdownPage
from generate_wiki.repo import Repo, LanguageCollection


class ReadMeCatalog:
    def __init__(self, repo):
        self.repo: Repo = repo
        self.pages: list[MarkdownPage] = list()

    def build_readme(self, page: MarkdownPage, language: LanguageCollection):
        page.add_row(f"# Sample Programs in {language.name.capitalize()}")
        page.add_section_break()
        page.add_row()

    def _get_intro_text(self, language: LanguageCollection):
        return f"""Welcome to Sample Programs in {language.name.capitalize()}! To find 
        documentation related to the {language.name.capitalize()} code in this repo, look 
        [here]({language.sample_program_url})."""
