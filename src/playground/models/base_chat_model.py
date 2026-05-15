from typing import Annotated

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from hat.playground.models.messages.messages import Messages  # type: ignore
from hat.playground.models.input_agent_model import InputAgentModel  # type: ignore


class BaseChatModel(BaseModel):
    model: Annotated[
        BaseChatModel, Field(default_factory=lambda: ChatOpenAI(model="gpt-4o-mini"))
    ]
    system_message: Annotated[
        SystemMessage, Field(default_factory=lambda: SystemMessage(content=""))
    ]
    prompt_messages: Annotated[
        list[HumanMessage | AIMessage], Field(default_factory=list)
    ]
