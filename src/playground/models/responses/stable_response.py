from pydantic import BaseModel
from typing_extensions import deprecated


@deprecated
class StableResponse[T](BaseModel):
    reasoning: str
    errorMessage: str
    result: T
