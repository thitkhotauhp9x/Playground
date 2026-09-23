from typing import Annotated, Any

from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class Response(BaseModel):
    reasoning: Annotated[
        str, Field(description="Step by step to form inputs to get result or errors")
    ]
    result: Annotated[Any, Field(description="The result of the execution with inputs")]
    errors: Annotated[
        str | None, Field(description="Error messages when the inputs have problems")
    ]


class StructuredSystemMessage(BaseModel):
    identity: Annotated[
        str,
        Field(
            description="Answer for the question 'What does OpenAI play a role in the conversation?'"
        ),
    ]
    instructions: Annotated[
        str, Field(description="How does OpenAI execute to do user requirements?")
    ]
    examples: Annotated[
        str | None, Field(description="Examples in input and output.")
    ] = None

    def to_message(self) -> SystemMessage:
        return SystemMessage(str(self))

    def __str__(self) -> str:
        content = f"""# Identity
{self.identity}

# Instructions
{self.instructions}
{PydanticOutputParser(pydantic_object=Response).get_format_instructions()}
"""
        if self.examples:
            content += f"""
# Examples
{self.examples}
"""
        return content


SSM_OUTPUT_PARSER = PydanticOutputParser(pydantic_object=StructuredSystemMessage)
