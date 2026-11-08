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


def int_to_binary(number: int, length: int) -> list[bool]:
    if number == 0:
        return [False]

    remainder_list: list[bool] = []
    temp = number

    while temp > 0:
        remainder = temp % 2
        remainder_list.append(bool(remainder))
        temp = temp // 2

    if length >= len(remainder_list):
        for _ in range(len(remainder_list), length):
            remainder_list.append(False)
    else:
        raise ValueError(f"length must be >= {len(remainder_list)}")

    remainder_list.reverse()

    return remainder_list
