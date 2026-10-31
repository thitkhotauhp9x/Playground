from langchain_core.output_parsers import BaseOutputParser
from app.libs.playground.parsers.block_code_output_parser import BlockCodeOutputParser


LATEX_OUTPUT_PARSER = BlockCodeOutputParser(lang="latex")


class AcupuncturePointOutputParser(BaseOutputParser):
    def __init__(self, point_code: str, images: list[str]) -> None:
        super().__init__()
        self._point_code = point_code
        self._images: list[str] = images

    def parse(self, text: str) -> str:
        return LATEX_OUTPUT_PARSER.parse(text)

    def get_format_instructions(self) -> str:
        illustration = ""
        for image in self._images:
            illustration += f'\\includegraphics[width=\\linewidth]{{"{image}"}}\n'

        return f"""The output is formatted as follows:

```latex
\\subsection{{{self._point_code} <<vietnamese_point_name>>}}
{illustration}

\\subsubsection{{Vị trí}}
<<location_content>>

\\subsubsection{{Chỉ định}}
<<indication_content>>

\\subsubsection{{Ứng dụng}}
<<application_content>>

\\subsubsection{{Kỹ thuật}}
<<technique_content>>

\\subsubsection{{Ghi chú}}
<<note_content>>
```
"""
