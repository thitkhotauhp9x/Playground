from pydantic import BaseModel, Field
from typing import Annotated


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
