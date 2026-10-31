from typing import Generic, TypeVar, Type

from langchain_core.output_parsers import BaseOutputParser, PydanticOutputParser

from app.libs.playground.models.responses.response_model import ResponseModel


T = TypeVar("T")


class StructureOutputParser(BaseOutputParser, Generic[T]):
    def __init__(self, instructions: str) -> None:
        super().__init__()
        self._instructions = instructions
        self._output_parser = PydanticOutputParser(
            pydantic_object=ResponseModel[type[T]]
        )

    def get_format_instructions(self) -> str:
        return _FUNCTION_FORMAT_INSTRUCTIONS.format(
            instructions=self._instructions,
            output_format=self._output_parser.get_format_instructions(),
        )

    def parse(self, text: str) -> ResponseModel:
        return self._output_parser.invoke(text)


_FUNCTION_FORMAT_INSTRUCTIONS = """{instructions}
{output_format}
"""
