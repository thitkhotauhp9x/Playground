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
class OxfordLearnerDictionary:
    word: str
    timeout: Optional[int] = None

    @cached_property
    def soup(self):
        response = get_definition(self.word, self.timeout)
        return BeautifulSoup(response.text, "html.parser")

    def phonetic_br(self):
        results = self.soup.select("div.top-container div.phons_br span.phon")
        if results:
            return results[0].text
        return None

    @property
    def main_column(self):
        return self.soup.find(id="main_column")
