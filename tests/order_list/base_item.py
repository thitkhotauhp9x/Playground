from pydantic import BaseModel


class BaseItem(BaseModel):
    description: str
