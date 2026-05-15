from dataclasses import dataclass

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.output_parsers import (
    StrOutputParser,
    PydanticOutputParser,
)
from pydantic import BaseModel


@dataclass
class BaseChat[T: BaseModel]:
    chat_model: BaseChatModel
    output_parser: PydanticOutputParser[T]
    system_message: SystemMessage
    prompt_messages: list[HumanMessage | AIMessage]

    def query(self, human_message: HumanMessage) -> str:
        response = self.chat_model.invoke(
            [
                self.system_message,
                *self.prompt_messages,
                human_message,
            ]
        )
        content = StrOutputParser().invoke(response)
        return content

    def update_prompt_messages(self) -> None:
        prompt_messages = []
        for message in self.prompt_messages:
            if isinstance(message, HumanMessage):
                prompt_messages.append(message)
                response = self.chat_model.invoke([self.system_message, message])
                prompt_messages.append(response)
        self.prompt_messages = prompt_messages

    def stable_prompt(self, human_message: HumanMessage) -> None:
        first_response = self.query(human_message)
        second_response = self.query(human_message)

        if first_response != second_response:
            # Is not stable result
            pass
