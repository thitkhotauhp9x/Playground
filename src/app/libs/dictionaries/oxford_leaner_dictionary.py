from dataclasses import dataclass
from functools import cached_property
from typing import Optional

from bs4 import BeautifulSoup
from requests import Response, get


def get_definition(word: str, timeout: int | None) -> Response:
    url = f"https://www.oxfordlearnersdictionaries.com/definition/english/{word}"
    response = get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=timeout)
    return response


@dataclass(frozen=True)
class OxfordLearnerDictionaries:
    word: str
    timeout: Optional[int] = None

    @cached_property
    def soup(self):
        response = get_definition(self.word, self.timeout)
        return BeautifulSoup(response.text, "html.parser")

    def phonetic_br(self):
        container = self.soup.find("div", class_="top-container")
        if container is None:
            return None
        phones_br = container.find("div", class_="phons_br")  # type: ignore
        if phones_br is None:
            return None
        phon = phones_br.find("span", class_="phon")  # type: ignore
        if phon is None:
            return None
        return phon.text  # type: ignore

    @property
    def main_column(self):
        return self.soup.find(id="main_column")
