import os
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
        self.source_dir: str = source_dir
        self.languages: list[LanguageCollection] = list()
        self.total_snippets: int = 0
        self.total_tests: int = 0
        self._collect_languages()
        self._analyze_repo()

    def _collect_languages(self) -> None:
        """
        Builds a list of language collections.
        :return: None
        """
        for root, directories, files in os.walk(self.source_dir):
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

    def get_languages_by_letter(self, letter: str) -> list:
        """
        A utility method for retrieving all language collections that start with a particular letter.

        :param letter: a character to search by
        :return: a list of programming languages starting with the provided letter
        """
        language_list = [language for language in self.languages if language.name.startswith(letter)]
        return sorted(language_list, key=lambda s: s.name.casefold())


class LanguageCollection:
    """
    An object representing a collection of sample programs files for a particular programming language.
    """

    def __init__(self, name: str, path: str, file_list: list[str]) -> None:
        """
        Constructs an instance of LanguageCollection.
        :param name: the name of the language (e.g., Python)
        :param path: the path of the language (e.g., .../archive/p/python/)
        :param file_list: the list of files in language collection
        """
        self.name: str = name
        self.path: str = path
        self.file_list: list[str] = file_list
        self.sample_programs: list[SampleProgram] = list()
        self.test_file_path: Optional[str] = None
        self.read_me_path: Optional[str] = None
        self.total_snippets: int = 0
        self.total_dir_size: int = 0
        self._collect_sample_programs()
        self._analyze_language_collection()

    def __str__(self) -> str:
        return self.name + ";" + str(self.total_snippets) + ";" + str(self.total_dir_size)

    def _collect_sample_programs(self) -> None:
        """
        Generates a list of sample program objects from all of the files in this language collection.
        :return: None
        """
        for file in self.file_list:
            file_name, file_ext = os.path.splitext(file)
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
