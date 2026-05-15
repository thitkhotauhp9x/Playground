import asyncio
from typing import Iterable, Callable, Any, Annotated

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from pydantic import BaseModel, Field

from hat.decorators.config import CHAT_MODEL
from hat.messages.message_flattening import flatten_messages


async def make_stable_prompt(messages: list[BaseMessage]) -> None:
    chat_model = ChatOpenAI(model="gpt-4o-mini")
    llm = chat_model | StrOutputParser()

    result = await asyncio.gather(llm.ainvoke(messages), llm.ainvoke(messages))
    if len(set(result)) != 1:
        flattened_messages = flatten_messages(messages)
        for mes in flattened_messages:
            print(mes)


def update_system_message(
    system_message: SystemMessage,
    human_message: HumanMessage,
    ai_messages: list[AIMessage],
) -> Iterable[str]:
    yield """Update the system message to make the result stable.
Bạn được nhận system_message, human_message và các ai_messages là kết quả chạy human_message với
system message. Hiện tại các ai_messages đang trả về các kết quả khác nhau. Tôi muốn bạn hiểu
sự khác nhau giữa các ai_messages và update lại system_message để sao cho những human-message
"""


async def is_stable[Inp, Out](
    runnable: Runnable[Inp, Out],
    inp: Inp,
    times: int,
    evaluate: Callable[[Out], Any] | None = None,
):
    coroutines = [runnable.ainvoke(inp) for _ in range(times)]
    results = await asyncio.gather(*coroutines)
    if evaluate is not None:
        results = [evaluate(result) for result in results]
    return len(set(results)) == 1


assert is_stable(CHAT_MODEL, [HumanMessage("hello")], times=2)


prompt = """
This is an output format

```md
# Identity
{identity}
# Instructions
{instructions}
```
"""


class OutputFormat(BaseModel):
    identity: Annotated[str, Field(description="Who or what somebody/something is")]
    instructions: list[
        Annotated[
            str, Field(description="Detailed information on how to do or use something")
        ]
    ]

    def update(self, inp, out, exp):
        """
        Xac dinh xem instruction nao co van de.
        :param inp:
        :param out:
        :param exp:
        :return:
        """
        pass
    # xac dinh xem instruction nao co van de
    # thuc hien cap nhat instruction
