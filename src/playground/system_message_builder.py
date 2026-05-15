from typing import Self


class SystemMessageBuilder:
    def __init__(self):
        self._identity: str | None = None
        self._instructions: list[str] = []

    def set_identity(self, identity: str) -> Self:
        self._identity = identity
        return self

    def add_instruction(self, instruction: str) -> Self:
        self._instructions.append(instruction)
        return self

    def build(self) -> str:
        content = ""
        if self._identity:
            content += f"""\
# Identity
* {self._identity}
"""
        if self._instructions:
            content += f"""\
# Instructions
* {self._instructions}
"""
        return content
