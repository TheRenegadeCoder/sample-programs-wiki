"""
The repo module contains all the classes need to represent the Sample Programs repo.
This file was designed with the intent of creating read-only objects that fully
represent the underlying repo. Ideally, classes that make use of these objects
should not need to know how they were generated. For example, we do not want users
to poke around the source directory that was used to generate these files. As a result,
users should make use of the public fields only.
"""

import os
import re
import yaml
from typing import Optional


class Repo:
    """
    An object representing the Sample Programs repository.
    """

    def __init__(self, source_dir: str) -> None:
        """
        Constructs an instance of Repo.
        :param source_dir: the location of the repo (e.g., C://.../sample-programs)
        """
        self._source_dir: str = source_dir
        self.languages: list[LanguageCollection] = list()
        self.total_snippets: int = 0
        self.total_tests: int = 0
        self._collect_languages()
        self._analyze_repo()
        self._organize_repo()

    def _collect_languages(self) -> None:
        """
        Builds a list of language collections.
        :return: None
        """
        for root, directories, files in os.walk(self._source_dir):
            if not directories:
                language = LanguageCollection(os.path.basename(root), root, files)
                self.languages.append(language)

    def _analyze_repo(self) -> None:
        """
        Provides analytics for the repo.
        :return: None
        """
        for language in self.languages:
            self.total_snippets += language.total_snippets
            self.total_tests += 1 if language.test_file_path else 0

    def _organize_repo(self) -> None:
        """
        Sorts the repo in alphabetical order by language name.
        :return: None
        """
        self.languages.sort(key=lambda lang: lang.name.casefold())

    def get_languages_by_letter(self, letter: str) -> list:
        """
        A utility method for retrieving all language collections that start with a particular letter.

        :param letter: a character to search by
        :return: a list of programming languages starting with the provided letter
        """
        language_list = [language for language in self.languages if language.name.startswith(letter)]
        return sorted(language_list, key=lambda s: s.name.casefold())

    def get_sorted_language_letters(self):
        """
        A utility method which generates a list of sorted letters from the sample programs archive.
        :return: a sorted list of letters
        """
        unsorted_letters = os.listdir(self._source_dir)
        return sorted(unsorted_letters, key=lambda s: s.casefold())


class LanguageCollection:
    """
    An object representing a collection of sample programs files for a particular programming language.
    """

    def __init__(self, name: str, path: str, file_list: list[str]) -> None:
        """
        Constructs an instance of LanguageCollection.
        :param name: the name of the language (e.g., python)
        :param path: the path of the language (e.g., .../archive/p/python/)
        :param file_list: the list of files in language collection
        """
        self.name: str = name
        self.path: str = path
        self.file_list: list[str] = file_list
        self.first_letter: str = name[0]
        self.sample_programs: list[SampleProgram] = list()
        self.test_file_path: Optional[str] = None
        self.read_me_path: Optional[str] = None
        self.sample_program_url: Optional[str] = None
        self.total_snippets: int = 0
        self.total_dir_size: int = 0
        self._collect_sample_programs()
        self._analyze_language_collection()
        self._generate_urls()
        self._organize_collection()

    def __str__(self) -> str:
        return self.name + ";" + str(self.total_snippets) + ";" + str(self.total_dir_size)

    def _collect_sample_programs(self) -> None:
        """
        Generates a list of sample program objects from all of the files in this language collection.
        :return: None
        """
        for file in self.file_list:
            file_name, file_ext = os.path.splitext(file)
            file_ext = file_ext.lower()
            if file_ext not in (".md", "", ".yml"):
                self.sample_programs.append(SampleProgram(self.path, file, self.name))
            elif file_ext == ".yml":
                self.test_file_path = os.path.join(file)
            elif file_name == "README":
                self.read_me_path = os.path.join(self.path, file)

    def _analyze_language_collection(self) -> None:
        """
        Runs some analytics on the collection of sample programs.
        :return: None
        """
        for sample_program in self.sample_programs:
            self.total_dir_size += sample_program.get_size()
        self.total_snippets = len(self.sample_programs)

    def _generate_urls(self) -> None:
        self.sample_program_url = f"https://sample-programs.therenegadecoder.com/languages/{self.name}"

    def _organize_collection(self):
        self.sample_programs.sort(key=lambda program: program.normalized_name.casefold())

    def get_readable_name(self) -> str:
        """
        Generates as close to the proper language name as possible given a language
        name in plain text separated by hyphens
            EX: google-apps-script -> Google Apps Script
            EX: c-sharp -> C#
        :return: a readable representation of the language name
        """
        text_to_symbol = {
            "plus": "+",
            "sharp": "#",
            "star": r"\*"
        }
        tokens = [text_to_symbol.get(token, token) for token in self.name.split("-")]
        if any(token in text_to_symbol.values() for token in tokens):
            return "".join(tokens).title()
        else:
            return " ".join(tokens).title()

    def get_test_data(self) -> Optional[dict]:
        test_data = None
        if self.test_file_path:
            with open(os.path.join(self.path, self.test_file_path)) as test_file:
                test_data = yaml.safe_load(test_file)
        return test_data


class SampleProgram:
    """
    An object representing a sample program in the repo.
    """

    def __init__(self, path: str, file_name: str, language: str):
        """
        Constructs a sample program.
        :param path: the path to the sample program without the file name
        :param file_name: the name of the file including the extension
        :param language: the programming language of this sample program
        """
        self.path = path
        self.file_name = file_name
        self.language = language
        self.sample_program_doc_url: Optional[str] = None
        self.sample_program_issue_url: Optional[str] = None
        self.normalized_name: Optional[str] = None
        self._generate_urls()

    def get_size(self) -> int:
        """
        Computes the size of the sample program using the file path.
        :return: the size of the sample program in bytes
        """
        relative_path = os.path.join(self.path, self.file_name)
        return os.path.getsize(relative_path)

    def get_language(self) -> str:
        """
        Retrieves the language name for this sample program.
        :return: the language of the sample program
        """
        return self.language

    def _normalize_program_name(self):
        stem = os.path.splitext(self.file_name)[0]
        if len(stem.split("-")) > 1:
            url = stem
        elif len(stem.split("_")) > 1:
            url = stem.replace("_", "-")
        else:
            url = "-".join(re.findall('[a-zA-Z][^A-Z]*', stem)).lower()
        return url

    def _generate_urls(self) -> None:
        doc_url_base = "https://sample-programs.therenegadecoder.com/projects"
        issue_url_base = "https://github.com//TheRenegadeCoder/" \
                         "sample-programs-website/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+"

        self.normalized_name = self._normalize_program_name()

        # doc URL
        self.sample_program_doc_url = f"{doc_url_base}/{self.normalized_name}/{self.language}"

        # issue URL
        program = self.normalized_name.replace("-", "+")
        self.sample_program_issue_url = f"{issue_url_base}{program}+{self.language}"
