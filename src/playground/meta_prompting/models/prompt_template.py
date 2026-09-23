from typing import Annotated
from pydantic import BaseModel, Field


class Example(BaseModel):
    user_query: str
    assistance_response: str


class PromptTemplate(BaseModel):
    identity: Annotated[
        str,
        Field(
            description="It should be a string that describes the identity of the AI assistant.",
        ),
    ]
    instructions: list[str]
    examples: list[Example]
