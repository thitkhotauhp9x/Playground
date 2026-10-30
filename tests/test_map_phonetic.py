import pytest
from dataclasses import dataclass
from app.libs.phonetic_mapping import map_phonetic


@dataclass
class MappingPhoneticData:
    word: str
    phonetic: str



@pytest.mark.parametrize("word, phonetic", [
    ["abdominal", "phonetic"]
])
def test_map_phonetic(data: MappingPhoneticData) -> None:
    result = map_phonetic(data.word, data.phonetic)
