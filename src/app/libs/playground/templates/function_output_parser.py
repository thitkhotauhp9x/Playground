import textwrap

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
import pytest

from app.libs.playground.parsers.block_code_output_parser import BlockCodeOutputParser
from app.libs.playground.parsers.function_output_parser import (
    FunctionOutputParser,
    RESPONSE_MODEL_PARSER,
)
from app.libs.playground.templates.instructions import STEP_BY_STEP_INSTRUCTIONS

LLM = ChatOpenAI(model="gpt-4o-mini") | RESPONSE_MODEL_PARSER


def indent(text: str, prefix: str = "  ") -> str:
    return textwrap.indent(textwrap.dedent(text), prefix, lambda line: True).strip()


FORMAT_INSTRUCTIONS = indent(RESPONSE_MODEL_PARSER.get_format_instructions())


@pytest.mark.parametrize(
    "query, expected",
    [
        ("a=1, b=2", 3),
        ("a=-1, b=5", 5),
        ("hello you", None),
    ],
)
def test_algorithm(query: str, expected):
    message = SystemMessage(f"""# Instructions
* {STEP_BY_STEP_INSTRUCTIONS}
* Given variables {{a}}, {{b}}.
  If {{a}} < 0 then {{a}} = 0.
  If {{b}} > 5 then {{b}} = 5.
  Respond with the sum of {{a}} and {{b}}.
* {FORMAT_INSTRUCTIONS}""")
    response = LLM.invoke([message, HumanMessage(query)])
    assert response.result == expected


@pytest.mark.parametrize(
    "query, expected",
    [
        ("a=1, b=2", 3),
        ("a=-1, b=5", 4),
        ("What is the capital of Vietnam?", None),
        ("a='hello', b=1", None),
    ],
)
def test_add_function(query: str, expected) -> None:
    output_parsers = FunctionOutputParser(
        input_variables=["a", "b"],
        functionality="Calculate the sum of a and b and populate the result field with the value.",
    )
    message = SystemMessage(f"""# Instructions
* {STEP_BY_STEP_INSTRUCTIONS}
* {indent(output_parsers.get_format_instructions())}
""")
    print(message.content)
    response = LLM.invoke([message, HumanMessage(query)])
    print(response)
    assert response.result == expected


@pytest.mark.parametrize(
    "query, expected",
    [
        # ("a=1, b=2", 3),
        # ("a=-1, b=5", 4),
        # ("What is the capital of Vietnam?", None),
        ("a='hello', b=1", None),
    ],
)
def test_block_code_output_parser(query: str, expected):
    content = f"""You will be provided with variables a={{a}} and b={{b}}.
If any required variable is missing or invalid, set the error field with a descriptive message.
Execute the function with variables and response result 
```python
def add(a, b):
    return a + b
```
{RESPONSE_MODEL_PARSER.get_format_instructions()}
"""
    message = SystemMessage(f"""# Instructions
* {STEP_BY_STEP_INSTRUCTIONS}
* {indent(content)}
""")
    print(message.content)
    chain = (
        ChatOpenAI(model="gpt-4o-mini")
        | BlockCodeOutputParser(lang="json")
        | RESPONSE_MODEL_PARSER
    )
    response = chain.invoke([message, HumanMessage(query)])
    print(response)
    assert response.result == expected
