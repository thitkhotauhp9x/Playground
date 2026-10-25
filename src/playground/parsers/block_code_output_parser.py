from langchain_core.output_parsers import BaseOutputParser
from markdown_it import MarkdownIt


class BlockCodeOutputParser(BaseOutputParser):
    def __init__(self, lang: str, index: int = -1) -> None:
        super().__init__()
        self._lang = lang
        self._index = index
        self._md = MarkdownIt()

    def parse(self, text: str) -> str:
        tokens = self._md.parse(text)
        code_blocks = []
        for token in tokens:
            if token.type == "fence":
                lang = token.info.strip().lower() if token.info else ""

                if lang == self._lang:
                    if token.content:
                        code_blocks.append(token.content.strip())
        return code_blocks[self._index]
