import re
from dataclasses import dataclass


@dataclass
class Item:
    value: str
    name: str


class Reg:
    pass


def sre(value: str):
    characters = dict(enumerate(list(value)))
    print(characters)
    x = re.compile("el").findall(value)
    print(x)


def main():
    sre("hello")


if __name__ == "__main__":
    main()
