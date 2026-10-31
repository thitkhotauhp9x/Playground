from collections.abc import Callable, Iterable

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from app.libs.playground.utils.dort import dort


chat_model = ChatOpenAI(model="gpt-4o-mini")
llm = chat_model | StrOutputParser()


def lst[**P, R](func: Callable[P, Iterable[R]]) -> Callable[P, list[R]]:
    return dort(lambda x: list(x))(func)


def llm_invoke[**P, R](func: Callable[P, R]) -> Callable[P, str]:
    return dort(llm.invoke)(func)


def human(func: Callable[..., str]) -> Callable[..., HumanMessage]:
    return dort(HumanMessage)(func)


def system(func: Callable[..., str]) -> Callable[..., SystemMessage]:
    return dort(SystemMessage)(func)


def ai(func: Callable[..., str]) -> Callable[..., AIMessage]:
    return dort(AIMessage)(func)


@llm_invoke
def ask(query: str) -> list[HumanMessage]:
    return [HumanMessage(query)]


@llm_invoke
def air(query: str) -> list[HumanMessage]:
    return [HumanMessage(query)]
