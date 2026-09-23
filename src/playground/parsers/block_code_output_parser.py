from langchain_core.output_parsers import BaseOutputParser
from markdown_it import MarkdownIt


class BlockCodeOutputParser(BaseOutputParser):
    def __init__(self, lang: str, index: int = -1) -> None:
        super().__init__()
        self._lang = lang
        self._index = index

    def parse(self, text: str) -> str:
        md = MarkdownIt()
        tokens = md.parse(text)

        code_blocks = []
        for token in tokens:
            if token.type == "fence":
                lang = token.info.strip().lower() if token.info else ""

                if lang == self._lang:
                    if token.content:
                        code_blocks.append(token.content.strip())

        if 0 <= self._index < len(code_blocks):
            return code_blocks[self._index]
        return text
