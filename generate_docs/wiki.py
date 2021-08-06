from snakemd import Document, InlineText, Paragraph, Table
from subete import Repo, LanguageCollection


class Wiki:
    """
    An object representing a GitHub wiki.
    """

    def __init__(self, repo: Repo):
        """
        Constructs an instance of a Wiki.
        :param repo: a GitHub repository object
        """
        self.repo: Repo = repo
        self.wiki_url_base: str = "/TheRenegadeCoder/sample-programs/wiki/"
        self.repo_url_base: str = "/TheRenegadeCoder/sample-programs/tree/main/archive/"
        self.issue_url_base: str = "/TheRenegadeCoder/sample-programs/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+"
        self.pages: list[Document] = list()
        self._build_alphabet_catalog()
        self._build_alphabet_pages()

    def _build_repo_link(self, text: str, letter: str, language: str) -> InlineText:
        """
        A helper method which creates a link to the language folder in the repo
        (e.g., https://github.com/TheRenegadeCoder/sample-programs/tree/main/archive/c/c-sharp.)

        :param str text: the link text
        :param str letter: the starting letter of the language
        :param str language: the language to link
        :return: a markdown link to a sample programs language page
        """
        return InlineText(text, url=f"{self.repo_url_base}{letter}/{language}")

    def _build_issue_link(self, language: str) -> InlineText:
        """
        A helper method which creates a link to all issues matching that language.

        :param str language: the language to search for issues
        :return: a markdown link to a GitHub query for issues matching this language
        """
        lang_query = language.replace("-", "+")
        return InlineText("Here", f"{self.issue_url_base}{lang_query}")

    @staticmethod
    def _build_test_link(language: LanguageCollection) -> InlineText:
        """
        A helper method which creates a link to the test file for a given language collection.

        :param LanguageCollection language: a language collection
        :return: a markdown link to a test file if it exists; an empty string otherwise
        """
        test = InlineText("Here", url=language.testinfo_url())
        if not test.verify_url():
            test = InlineText("")
        return test

    @staticmethod
    def _build_language_link(language: LanguageCollection) -> InlineText:
        """
        A handy abstraction for the create_md_link() method which creates a link to a sample programs language page.
        (e.g., https://sample-programs.therenegadecoder.com/languages/c/)

        :param LanguageCollection language: the language to link
        :return: a markdown link to the language page if it exists; an empty string otherwise
        """
        lang = InlineText("Here", language.lang_docs_url())
        if not lang.verify_url():
            lang = InlineText("")
        return lang

    def _build_alphabet_page(self, letter: str) -> Document:
        """
        A helper method which generates a single wiki alphabet page given a letter.

        :param str letter: the starting letter of a set of programming languages (e.g., "p" for [pascal, perl, python])
        :return: a alphabet page markdown document
        """
        page = Document(letter.capitalize())
        page.add_paragraph(
            f"""
            The following table contains all the existing languages in the repository that start with the letter 
            {letter.capitalize()}:
            """
        )
        header = ["Language", "Article(s)", "Issue(s)", "Test(s)", "# of Snippets"]
        body = []
        languages_by_letter = self.repo.get_languages_by_letter(letter)
        total_snippets = 0
        for language in languages_by_letter:
            total_snippets += language.total_programs()
            language_link = self._build_repo_link(str(language), letter, str(language))
            tag_link = self._build_language_link(language)
            issues_link = self._build_issue_link(str(language))
            tests_link = self._build_test_link(language)
            body.append([language_link, tag_link, issues_link, tests_link, str(language.total_programs())])
        body.append(["**Totals**", "", "", "", str(total_snippets)])
        page.add_element(Table(header, body))
        return page

    def _build_alphabet_pages(self) -> None:
        """
        Builds a set of wiki alphabet pages from the repo.

        :return: None
        """
        alphabetical_list = self.repo.get_sorted_language_letters()
        for index, letter in enumerate(alphabetical_list):
            page = self._build_alphabet_page(letter)
            previous_index = index - 1
            next_index = (index + 1) % len(alphabetical_list)
            previous_letter = alphabetical_list[previous_index].capitalize()
            next_letter = alphabetical_list[next_index].capitalize()
            previous_text = f"Previous ({previous_letter})"
            next_text = f"Next ({next_letter})"
            previous_link = InlineText(previous_text, url=f"{self.wiki_url_base}{previous_letter}")
            next_link = InlineText(next_text, url=f"{self.wiki_url_base}{next_letter}")
            page.add_element(Paragraph(["< ", previous_link, " | ", next_link, " >"]))
            self.pages.append(page)

    def _build_alphabet_catalog(self) -> None:
        """
        Builds a wiki alphabet catalog from the repo.
        :return: None
        """
        page = Document("Alphabetical Language Catalog")
        alphabetical_list = self.repo.get_sorted_language_letters()
        header = ["Collection", "# of Languages", "# of Snippets", "# of Tests"]
        body = []
        for letter in alphabetical_list:
            letter_link = InlineText(letter.capitalize(), url=f"{self.wiki_url_base}{letter.capitalize()}")
            languages_by_letter = self.repo.get_languages_by_letter(letter)
            num_of_languages = len(languages_by_letter)
            num_of_snippets = sum([language.total_programs() for language in languages_by_letter])
            num_of_tests = sum(1 for language in languages_by_letter if language.has_testinfo())
            body.append([letter_link, str(num_of_languages), str(num_of_snippets), str(num_of_tests)])
        body.append([
            "**Totals**",
            str(len(self.repo.language_collections())),
            str(self.repo.total_programs()),
            str(self.repo.total_tests())
        ])
        page.add_table(header, body)
        self.pages.append(page)
