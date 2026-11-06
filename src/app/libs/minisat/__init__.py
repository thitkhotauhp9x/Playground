import itertools
import math
from collections import UserList
from typing import Any

from sympy import And, Equivalent, Not, Or, numbered_symbols
from sympy.logic.boolalg import Boolean


def select(elements: list, number: int):
    clauses = []
    for items in itertools.combinations(elements, len(elements) - number + 1):
        clauses.append(Or(*items))

    for items in itertools.combinations(elements, number + 1):
        clauses.append(Or(*[Not(item) for item in items]))
    return And(*clauses)


class NumberSymbol(UserList[Boolean]):
    def eq(self, other: Any) -> Any:
        if isinstance(other, NumberSymbol):
            clauses = []
            for i, j in zip(self.data, other.data, strict=True):
                clauses.append(Equivalent(i, j))
            return And(*clauses)
        if isinstance(other, int):
            string_code = f"{other:0{len(self.data)}b}"
            clauses = []
            for element, binary in zip(self.data, string_code, strict=True):
                if binary == "1":
                    clauses.append(element)
                elif binary == "0":
                    clauses.append(Not(element))
                else:
                    raise ValueError("Should be 0 or 1")

            return And(*clauses)
        raise ValueError("Does not supported")

    def read_solution(self, solution) -> int:
        result_mapping: dict[bool, str] = {
            True: "1",
            False: "0",
        }
        code = ""

        for variable in self.data:
            result = solution.get(variable)
            code += result_mapping[result]

        return int(code, 2)

    def lt(self, n: int):
        expr = []

        for number in range(n, 2 ** len(self.data), 1):
            expr.append(Not(equal(self.data, number)))

        return Or(*expr)

    def add(self, result: "NumberSymbol", number: int):
        """
        Result = Self + number
        :param result:
        :param number:
        :return:
        """

    @classmethod
    def create(cls, prefix: str, buffer_size: int) -> "NumberSymbol":
        ns = numbered_symbols(prefix)
        vs = []
        for _ in range(0, buffer_size, 1):
            vs.append(next(ns))
        return cls(*vs)


def auto_n(n: int, size: int, prefix: str):
    ns = NumberSymbol.create(prefix, size)
    return ns.eq(n), ns.data


def equal(variables, number: int):
    ns = NumberSymbol(variables)
    return ns.eq(number)


def allocate(prefix: str, size: int):
    bit_num = math.ceil(math.log2(size))
    ns = NumberSymbol.create(prefix, bit_num)
    return ns.data, ns.lt(size)


def read_number(solution, variables):
    ns = NumberSymbol(variables)
    return ns.read_solution(solution)


def group_by(items, key):
    return itertools.groupby(sorted(items, key=key), key=key)
