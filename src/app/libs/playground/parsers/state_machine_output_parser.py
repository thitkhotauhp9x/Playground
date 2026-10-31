from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import BaseOutputParser

from app.libs.playground.parsers.mermaid_output_parser import MermaidOutputParser
from textwrap import indent

from app.libs.playground.utils.openai_runner import llm_invoke


class StateMachineOutputParser(BaseOutputParser):
    def get_format_instructions(self) -> str:
        return "The output must be a Mermaid state machine diagram."

    def parse(self, text: str) -> str:
        return MermaidOutputParser(lang="mermaid", index=-1).parse(text)


@llm_invoke
def draw_word_family(word: str):
    output_parser = StateMachineOutputParser()

    return [
        HumanMessage(f"""# Instructions
* Vẽ sơ đồ thể hiện quy trình chuyển đổi từ loại của từ "{word}"
  {indent(output_parser.get_format_instructions(), "  ", lambda x: True).strip()}
""")
    ]


def main():
    figure = draw_word_family(word="agreement")
    print(figure)


if __name__ == "__main__":
    main()
