import sys

import itertools
from typing import Any
import regex as re
from pip._internal.resolution.resolvelib import candidates

from app.libs.dictionaries.longman_dictionary import LongManWord
from app.libs.dictionaries.oxford_leaner_dictionary import OxfordLearnerDictionary
from app.libs.dictionaries.regex_dict import RegexDict


def get_letters(word: str) -> list[str]:
    pattern = r"""
    (?(DEFINE)
        (?<vowel>u|e|o|a|i)
        (?<consonant>b|c|d|f|g|h|j|k|l|m|n|p|q|r|s|t|v|w|x|y|z)
    )
    (?&vowel)|(?&consonant)
    """
    formatted_pattern = re.sub(r"\s", "", pattern)
    return re.compile(formatted_pattern).findall(word)


def get_letter_consonants(word: str) -> list[str]:
    pattern = r"""
    (?(DEFINE)
        (?<vowel>u|e|o|a|i|y)
        (?<consonant>b|c|d|f|g|h|j|k|l|m|n|p|q|r|s|t|v|w|x|z)
    )
    (?&consonant)
    """
    formatted_pattern = re.sub(r"\s", "", pattern)
    return re.compile(formatted_pattern).findall(word)


def get_letter_vowels(word: str) -> list[str]:
    pattern = r"""
    (?(DEFINE)
        (?<vowel>u|e|o|a|i|y)
        (?<consonant>b|c|d|f|g|h|j|k|l|m|n|p|q|r|s|t|v|w|x|z)
    )
    (?&vowel)
    """
    formatted_pattern = re.sub(r"\s", "", pattern)
    return re.compile(formatted_pattern).findall(word)


def get_phonemes(phonetic: str) -> list[str]:
    pattern = r"""
    (?(DEFINE)
        (?<long_vowel>iː|ɑː|uː|ɔː|ɜː)
        (?<short_vowel>i|ɪ|ʌ|æ|ʊ|u|ɒ|e|ə)
        (?<diphthong>eɪ|əʊ|aɪ|ɔɪ|aʊ|ɪə|eə|ʊə)
        (?<consonant>tʃ|dʒ|p|b|t|d|k|g|f|v|θ|ð|s|z|ʃ|ʒ|h|m|n|ŋ|l|r|j|w)
        (?<vowel>(?&diphthong)|(?&long_vowel)|(?&short_vowel))
        (?<phonetic>(?&vowel)|(?&consonant))
        (?<stress>ˈ)
    )
    (?&vowel)|(?&consonant)
    """
    formatted_pattern = re.sub(r"\s", "", pattern)
    return re.compile(formatted_pattern).findall(phonetic)


def get_phoneme_consonants(phonetic: str) -> list[str]:
    pattern = r"""
    (?(DEFINE)
        (?<long_vowel>iː|ɑː|uː|ɔː|ɜː)
        (?<short_vowel>i|ɪ|ʌ|æ|ʊ|u|ɒ|e|ə)
        (?<diphthong>eɪ|əʊ|aɪ|ɔɪ|aʊ|ɪə|eə|ʊə)
        (?<consonant>tʃ|dʒ|p|b|t|d|k|g|f|v|θ|ð|s|z|ʃ|ʒ|h|m|n|ŋ|l|r|j|w)
        (?<vowel>(?&diphthong)|(?&long_vowel)|(?&short_vowel))
        (?<phonetic>(?&vowel)|(?&consonant))
        (?<stress>ˈ)
    )
    (?&consonant)
    """
    formatted_pattern = re.sub(r"\s", "", pattern)
    return re.compile(formatted_pattern).findall(phonetic)


def get_phoneme_vowels(phonetic: str) -> list[str]:
    pattern = r"""
    (?(DEFINE)
        (?<long_vowel>iː|ɑː|uː|ɔː|ɜː)
        (?<short_vowel>i|ɪ|ʌ|æ|ʊ|u|ɒ|e|ə)
        (?<diphthong>eɪ|əʊ|aɪ|ɔɪ|aʊ|ɪə|eə|ʊə)
        (?<consonant>tʃ|dʒ|p|b|t|d|k|g|f|v|θ|ð|s|z|ʃ|ʒ|h|m|n|ŋ|l|r|j|w)
        (?<vowel>(?&diphthong)|(?&long_vowel)|(?&short_vowel))
        (?<phonetic>(?&vowel)|(?&consonant))
        (?<stress>ˈ)
    )
    (?&vowel)
    """
    formatted_pattern = re.sub(r"\s", "", pattern)
    return re.compile(formatted_pattern).findall(phonetic)


def render_diff_result(diff_result: list[str]) -> str:
    content = ""
    i = 0
    while i < len(diff_result):
        item = diff_result[i]

        diff_type = item[0]
        diff_value = item[2:]

        if diff_type == " ":
            content += diff_value
        elif diff_type == "-":
            if i + 1 < len(diff_result):
                next_item = diff_result[i + 1]
                next_type = next_item[0]
                next_value = next_item[2:]
                if next_type == "+":
                    content += f"<ruby>{diff_value}<rt>{next_value}</rt></ruby>"
                    i += 1
                else:
                    content += f"<del>{diff_value}</del>"
            else:
                content += f"<del>{diff_value}</del>"
        elif diff_type == "+":
            content += f"({diff_value})"
        else:
            content += f"({diff_value})"
        i += 1
    return content


PHONEME_MAPPING: dict[str, list[Any]] = {
    "a": ["eɪ", "e", "æ", "ʌ", "ɒ", "ɑː", "ɔː", "ɪ", "ə", ""],
    "e": ["iː", "e", "ɪ", "ə", "ɜː", ""],
    "i": ["aɪ", "iː", "ɪ", "ə", "i", ""],
    "o": ["əʊ", "ʌ", "ɒ", "ɑː", "ɔː", "uː", "ʊ", "ɪ", "ə", ""],
    "u": ["uː", ["j", "uː"], "ʌ", "ʊ", "ɪ", "ə", ""],
    "b": ["b", ""],
    "c": ["s", "k", "ʃ", "tʃ", ""],
    "d": ["d", "dʒ", "t", ""],
    "f": ["f", "v", ""],
    "g": ["g", "dʒ", "ʒ", "f", ""],
    "h": ["h", ""],
    "j": ["dʒ"],
    "k": ["k", ""],
    "l": ["l", ""],
    "m": ["m", ""],
    "n": ["n", ""],
    "p": ["p", "f", ""],
    "qu": ["kw"],
    "r": ["r", ""],
    "s": ["s", "z", "ʒ", "ʃ", ""],
    "t": ["t", "ʃ", "tʃ", "θ", "ð", ""],
    "v": ["v"],
    "w": ["w", ""],
    "x": ["ks", "gz", "kʃ"],
    "y": ["ɪ", "ə"],
    "z": ["z", "ʒ", ""],
}


def map_slow(word: str, phonetic: str):
    phonemes = get_phonemes(phonetic)
    formated_phonetic = "".join(phonemes)
    letters = get_letters(word)

    candidates = []

    for letter in letters:
        candidate_phonemes = PHONEME_MAPPING.get(letter, [])
        filter_phonemes = [p for p in candidate_phonemes if p in phonetic]
        candidates.append(filter_phonemes)

    mapping_result = []
    for guest_phonemes in itertools.product(*candidates):
        guest_phonetic = "".join(guest_phonemes)
        if guest_phonetic == formated_phonetic:
            mapping_result.append(list(zip(letters, guest_phonemes)))
    # import pdb; pdb.set_trace()
    return mapping_result[0]


def map_consonants(word: str, phonetic: str) -> list[list[tuple[str, str]]]:
    candidates = []
    phoneme_consonants = get_phoneme_consonants(phonetic)
    # print(phoneme_consonants)
    formated_phonetic = "".join(phoneme_consonants)
    letter_consonants = get_letter_consonants(word)
    # print(letter_consonants)
    for letter_consonant in letter_consonants:
        phonemes = PHONEME_MAPPING.get(letter_consonant, [])
        filter_phonemes = [p for p in phonemes if p in phonetic]
        candidates.append(filter_phonemes)

    # print(candidates)
    # print("FM", formated_phonetic)
    mapping_result = []
    for guest_phonemes in itertools.product(*candidates):
        guest_phonetic = "".join(guest_phonemes)
        print(guest_phonetic)
        if guest_phonetic == formated_phonetic:
            mapping_result.append(list(zip(letter_consonants, guest_phonemes)))
    return mapping_result


def map_vowels(word: str, phonetic: str) -> list[list[tuple[str, str]]]:
    candidates = []
    phoneme_vowels = get_phoneme_vowels(phonetic)
    formated_phonetic = "".join(phoneme_vowels)
    letter_vowels = get_letter_vowels(word)

    for letter_vowel in letter_vowels:
        phonemes = PHONEME_MAPPING.get(letter_vowel, [])
        filter_phonemes = [p for p in phonemes if p in phonetic]
        candidates.append(filter_phonemes)

    mapping_result = []
    for guest_phonemes in itertools.product(*candidates):
        guest_phonetic = "".join(guest_phonemes)
        if guest_phonetic == formated_phonetic:
            mapping_result.append(list(zip(letter_vowels, guest_phonemes)))
    return mapping_result


def find_letter(letter: str, mapping: list[tuple[str, str]]) -> int:
    for index, value in enumerate(mapping):
        mapped_letter, phoneme = value
        if letter == mapped_letter:
            return index
    return -1


def map_phonetic_2(word: str, phonetic: str) -> list[tuple[str, str]]:
    phonetic_map = map_slow(word, phonetic)
    map_result = []

    for letter in word:
        for index, letter in enumerate(phonetic_map):
            map_result.append(phonetic_map[index])
        else:
            map_result.append((letter, letter))
    return map_result


def map_phonetic(word: str, phonetic: str) -> Any:
    mapped_consonants: list[tuple[str, str]] = map_consonants(word, phonetic)[0]
    mapped_vowels = map_vowels(word, phonetic)[0]

    map_result = []

    for letter in word:
        letter_index = find_letter(letter, mapped_consonants)
        if letter_index >= 0:
            map_result.append(mapped_consonants[letter_index])
            mapped_consonants = (
                mapped_consonants[:letter_index] + mapped_consonants[letter_index + 1 :]
            )
        else:
            letter_index = find_letter(letter, mapped_vowels)
            if letter_index >= 0:
                map_result.append(mapped_vowels[letter_index])
                mapped_vowels = (
                    mapped_vowels[:letter_index] + mapped_vowels[letter_index + 1 :]
                )
            else:
                map_result.append((letter, letter))
    return map_result


def render_mapping_result(mapping_result: list[tuple[str, str]]) -> str:
    content = ""
    for letter, phoneme in mapping_result:
        if letter == phoneme:
            content += letter
        elif phoneme == "":
            content += f"<del>{letter}</del>"
        else:
            content += f"<ruby>{letter}<rt>{phoneme}</rt></ruby>"
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
  </head>
  <body>
    <h1>{content}</h1>
  </body>
</html>
"""


def main() -> None:
    item = "cal"
    for word in RegexDict(regex="cal$").find():
        # word = "ducal"
        try:
            ld_dictionary = LongManWord(word)
            hyphenation = ld_dictionary.hyphenation()
            dictionary = OxfordLearnerDictionary(word)
            phonetic = dictionary.phonetic_br()
            if hyphenation and phonetic:
                parts = hyphenation.split("‧")
                if item in parts:
                    mapping_result = map_phonetic_2(
                        hyphenation.lower(), phonetic.lower()
                    )
                    # mapping_result & hyphenation
                    fid = hyphenation.find(item)
                    if fid:
                        cut_result = mapping_result[fid : fid + len(item)]
                        print(hyphenation, "".join([v for i, v in cut_result]))
                    else:
                        print(hyphenation, None)
                else:
                    print(hyphenation, None)
            else:
                print(word, None)
        except Exception as e:
            print(word, e, file=sys.stderr)
            raise e

    # word = "exclamation"
    # dictionary = OxfordLearnerDictionary(word)
    # phonetic = dictionary.phonetic_br()
    #
    # ld_dictionary = LongManWord(word)
    # hyphenation = ld_dictionary.hyphenation()
    # hyph_or_word = hyphenation if hyphenation else word
    # mapping_result = map_phonetic(hyph_or_word.lower(), phonetic.lower())
    # html = render_mapping_result(mapping_result)
    # Path("output.html").write_text(html)


if __name__ == "__main__":
    main()


# Vấn đề của mapping phụ âm trước rồi nguyên âm sau.
