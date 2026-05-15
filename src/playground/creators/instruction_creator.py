from typing import Iterable, Callable

from hat.decorators.air import air


class InstructionCreator:
    def __init__(self, prompt: str) -> None:
        self._prompt: str = prompt

    @air
    def create(self) -> Iterable[str]:
        yield f"""Create instructions (detailed information on how to do or use something) \
for the following prompt (an instruction given to an artificial intelligence program \
to tell it what you want it to produce):

> {self._prompt}\
"""
        yield f"""If there are multiple methods (a particular way of doing something), \
select the most appropriate one to generate the instructions. \
Output only the instructions you have selected.\
"""


def create_instruction[**P](func: Callable[P, str]) -> Callable[P, str]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> str:
        prompt = func(*args, **kwargs)
        instructions = InstructionCreator(prompt=prompt).create()
        return instructions
    return wrapper
