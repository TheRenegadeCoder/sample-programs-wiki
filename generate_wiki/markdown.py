class MarkdownPage:
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
