from bs4 import BeautifulSoup
from requests import get


class LongManWord:
    def __init__(
        self, word: str, url: str = "https://www.ldoceonline.com/dictionary/{word}"
    ):
        self._word: str = word
        self._url: str = url.format(word=self._word)

    def hyphenation(self) -> str | None:
        response = get(self._url, headers={"User-Agent": "Mozilla/5.0"}, timeout=None)
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.select(".HYPHENATION")
        if results:
            return results[0].text
        return None

    def phonetic(self) -> str | None:
        response = get(self._url, headers={"User-Agent": "Mozilla/5.0"}, timeout=None)
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.select("span.PronCodes span.PRON")
        if results:
            return results[0].text
        return None
