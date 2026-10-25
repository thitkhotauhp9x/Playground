"""Generate a standalone SVG image from a text prompt using a chat model."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.exceptions import OutputParserException
from langchain_openai import ChatOpenAI

from playground.svg_output_parser import SvgOutputParser


SYSTEM_PROMPT = """You create polished, self-contained SVG illustrations from user prompts.
Return only valid SVG markup, starting with <svg and ending with </svg>.
Use a viewBox, include explicit width and height, and use inline SVG shapes and styles.
Do not include scripts, external images, external fonts, or external resources.
Keep the SVG accessible with a title and a concise description when appropriate."""


CHAT_MODEL = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def generate_svg(prompt: str) -> str:
    output_parser = SvgOutputParser()
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", f"{SYSTEM_PROMPT}\n\n{{format_instructions}}"),
            ("human", prompt),
        ]
    )
    chain = prompt_template | CHAT_MODEL | output_parser
    return chain.invoke(
        {
            "prompt": prompt,
            "format_instructions": output_parser.get_format_instructions(),
        }
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate an SVG image from a prompt.")
    parser.add_argument("prompt", help="Describe the image to create.")
    parser.add_argument("-o", "--output", type=Path, default=Path("output.svg"))
    args = parser.parse_args()

    try:
        svg = generate_svg(args.prompt)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(svg, encoding="utf-8")
    except (ValueError, OSError, OutputParserException) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"SVG saved to {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
