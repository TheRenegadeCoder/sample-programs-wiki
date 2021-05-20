import os
import pathlib


def create_md_link(text: str, url: str) -> str:
    """
    Generates a markdown link in the form [text](url).
    :param text: the link text
    :param url: the url to link
    :return: a markdown link
    """
    separator = ""
    return separator.join(["[", text, "]", "(", url, ")"])


class MarkdownPage:
    def __init__(self, name: str):
        self.name: str = name
        self.ext = ".md"
        self.wiki_url_base: str = "/jrg94/sample-programs/wiki/"
        self.content = list()

    def __str__(self):
        return f"{self.name}\n{self._build_page()}"

    def _build_page(self):
        return "\n".join(self.content)

    def add_content(self, *lines: str):
        for line in lines:
            self.content.append(line)

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

    def add_list_item(self, item: str, depth: int = 0):
        self.content.append(f"{' ' * depth}- {item}")

    def output_page(self, dump_dir):
        pathlib.Path(dump_dir).mkdir(parents=True, exist_ok=True)
        output_file = open(os.path.join(dump_dir, self._get_file_name()), "w+")
        output_file.write(self._build_page())
        output_file.close()

    def _get_file_name(self):
        separator = "-"
        file_name = f"{separator.join(self.name.split())}{self.ext}"
        return file_name
