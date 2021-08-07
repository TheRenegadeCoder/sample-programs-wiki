from snakemd import Document, Paragraph, InlineText, MDList
from subete import Repo, LanguageCollection


def _get_intro_text(language: LanguageCollection) -> Paragraph:
    paragraph = Paragraph([f"Welcome to Sample Programs in {language}! "])
    text = InlineText("here.", url=language.lang_docs_url())
    if text.verify_url():
        paragraph.add(f"To find documentation related to the {language} code in this repo, look ")
        paragraph.add(text)
    return paragraph


def _get_sample_programs_text() -> str:
    return """
    Below, you'll find a list of code snippets in this collection.
    Code snippets preceded by :warning: link to a GitHub 
    issue query featuring a possible article request issue. If an article request issue 
    doesn't exist, we encourage you to create one. Meanwhile, code snippets preceded 
    by :white_check_mark: link to an existing article which provides further documentation.
    """


def _generate_program_list(language: LanguageCollection) -> MDList:
    """
    A helper function which generates a list of programs for the README.
    :param language: a language collection
    :return: a list of sample programs list items
    """
    list_items = list()
    for program in language.sample_programs().values():
        program_name = f"{program}"
        program_line = Paragraph([f":white_check_mark: {program_name} [Requirements]"]) \
            .insert_link(program_name, program.documentation_url()) \
            .insert_link("Requirements", program.requirements_url())
        if not program_line.verify_urls()[program.documentation_url()]:
            program_line.replace(":white_check_mark:", ":warning:") \
                .replace_link(program.documentation_url(), program.article_issue_query_url())
        list_items.append(program_line)
    return MDList(list_items)


def _generate_credit() -> Paragraph:
    p = Paragraph([
        """
        This page was generated automatically by the Sample Programs Docs Generator. 
        Find out how to support this project on Github.
        """
    ])
    p.insert_link("this project", "https://github.com/TheRenegadeCoder/sample-programs-docs-generator")
    return p


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
        self.pages: dict[str, Document] = dict()
        self._build_readmes()

    def _build_readme(self, language: LanguageCollection) -> None:
        """
        Creates a README page from a language collection.
        :param language: a programming language collection (e.g., Python)
        :return: None
        """
        page = Document("README")

        # Introduction
        page.add_header(f"Sample Programs in {language}")
        page.add_element(_get_intro_text(language))

        # Sample Programs List
        page.add_header("Sample Programs List", level=2)
        page.add_paragraph(_get_sample_programs_text())
        page.add_element(_generate_program_list(language))

        # Testing
        page.add_header("Testing", level=2)
        test_data = language.testinfo()
        if not test_data:
            page.add_paragraph(
                """
                This language currently does not feature testing. If you'd like to help in the efforts to test all of 
                the code in this repo, consider creating a testinfo.yml file with the following information:
                """
            )
            page.add_code("folder:\n  extension:\n  naming:\n\ncontainer:\n  image:\n  tag:\n  cmd:", lang="yml")
        else:
            page.add_paragraph(
                f"The following list shares details about what we're using to test all Sample Programs in {language}."
            )
            page.add_unordered_list([
                f"Docker Image: {test_data['container']['image']}",
                f"Docker Tag: {test_data['container']['tag']}"
            ])
        glotter = page.add_paragraph("See the Glotter project for more information on how to create a testinfo file.")
        glotter.insert_link("Glotter project", "https://github.com/auroq/glotter")
        page.add_horizontal_rule()
        page.add_element(_generate_credit())

        self.pages[language.pathlike_name()] = page

    def _build_readmes(self) -> None:
        """
        Generates all READMEs for the repo.
        :return: None
        """
        for _, language in self.repo.language_collections().items():
            self._build_readme(language)
