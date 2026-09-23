from typing import Literal, Annotated

from pydantic import BaseModel, Field


class FormInput(BaseModel):
    type: Literal["text"]
    placeholder: Annotated[
        str,
        Field(
            description="""Valid for text, search, url, tel, email, password, and number, the placeholder attribute provides a brief hint to the user as to what kind of information is expected in the field. It should be a word or short phrase that provides a hint as to the expected type of data, rather than an explanation or prompt. The text must not include carriage returns or line feeds. So for example if a field is expected to capture a user's first name, and its label is "First Name", a suitable placeholder might be "e.g., Mustafa"."""
        ),
    ]
