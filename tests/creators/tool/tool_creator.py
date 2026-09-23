import inspect
from abc import ABC, abstractmethod
from typing import Callable, get_type_hints, Self

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from tests.creators.tool.creator import describe_arguments


class Instructions:
    def __init__(self):
        self._identity: str | None = None
        self._instructions: str | None = None
        self._examples: str | None = None

    def set_identity(self, identity: str) -> Self:
        self._identity = identity
        return self

    def set_instructions(self, instructions: str) -> Self:
        self._instructions = instructions
        return self

    def set_examples(self, examples: str) -> Self:
        self._examples = examples
        return self

    def __str__(self) -> str:
        content = ""
        if self._identity:
            content += f"# Identity\n{self._identity}\n"
        if self._instructions:
            content = f"# Instructions\n{self._instructions}\n"
        if self._examples:
            content = f"# Examples\n{self._examples}\n"
        return content


class ToolCreator(ABC):
    def __init__(self, max_retries=3):
        self._max_retries = max_retries
        self._chain = ChatOpenAI(model="gpt-4o-mini") | StrOutputParser()

    def convert_function_to_instructions[**P, R](
        self, func: Callable[P, R], *args: P.args, **kwargs: P.kwargs
    ) -> str:
        type_hints = get_type_hints(func)
        return_type = type_hints["return"]
        messages = [
            SystemMessage(content="Convert a function to OpenAI instructions."),
            HumanMessage(
                content=f"This is the function which need convert to OpenAI instructions:\n{inspect.getsource(func)}"
            ),
        ]
        instructions = self._chain.invoke(messages)
        return instructions

    @abstractmethod
    def evaluate[R](self, func_result: R, openai_result: R) -> bool:
        pass

    def correct_instructions(
        self, instructions: str, function_result, openai_result
    ) -> str:
        pass

    def create[**P, R](
        self, func: Callable[P, R], *args: P.args, **kwargs: P.kwargs
    ) -> str | None:
        func_result = func(*args, **kwargs)

        openai_instructions = self.convert_function_to_instructions(
            func, *args, **kwargs
        )
        messages = [
            SystemMessage(openai_instructions),
            HumanMessage(content=describe_arguments(func, *args, **kwargs)),
        ]

        for counter in range(0, self._max_retries):
            openai_result = self._chain.invoke(messages)
            if self.evaluate(func_result, openai_result):
                return openai_instructions
            else:
                openai_instructions = self.correct_instructions(
                    openai_instructions, func_result, openai_result
                )
        return None


def main():
    """
    content = "Your input fields are:\n"
            for index, item in enumerate(inputs):
                content += (
                    f"{index + 1}. `{item.name}`({item.annotation}): {item.description}\n"
                )
            content += "Your output fields are:\n"
            for index, item in enumerate(outputs):
                content += (
                    f"{index + 1}. `{item.name}`({item.annotation}): {item.description}\n"
                )
    """

    def add(a: int, b: int) -> int:
        return a + b

    type_hints = get_type_hints(add, include_extras=True)

    print(type_hints["return"])
    pass


if __name__ == "__main__":
    main()
