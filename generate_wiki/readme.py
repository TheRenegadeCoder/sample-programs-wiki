from generate_wiki.markdown import MarkdownPage, build_doc_link
from generate_wiki.repo import Repo, LanguageCollection


def _get_intro_text(language: LanguageCollection) -> str:
    # TODO: need to think about languages that don't exist in documentation
    return f"""Welcome to Sample Programs in {language.name.capitalize()}! To find 
    documentation related to the {language.name.capitalize()} code in this repo, look 
    [here]({language.sample_program_url})."""


def _get_sample_programs_text() -> str:
    """
    Produces the sample programs boilerplate text about the list of code snippets to follow.
    :return: sample programs boilerplate
    """
    return """Below, you'll find a list of code snippets in this collection.
    Code snippets preceded by :warning: link to an article request 
    issue while code snippets preceded by :white_check_mark: link
    to an existing article which provides further documentation.
    """


def _generate_program_list(language: LanguageCollection) -> list:
    """
    A helper function which generates a list of programs for the README.
    :param language: a language collection
    :return: a list of sample programs list items
    """
    list_items = list()
    for program in language.sample_programs:
        readable_name = program.normalized_name.replace("-", " ").title()
        doc_link = build_doc_link(program, f"{readable_name} in {program.language.capitalize()}")
        list_items.append(f"- {doc_link}")
    return list_items


class ReadMeCatalog:
    """
    An representation of the collection of READMEs in the Sample Programs repo.
    """

    def __init__(self, repo: Repo):
        """
        Constructs an instance of a ReadMeCatalog.
        :param repo: a repository instance
        """
        self.repo: Repo = repo
        self.pages: dict[str, MarkdownPage] = dict()
        self._build_readmes()

    def _build_readme(self, language: LanguageCollection) -> None:
        """
        Creates a README page from a language collection.
        :param language: a programming language collection (e.g., Python)
        :return: None
        """
        page = MarkdownPage("README")
        page.add_content(f"# Sample Programs in {language.name.capitalize()}")
        page.add_section_break()
        page.add_content(_get_intro_text(language))
        page.add_section_break()
        page.add_content("## Sample Programs")
        page.add_section_break()
        page.add_content(_get_sample_programs_text())
        page.add_section_break()
        page.add_content(*_generate_program_list(language))
        page.add_section_break()
        self.pages[language.name] = page

    def _build_readmes(self) -> None:
        """
        Generates all READMEs for the repo.
        :return: None
        """
        for language in self.repo.languages:
            self._build_readme(language)
