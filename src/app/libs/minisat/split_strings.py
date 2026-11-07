import re


def solution(s):
    if len(s) % 2 == 1:
        s += "_"
    result = []
    for i in range(0, len(s), 2):
        result.append(s[i : i + 2])
    return result


def reverse_words(text):
    return " ".join([s[::-1] for s in text.split(" ")])


def alphabet_position(text):
    result = []
    for letter in re.compile(r"[A-Za-z]").findall(text):
        result.append(str(ord(letter.lower()) - 96))
    return " ".join(result)
