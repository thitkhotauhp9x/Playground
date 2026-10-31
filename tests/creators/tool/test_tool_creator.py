import inspect
from functools import partial
from typing import get_type_hints
from collections.abc import Callable

from langchain_core.messages import SystemMessage

from app.libs.playground.utils.dort import dort


def test_describe_arguments() -> None:
    def add(a, b):
        return a + b

    def describe_arguments[**P, R](
        func: Callable[P, R], *args: P.args, **kwargs: P.kwargs
    ) -> str:
        lines = []
        for key, value in (
            inspect.signature(func).bind(*args, **kwargs).arguments.items()
        ):
            lines.append(f"{key}={value}")
        return ", ".join(lines)

    assert describe_arguments(add, 3, 4) == "a=3, b=4"
    assert describe_arguments(add, a=3, b=4) == "a=3, b=4"


def test_system_decorator() -> None:
    @dort(SystemMessage)
    def goodbye() -> str:
        return "goodbye"

    goodbye_message: SystemMessage = goodbye()
    # system = dort(SystemMessage)

    system = partial(dort, SystemMessage)

    @system()
    def hello() -> str:
        return "hello"

    hello_message: SystemMessage = hello()
    import pdb

    pdb.set_trace()

    print(get_type_hints(system))
    # print(get_type_hints(goodbye))
