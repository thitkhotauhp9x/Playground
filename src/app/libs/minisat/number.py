from collections import UserList
from typing import Any

from sympy import Equivalent, Symbol, And, Not, Or, numbered_symbols, Xor


class Number(UserList[Symbol]):
    def eq(self, other: Any) -> Any:
        if isinstance(other, Number):
            clauses = []
            for i, j in zip(self.data, other.data, strict=True):
                clauses.append(Equivalent(i, j))
            return And(*clauses)
        elif isinstance(other, int):
            clauses = []
            for element, binary in zip(
                self.data, self.int_to_bin(other, len(self.data))
            ):
                if binary:
                    clauses.append(element)
                else:
                    clauses.append(Not(element))
            return And(*clauses)
        else:
            raise ValueError("Does not supported")

    @property
    def name(self) -> str:
        code = [i.name for i in self.data]
        return f"Number({code})"

    @staticmethod
    def int_to_bin(value: int, length: int) -> list[bool]:
        bool_mapping = {
            "0": False,
            "1": True,
        }

        result: list[bool] = []
        for code in f"{value:0{length}b}":
            result.append(bool_mapping[code])
        return result

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
            expr.append(Not(self.eq(number)))

        return Or(*expr)

    @staticmethod
    def r_add(
        a: list[Symbol], b: list[Symbol | bool], c: list[Symbol], s: list[Symbol]
    ):
        expr = Equivalent(s[0], Or(a[0], b[0]))

        expr = And(expr, Equivalent(c[0], a[0] & b[0]))

        for i, (a_i, b_i, s_i) in enumerate(zip(a[1:], b[1:], s[1:])):
            expr = And(expr, Equivalent(s[i], Xor(a_i, b_i, c[i - 1])))
            expr = And(
                expr, Equivalent(c[i], Or(And(a_i, b_i), And(c[i - 1], Or(a_i, b_i))))
            )

        return expr

    @staticmethod
    def add(a: list[Symbol], b: list[Symbol | bool], c: list[Symbol], s: list[Symbol]):
        return Number.r_add(a[::-1], b[::-1], c[::-1], s[::-1])

    @staticmethod
    def st_name(a: list[Symbol]) -> str:
        return "_".join([i.name for i in a])

    @staticmethod
    def add_number(a: list[Symbol], b: int, s: list[Symbol]):
        assert len(a) == len(s)

        sized = len(a)

        auto_gen_symbols = numbered_symbols(
            f"C({Number.st_name(a)}+{b}={Number.st_name(s)})"
        )

        return Number.add(
            a,
            Number.int_to_bin(b, sized),
            [next(auto_gen_symbols) for _ in range(sized)],
            s,
        )

    def ad(self, b: int, s: "Number"):
        return Number.add_number(self.data, b, s.data)

    @classmethod
    def create(cls, prefix: str, buffer_size: int) -> "Number":
        ns = numbered_symbols(prefix)
        vs = []
        for i in range(0, buffer_size, 1):
            vs.append(next(ns))
        return cls(*vs)
