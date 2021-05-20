import os
import urllib.request

from generate_wiki.markdown import MarkdownPage, create_md_link
from generate_wiki.repo import Repo, LanguageCollection


class Wiki:
    def __init__(self, repo):
        self.repo: Repo = repo
        self.wiki_url_base: str = "/TheRenegadeCoder/sample-programs/wiki/"
        self.repo_url_base: str = "/TheRenegadeCoder/sample-programs/tree/main/archive/"
        self.tag_url_base: str = "https://sample-programs.therenegadecoder.com/languages/"
        self.issue_url_base: str = "/TheRenegadeCoder/sample-programs/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+"
        self.pages: list[MarkdownPage] = list()

    @staticmethod
    def verify_link(url):
        """
        Verifies that a URL is a valid URL.
        :param url: a website URL
        :return: True if the URL is valid; False otherwise
        """
        request = urllib.request.Request(url)
        request.get_method = lambda: 'HEAD'
        print(f"Trying: {url}")
        try:
            urllib.request.urlopen(request)
            return True
        except urllib.request.HTTPError:
            print(f"{url} is invalid")
            return False

    def _build_wiki_link(self, text: str, page_name: str) -> str:
        """
        A helper method which creates a link to a wiki page.
        (e.g., https://github.com/TheRenegadeCoder/sample-programs/wiki/S)
        :param text: the text to display for the link
        :param page_name: the name of the page to link
        :return: a markdown link to a wiki page
        """
        return create_md_link(text, self.wiki_url_base + page_name)

    def _build_repo_link(self, text: str, letter: str, language: str) -> str:
        """
        A helper method which creates a link to the language folder in the repo
        (e.g., https://github.com/TheRenegadeCoder/sample-programs/tree/main/archive/c/c-sharp.)
        :param text: the link text
        :param letter: the starting letter of the language
        :param language: the language to link
        :return: a markdown link to a sample programs language page
        """
        return create_md_link(text, self.repo_url_base + letter + "/" + language)

    def build_tag_link(self, language):
        test_url = self.tag_url_base + language
        if not self.verify_link(test_url):
            markdown_url = ""
        else:
            markdown_url = create_md_link("Here", test_url)
        return markdown_url

    def build_issue_link(self, language: str):
        lang_query = language.replace("-", "+")
        return create_md_link("Here", self.issue_url_base + lang_query)

    def build_test_link(self, language: LanguageCollection, letter: str):
        file_name = language.get_test_file_path()
        if file_name:
            file_path = self.repo_url_base + letter + "/" + language.name + "/" + file_name
            file_path_link = create_md_link("Here", file_path)
        else:
            file_path_link = ""
        return file_path_link

    def get_sorted_letters(self):
        unsorted_letters = os.listdir(self.repo.source_dir)
        return sorted(unsorted_letters, key=lambda s: s.casefold())

    def build_alphabet_catalog(self):
        page = MarkdownPage("Alphabetical Language Catalog")
        alphabetical_list = self.get_sorted_letters()
        page.add_table_header("Collection", "# of Languages", "# of Snippets", "# of Tests")
        for letter in alphabetical_list:
            letter_link = self._build_wiki_link(letter.capitalize(), letter.capitalize())
            languages_by_letter = self.repo.get_languages_by_letter(letter)
            num_of_languages = len(languages_by_letter)
            num_of_snippets = sum([language.total_snippets for language in languages_by_letter])
            num_of_tests = sum([1 if language.get_test_file_path() else 0 for language in languages_by_letter])
            page.add_table_row(letter_link, str(num_of_languages), str(num_of_snippets), str(num_of_tests))
        page.add_table_row("**Totals**", str(len(self.repo.languages)), str(self.repo.total_snippets), str(self.repo.total_tests))
        self.pages.append(page)

    def build_alphabet_pages(self):
        alphabetical_list = self.get_sorted_letters()
        for index, letter in enumerate(alphabetical_list):
            page = self.build_alphabet_page(letter)
            previous_index = index - 1
            next_index = (index + 1) % len(alphabetical_list)
            previous_letter = alphabetical_list[previous_index].capitalize()
            next_letter = alphabetical_list[next_index].capitalize()
            previous_text = "Previous (%s)" % previous_letter
            next_text = "Next (%s)" % next_letter
            previous_link = self._build_wiki_link(previous_text, previous_letter)
            next_link = self._build_wiki_link(next_text, next_letter)
            page.add_table_header(previous_link, next_link)
            self.pages.append(page)

    def build_alphabet_page(self, letter):
        page = MarkdownPage(letter.capitalize())
        introduction = """The following table contains all the existing languages
                    in the repository that start with the letter %s:""" % letter.capitalize()
        page.add_row(introduction)
        page.add_section_break()
        page.add_table_header("Language", "Article(s)", "Issue(s)", "Test(s)", "# of Snippets")
        languages_by_letter = self.repo.get_languages_by_letter(letter)
        total_snippets = 0
        for language in languages_by_letter:
            total_snippets += language.total_snippets
            language_link = self._build_repo_link(language.name.capitalize(), letter, language.name)
            tag_link = self.build_tag_link(language.name)
            issues_link = self.build_issue_link(language.name)
            tests_link = self.build_test_link(language, letter)
            page.add_table_row(language_link, tag_link, issues_link, tests_link, str(language.total_snippets))
        page.add_table_row("**Totals**", "", "", "", str(total_snippets))
        page.add_section_break()
        return page
