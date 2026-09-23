import textwrap
from typing import Annotated

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import PydanticOutputParser, BaseOutputParser
from langchain_openai import ChatOpenAI
import pytest
from pydantic import BaseModel, Field


class ResponseModel[T](BaseModel):
    reasoning: Annotated[
        str,
        Field(
            description="Step-by-step reasoning or thought process used to arrive at the final result. Always generate this first.\n"
            "CRITICAL: Do NOT assume, extrapolate, or invent any missing input values or contextual facts."
            "Work STRICTLY with the provided inputs."
            "If required inputs are missing or ambiguous, state the exact missing information here and fail gracefully by returning an error."
        ),
    ]
    error: Annotated[
        str | None,
        Field(
            description="An error message if the result cannot be inferred due to invalid inputs, missing context, or logical issues. Must be explicit JSON null (not 'null' as string) if operation is successful."
        ),
    ]
    result: Annotated[
        T | None,
        Field(
            description="THIS IS THE MAIN RESPONSE FIELD."
            " The final inferred result. Must be explicit JSON null (not 'null' as string) if an error occurred."
        ),
    ]


RESPONSE_MODEL_PARSER = PydanticOutputParser(pydantic_object=ResponseModel[int])
LLM = ChatOpenAI(model="gpt-4o-mini") | RESPONSE_MODEL_PARSER
FORMAT_INSTRUCTIONS = textwrap.indent(
    RESPONSE_MODEL_PARSER.get_format_instructions(), "* ", lambda line: True
)


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
* Let's work this out in a step by step way to be sure we have the right answer.
* Given variables {{a}}, {{b}}.
  If {{a}} < 0 then {{a}} = 0.
  If {{b}} > 5 then {{b}} = 5.
  Respond with the sum of {{a}} and {{b}}.
{FORMAT_INSTRUCTIONS}""")
    response = LLM.invoke([message, HumanMessage(query)])
    assert response.result == expected


class FunctionOutputParser(BaseOutputParser):
    def get_format_instructions(self) -> str:
        variables = "a = {{a}} and b = {{b}}"
        return _FUNCTION_FORMAT_INSTRUCTIONS.format(variables=variables, output_format=RESPONSE_MODEL_PARSER.get_format_instructions())

    def parse(self, text: str) -> ResponseModel:
        return RESPONSE_MODEL_PARSER.invoke(text)


_FUNCTION_FORMAT_INSTRUCTIONS = """You will be provided with variables {variables}.
If any required variable is missing or invalid, set the error field with a descriptive message.
Otherwise, calculate the sum of a and b and populate the result field with the value."
{output_format}
"""


@pytest.mark.parametrize(
    "query, expected",
    [
        ("a=1, b=2", 3),
        ("a=-1, b=5", 4),
        ("What is the capital of Vietnam?", None),
    ],
)
def test_add_function(query: str, expected) -> None:
    output_parsers = FunctionOutputParser()
    message = SystemMessage(f"""# Instructions
* Let's work this out in a step by step way to be sure we have the right answer.
* {textwrap.indent(output_parsers.get_format_instructions(), "  ", lambda line: True).strip()}
""")
    response = LLM.invoke([message, HumanMessage(query)])
    print(response)
    assert response.result == expected
