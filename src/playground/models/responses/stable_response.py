from pydantic import BaseModel


class StableResponse[T](BaseModel):
    reasoning: str
    errorMessage: str
    result: T
