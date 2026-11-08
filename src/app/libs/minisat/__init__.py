import itertools

from sympy import And, Not, Or


def select(elements: list, number: int):
    clauses = []
    for items in itertools.combinations(elements, len(elements) - number + 1):
        clauses.append(Or(*items))

    for items in itertools.combinations(elements, number + 1):
        clauses.append(Or(*[Not(item) for item in items]))
    return And(*clauses)


def group_by(items, key):
    return itertools.groupby(sorted(items, key=key), key=key)


def int_to_binary(number: int) -> list[bool]:
    if number == 0:
        return [False]

    remainder_list: list[bool] = []
    temp = number

    while temp > 0:
        remainder = temp % 2
        remainder_list.append(bool(remainder))
        temp = temp // 2

    remainder_list.reverse()
    return remainder_list


def int_to_bin(value: int, length: int) -> list[bool]:
    bool_mapping = {
        "0": False,
        "1": True,
    }

    result: list[bool] = []
    for code in f"{value:0{length}b}":
        result.append(bool_mapping[code])
    return result
