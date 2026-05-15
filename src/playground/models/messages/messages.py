from collections import UserList

from langchain_core.messages import BaseMessage
from hat.formatters.prompt_formater import PromptFormatter  # type: ignore


class Messages(UserList[BaseMessage]):
    pass
