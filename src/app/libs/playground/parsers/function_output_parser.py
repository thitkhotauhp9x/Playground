from langchain_core.output_parsers import BaseOutputParser, PydanticOutputParser

from app.libs.playground.models.responses.response_model import ResponseModel


class FunctionOutputParser(BaseOutputParser):
    def __init__(self, input_variables: list[str], functionality: str) -> None:
        super().__init__()
        self._variables = input_variables
        self._functionality = functionality

    def get_format_instructions(self) -> str:
        rows = []
        for variable in self._variables:
            rows.append(f"{variable} = {{{variable}}}")
        return _FUNCTION_FORMAT_INSTRUCTIONS.format(
            variables=", ".join(rows),
            functionality=self._functionality,
            output_format=RESPONSE_MODEL_PARSER.get_format_instructions(),
        )

    def parse(self, text: str) -> ResponseModel:
        return RESPONSE_MODEL_PARSER.invoke(text)


_FUNCTION_FORMAT_INSTRUCTIONS = """You will be provided with variables {variables}.
If any required variable is missing or invalid, set the error field with a descriptive message.
{functionality}
{output_format}
"""
RESPONSE_MODEL_PARSER = PydanticOutputParser(pydantic_object=ResponseModel[int])
