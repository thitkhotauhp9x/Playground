from collections import UserList

from langchain_core.messages import BaseMessage


class Messages(UserList[BaseMessage]):
    pass
