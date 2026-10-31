import re
from dataclasses import dataclass


@dataclass()
class Char:
    data: str


@dataclass()
class Str:
    data: list[Char]

    def __str__(self):
        return "".join(*self.data)

    def find_all(self, pattern: str):
        r = re.compile(pattern).findall(str(self))
        if r:
            pass
