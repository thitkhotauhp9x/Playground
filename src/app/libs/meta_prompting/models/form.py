from pydantic import BaseModel

from app.libs.meta_prompting.models.form_field import FormField


class Form(BaseModel):
    fields: list[FormField]

    @property
    def is_null(self) -> bool:
        return False
