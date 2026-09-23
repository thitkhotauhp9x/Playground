import functools
from operator import methodcaller
from pathlib import Path
from typing import Self, Mapping, Callable

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from playground.creators.dort import dort

llm = ChatOpenAI(model="gpt-4o-mini") | StrOutputParser()


def air():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> str:
            return llm.invoke([HumanMessage(content=func(*args, **kwargs))])

        return wrapper


    return decorator

llm_invoke = dort(llm.invoke)
human = dort(HumanMessage)
system = dort(SystemMessage)
ai = dort(AIMessage)


def run(content: str) -> str:
    return llm.invoke([HumanMessage(content=content)])


r = dort(run)


@r
def say_hello():
    return "Hello"


def main():
    response = say_hello()
    print(response)
    response = run("Hello")
    print(response)


class Messages:
    def __init__(self):
        self._system: SystemMessage
        self._queries: list[HumanMessage]

    _LOADING_METHOD_MAP: Mapping[type, Callable[..., str]] = {
        str: lambda content: content,
        Path: methodcaller("read_text", encoding="utf-8"),
    }

    def set_system_message(self, content: str | Path) -> Self:
        self._system = SystemMessage(self._LOADING_METHOD_MAP[type(content)](content))
        return self


def abc():
    return [
        SystemMessage(content="dfdf"),
        HumanMessage(content="Hello"),
        AIMessage(content="World"),
    ]


if __name__ == '__main__':
    main()
