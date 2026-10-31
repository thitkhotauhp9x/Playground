from typing import Annotated

from pydantic import BaseModel, Field

from app.libs.playground.meta_prompting.models.form_input import FormInput


class FormField(BaseModel):
    label: Annotated[
        str,
        Field(
            description="The <label> HTML element represents a caption for an item in"
            " a user interface."
        ),
    ]
    input: Annotated[
        FormInput,
        Field(
            description="The <input> HTML element is used to create interactive controls"
            " for web-based forms in order to accept data from the user; a wide"
            " variety of types of input data and control widgets are available,"
            " depending on the device and user agent. The <input> element is one"
            " of the most powerful and complex in all of HTML due to the sheer"
            " number of combinations of input types and attributes."
        ),
    ]
