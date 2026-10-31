from collections import UserList

import math
from typing import Any

import pytest
from sympy import Or, And, Not, symbols, to_cnf, satisfiable, Equivalent
import itertools
from sympy import numbered_symbols
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
        elif isinstance(other, int):
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
        else:
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
        pass

    @classmethod
    def create(cls, prefix: str, buffer_size: int) -> "NumberSymbol":
        ns = numbered_symbols(prefix)
        vs = []
        for i in range(0, buffer_size, 1):
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


def test_number() -> None:
    with pytest.raises(ValueError):
        equal([], 2)

    expr1 = equal([symbols("1"), symbols("2")], 2)
    assert expr1 == And(symbols("1"), Not(symbols("2")))

    expr2 = equal([symbols("1"), symbols("2"), symbols("3"), symbols("4")], 2)
    assert expr2 == And(
        Not(symbols("1")), Not(symbols("2")), symbols("3"), Not(symbols("4"))
    )


def test_auto_n():
    a = auto_n(0, 2, "a")
    b = auto_n(1, 2, "a")
    c = auto_n(2, 2, "a")
    d = auto_n(3, 2, "a")
    expr = select([a[0], b[0], c[0], d[0]], 1)
    cnf_expr = to_cnf(expr)
    solution = satisfiable(cnf_expr)

    if not solution:
        print(read_number(solution, a[1]))
        print(read_number(solution, b[1]))
        print(read_number(solution, c[1]))
        print(read_number(solution, d[1]))


def test_allocate():
    A, B = symbols("A B")
    And(Or(A, Not(A)), Or(B, Not(B)))

    a, a_expr = allocate("a", 4)
    print(a, a_expr)


def test_sv():
    a, a_expr = allocate("a", 4)
    b, b_expr = allocate("b", 4)
    c, c_expr = allocate("c", 4)
    d, d_expr = allocate("d", 4)

    a_ = NumberSymbol(a)
    b_ = NumberSymbol(b)
    c_ = NumberSymbol(c)
    d_ = NumberSymbol(d)

    expr = And(
        select(
            [
                a_.eq(0),
                b_.eq(0),
                c_.eq(0),
                d_.eq(0),
            ],
            1,
        ),
        select(
            [
                a_.eq(1),
                b_.eq(1),
                c_.eq(1),
                d_.eq(1),
            ],
            1,
        ),
        select(
            [
                a_.eq(2),
                b_.eq(2),
                c_.eq(2),
                d_.eq(2),
            ],
            1,
        ),
        select(
            [
                a_.eq(3),
                b_.eq(3),
                c_.eq(3),
                d_.eq(3),
            ],
            1,
        ),
    )

    cnf_expr = to_cnf(expr)
    print(cnf_expr)
    solution = satisfiable(cnf_expr)
    if solution:
        print("a", read_number(solution, a))
        print("b", read_number(solution, b))
        print("c", read_number(solution, c))
        print("d", read_number(solution, d))
    else:
        print("No solution")
