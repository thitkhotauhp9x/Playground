from playground.meta_prompting.models.form import Form
from playground.meta_prompting.models.form_field import FormField


class NullForm(Form):
    fields: list[FormField] = []

    @property
    def is_null(self) -> bool:
        return True
