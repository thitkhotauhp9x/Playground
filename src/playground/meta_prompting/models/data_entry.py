from rich.prompt import Prompt

from playground.meta_prompting.models.form import Form


class DataEntry:
    def __init__(self, form: Form) -> None:
        self._form = form

    def enter(self) -> str:
        content = ""
        for index, field in enumerate(self._form.fields):
            question = f"""{index + 1}. {field.label}?"""
            answer = Prompt.ask(question, default=field.input.placeholder)
            content += f"{question}\n{answer}\n"
        return content
