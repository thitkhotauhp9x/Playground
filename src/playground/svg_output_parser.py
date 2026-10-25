"""Output parser for extracting SVG content from a Markdown code fence."""

from __future__ import annotations

from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import BaseOutputParser
from markdown_it import MarkdownIt


class SvgOutputParser(BaseOutputParser[str]):
    """Return the content of the last SVG Markdown code fence."""

    def parse(self, text: str) -> str:
        tokens = MarkdownIt().parse(text)
        svg_fences = [
            token.content
            for token in tokens
            if token.type == "fence" and token.info.strip().lower() == "svg"
        ]

        if not svg_fences:
            raise OutputParserException(
                "markdown-it could not find an SVG code fence in the model response."
            )

        return svg_fences[-1].rstrip()

    @property
    def _type(self) -> str:
        return "svg_output_parser"

    def get_format_instructions(self) -> str:
        return (
            "Return exactly one Markdown code block with the language label `svg`. "
            "Put the complete SVG markup inside the block and include no text before or after it."
        )
