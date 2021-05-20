import os
import pathlib


class Repo:
    def __init__(self, source_dir):
        self.source_dir: str = source_dir
        self.languages: list[LanguageCollection] = list()
        self.total_snippets: int = 0
        self.total_tests: int = 0

    def analyze_repo(self):
        for root, directories, files in os.walk(self.source_dir):
            if not directories:
                language = LanguageCollection(os.path.basename(root), root, files)
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


class LanguageCollection:
    def __init__(self, name: str, path: str, file_list: list[str]):
        self.name: str = name
        self.path: str = path
        self.file_list: list[str] = file_list
        self.sample_programs: list[SampleProgram] = list()
        self.total_snippets: int = 0
        self.total_dir_size: int = 0
        self._collect_sample_programs()
        self._analyze_language_collection()

    def __str__(self):
        return self.name + ";" + str(self.total_snippets) + ";" + str(self.total_dir_size)

    def _collect_sample_programs(self) -> None:
        """
        Generates a list of sample program objects from all of the files in this language collection.
        :return: None
        """
        for file in self.file_list:
            file_name, file_ext = os.path.splitext(file)
            if file_ext not in (".md", "", ".yml"):
                self.sample_programs.append(SampleProgram(self.path, file))

    def _analyze_language_collection(self) -> None:
        """
        Runs some analytics on the collection of sample programs.
        :return: None
        """
        for sample_program in self.sample_programs:
            self.total_dir_size += sample_program.get_size()
        self.total_snippets = len(self.sample_programs)

    def get_test_file_path(self):
        return next((file for file in self.file_list if os.path.splitext(file)[1] == ".yml"), None)


class SampleProgram:
    """
    An object representing a sample program in the repo.
    """
    def __init__(self, path: str, file_name: str):
        self.path = path
        self.file_name = file_name

    def get_size(self) -> int:
        """
        Computes the size of the sample program using the file path.
        :return: the size of the sample program in bytes
        """
        relative_path = os.path.join(self.path, self.file_name)
        return os.path.getsize(relative_path)

    def get_language(self) -> str:
        """
        Determines the language of the sample program from the folder it is contained within.
        :return: the language of the sample program
        """
        return pathlib.PurePath(self.path).name
