from pydantic import BaseModel


class AppField(BaseModel):
    name: str
    annotation: str
    description: str | None
