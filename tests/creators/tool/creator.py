from functools import wraps
import inspect
from typing import Callable, Iterable

from langchain_core.messages import HumanMessage, SystemMessage
from playground.utils.dort import dort
from playground.utils.openai_runner import lst, llm_invoke


@llm_invoke
def correct_instruction(
    instruction: SystemMessage, function_result, openai_result
) -> SystemMessage:
    pass


@dort(SystemMessage)
@llm_invoke
@lst
def convert_function_to_instruction(source) -> Iterable[HumanMessage]:
    yield HumanMessage(f"""Convert the function to OpenAI instructions.

```python
{source}
```
""")


def describe_arguments[**P, R](
    func: Callable[P, R], *args: P.args, **kwargs: P.kwargs
) -> str:
    lines = []
    for key, value in inspect.signature(func).bind(*args, **kwargs).arguments.items():
        lines.append(f"{key}={value}")
    return ", ".join(lines)


@llm_invoke
@lst
def invoke_instructions[**P, R](
    instructions: SystemMessage, func: Callable[P, R], *args: P.args, **kwargs: P.kwargs
):
    yield instructions
    yield HumanMessage(describe_arguments(func, *args, **kwargs))


def check_result(function_result, openai_result) -> bool:
    pass


def tool_creator[**P, R](func: Callable[P, R], max_retries=3):
    source = inspect.getsource(func)

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs):
        instructions: SystemMessage = convert_function_to_instruction(source)
        function_result = func(*args, **kwargs)
        for counter in range(0, max_retries):
            openai_result = invoke_instructions(instructions, func, *args, **kwargs)

            if check_result(function_result, openai_result):
                instructions = correct_instruction(
                    instructions, function_result, openai_result
                )
            else:
                break

    return wrapper


