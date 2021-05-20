import os
import sys
import pathlib
import urllib.request
from typing import List, Optional


class Repo:
    def __init__(self, source_dir):
        self.source_dir: str = source_dir
        self.languages: List[Language] = list()
        self.total_snippets: int = 0
        self.total_tests: int = 0

    def analyze_repo(self):
        for root, directories, files in os.walk(self.source_dir):
            if not directories:
                language = Language(os.path.basename(root), root, files)
                language.analyze_language()
                self.languages.append(language)
        self.compute_total_snippets()
        self.compute_total_tests()

    def compute_total_snippets(self):
        count = 0
        for language in self.languages:
            count += language.total_snippets
        self.total_snippets = count
        
    def compute_total_tests(self):
        count = 0
        for language in self.languages:
            count += 1 if language.get_test_file_path() else 0
        self.total_tests = count

    def get_languages_by_letter(self, letter):
        language_list = [language for language in self.languages if language.name.startswith(letter)]
        return sorted(language_list, key=lambda s: s.name.casefold())


class Language:
    def __init__(self, name: str, path: str, file_list: List[str]):
        self.name: str = name
        self.path: str = path
        self.file_list: List[str] = file_list
        self.total_snippets: int = 0
        self.total_dir_size: int = 0

    def __str__(self):
        return self.name + ";" + str(self.total_snippets) + ";" + str(self.total_dir_size)

    def analyze_language(self):
        self.compute_total_snippets()
        self.computer_total_dir_size()

    def get_test_file_path(self):
        return next((file for file in self.file_list if os.path.splitext(file)[1] == ".yml"), None)

    def compute_total_snippets(self):
        count = 0
        for file in self.file_list:
            file_name, file_ext = os.path.splitext(file)
            if file_ext not in (".md", "", ".yml"):
                count += 1
        self.total_snippets = count

    def computer_total_dir_size(self):
        size = 0
        for file in self.file_list:
            relative_path = os.path.join(self.path, file)
            size += os.path.getsize(relative_path)
        self.total_dir_size = size

class Page:
    def __init__(self, name: str):
        self.name: str = name
        self.wiki_url_base: str = "/jrg94/sample-programs/wiki/"
        self.content = list()

    def __str__(self):
        return self.name + self._build_page()

    def _build_page(self):
        return "\n".join(self.content)

    def add_row(self, row: str):
        self.content.append(row)

    def add_table_header(self, *args):
        column_separator = " | "
        header = column_separator.join(args)
        divider = column_separator.join(["-----"] * len(args))
        self.content.append(header)
        self.content.append(divider)

    def add_table_row(self, *args):
        column_separator = " | "
        row = column_separator.join(args)
        self.content.append(row)

    def add_section_break(self):
        self.content.append("")

    def output_page(self):
        separator = "-"
        file_name = separator.join(self.name.split()) + ".md"
        dump_dir = 'wiki'
        pathlib.Path(dump_dir).mkdir(parents=True, exist_ok=True)
        output_file = open(os.path.join(dump_dir, file_name), "w+")
        output_file.write(self._build_page())
        output_file.close()


class Wiki:
    def __init__(self, repo):
        self.repo: Repo = repo
        self.wiki_url_base: str = "/TheRenegadeCoder/sample-programs/wiki/"
        self.repo_url_base: str = "/TheRenegadeCoder/sample-programs/tree/master/archive/"
        self.tag_url_base: str = "https://sample-programs.therenegadecoder.com/languages/"
        self.issue_url_base: str = "/TheRenegadeCoder/sample-programs/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+"
        self.pages: List[Page] = list()

    @staticmethod
    def _build_link(text: str, url: str) -> str:
        separator = ""
        return separator.join(["[", text, "]", "(", url, ")"])

    @staticmethod
    def verify_link(url):
        request = urllib.request.Request(url)
        request.get_method = lambda: 'HEAD'
        print("Trying: ", url)
        try:
            urllib.request.urlopen(request)
            return True
        except urllib.request.HTTPError:
            return False

    def build_wiki_link(self, text: str, page_name: str) -> str:
        return self._build_link(text, self.wiki_url_base + page_name)

    def build_repo_link(self, text: str, letter: str, language: str) -> str:
        return self._build_link(text, self.repo_url_base + letter + "/" + language)

    def build_tag_link(self, language):
        test_url = self.tag_url_base + language
        if not self.verify_link(test_url):
            markdown_url = ""
        else:
            markdown_url = self._build_link("Here", test_url)
        return markdown_url

    def build_issue_link(self, language: str):
        lang_query = language.replace("-", "+")
        return self._build_link("Here", self.issue_url_base + lang_query)

    def build_test_link(self, language: Language, letter: str):
        file_name = language.get_test_file_path()
        if file_name:
            file_path = self.repo_url_base + letter + "/" + language.name + "/" + file_name
            file_path_link = self._build_link("Here", file_path)
        else:
            file_path_link = ""
        return file_path_link

    def output_pages(self):
        for page in self.pages:
            page.output_page()

    def get_sorted_letters(self):
        unsorted_letters = os.listdir(self.repo.source_dir)
        return sorted(unsorted_letters, key=lambda s: s.casefold())

    def build_alphabet_catalog(self):
        page = Page("Alphabetical Language Catalog")
        alphabetical_list = self.get_sorted_letters()
        page.add_table_header("Collection", "# of Languages", "# of Snippets", "# of Tests")
        for letter in alphabetical_list:
            letter_link = self.build_wiki_link(letter.capitalize(), letter.capitalize())
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
            previous_link = self.build_wiki_link(previous_text, previous_letter)
            next_link = self.build_wiki_link(next_text, next_letter)
            page.add_table_header(previous_link, next_link)
            self.pages.append(page)

    def build_alphabet_page(self, letter):
        page = Page(letter.capitalize())
        introduction = """The following table contains all the existing languages
                    in the repository that start with the letter %s:""" % letter.capitalize()
        page.add_row(introduction)
        page.add_section_break()
        page.add_table_header("Language", "Article(s)", "Issue(s)", "Test(s)", "# of Snippets")
        languages_by_letter = self.repo.get_languages_by_letter(letter)
        total_snippets = 0
        for language in languages_by_letter:
            total_snippets += language.total_snippets
            language_link = self.build_repo_link(language.name.capitalize(), letter, language.name)
            tag_link = self.build_tag_link(language.name)
            issues_link = self.build_issue_link(language.name)
            tests_link = self.build_test_link(language, letter)
            page.add_table_row(language_link, tag_link, issues_link, tests_link, str(language.total_snippets))
        page.add_table_row("**Totals**", "", "", "", str(total_snippets))
        page.add_section_break()
        return page


class ReadMeCatalog:
    def __init__(self, repo):
        self.repo: Repo = repo


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
        self.wiki.build_alphabet_catalog()
        self.wiki.build_alphabet_pages()

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
        self.wiki.output_pages()


def main():
    if len(sys.argv) > 1:
        generator = Generator(sys.argv[1])
        generator.build()
    else:
        print("Please supply an input path")


if __name__ == '__main__':
    main()
