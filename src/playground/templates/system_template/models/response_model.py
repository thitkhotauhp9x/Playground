from pydantic import BaseModel, Field
from typing import Annotated

class ResponseModel[T](BaseModel):
    reasoning: Annotated[
        str,
        Field(
            description="Step-by-step reasoning or thought process used to arrive at the final result. "
            "Always generate this first.\n"
            "CRITICAL: Do NOT assume, extrapolate, or invent any missing input values or contextual facts."
            "Work STRICTLY with the provided inputs."
            "If required inputs are missing or ambiguous, state the exact missing information here and fail "
            "gracefully by returning an error."
        ),
    ]
    error: Annotated[
        str | None,
        Field(
            description="An error message if the result cannot be inferred due to invalid inputs, missing context, "
            "or logical issues. Must be explicit JSON null (not 'null' as string) "
            "if operation is successful."
        ),
    ]
    result: Annotated[
        T | None,
        Field(
            description="THIS IS THE MAIN RESPONSE FIELD."
            " The final inferred result. Must be explicit JSON null (not 'null' as string) if an error occurred."
        ),
    ]
