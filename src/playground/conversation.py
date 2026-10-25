from langchain_core.language_models import BaseChatModel
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.output_parsers import (
    StrOutputParser,
)


class Conversation:
    def __init__(self, chat_model: BaseChatModel, system_message: SystemMessage) -> None:
        self._chat_model: BaseChatModel = chat_model
        self._system_message: SystemMessage = system_message
        self._history_messages:  list[HumanMessage | AIMessage] = []

    def chat(self, human_message: HumanMessage) -> str:
        self._history_messages.append(human_message)
        response = self._chat_model.invoke(
            [
                self._system_message,
                self._history_messages,
            ]
        )
        self._history_messages.append(response)
        content = StrOutputParser().invoke(response)
        return content
