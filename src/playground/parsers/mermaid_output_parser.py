from langchain_core.output_parsers import BaseOutputParser
from markdown_it import MarkdownIt

from playground.executors.mermaid_to_svg_converter import convert_mermaid_to_svg
from playground.utils.temp import temp_file


class MermaidOutputParser(BaseOutputParser):
    def __init__(self, lang: str = "mermaid", index: int = -1):
        super().__init__()
        self._md = MarkdownIt()
        self._index: int = index
        self._lang: str = lang

    def parse(self, text: str) -> str:
        tokens = self._md.parse(text)
        mermaid_codes = [
            token.content.strip()
            for token in tokens
            if token.type == "fence" and token.info.strip() == self._lang
        ]
        mermaid_code = mermaid_codes[self._index]

        with temp_file(suffix=".svg") as svg_file:
            convert_mermaid_to_svg(mermaid_code, svg_file.as_posix())

        return mermaid_code
