import os


class Repo:
    def __init__(self, source_dir):
        self.source_dir: str = source_dir
        self.languages: list[Language] = list()
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
    def __init__(self, name: str, path: str, file_list: list[str]):
        self.name: str = name
        self.path: str = path
        self.file_list: list[str] = file_list
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
