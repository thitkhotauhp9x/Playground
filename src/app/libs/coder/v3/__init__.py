# prompt -> phân tích tâm trạng thói quen sở thích
from pydantic import BaseModel


class User(BaseModel):
    fullname: str
    email: str
    phone: str
    dateOfBirth: str
    gender: str
    hobbies: str
    history: list[str]
