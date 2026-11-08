from collections import UserList
from functools import singledispatch

from sympy import And, Equivalent, Not, Or, Symbol, Xor, numbered_symbols
from sympy.logic.boolalg import Boolean

from app.libs.minisat import int_to_bin
from app.libs.minisat.numbered_symbol_container import NumberedSymbolContainer

NUMBER_RESULT_MAPPING: dict[bool, str] = {
    True: "1",
    False: "0",
}


class Number(UserList[Symbol]):
    @classmethod
    def create(cls, prefix: str, buffer_size: int) -> "Number":
        ns = numbered_symbols(prefix)
        vs = []
        for _ in range(0, buffer_size, 1):
            vs.append(next(ns))

        return cls(*vs)

    def get_value(self, solution) -> int:
        code = ""
        for variable in self.data:
            result = solution.get(variable)
            code += NUMBER_RESULT_MAPPING[result]

        return int(code, 2)


def add(first: Number, second: Number, result: Number) -> Boolean:
    if len(first) != len(second) != len(result):
        raise ValueError("Arrays must have the same length")

    container = NumberedSymbolContainer()
    memory = [next(container.numbered_symbol_singleton()) for _ in range(len(first))]

    ra = first[::-1]
    rb = second[::-1]
    rc = memory[::-1]
    rs = result[::-1]

    expr = Equivalent(rs[0], Or(ra[0], rb[0]))

    expr = And(expr, Equivalent(rc[0], ra[0] & rb[0]))

    for i, (ra_i, rb_i, _) in enumerate(zip(ra[1:], rb[1:], rs[1:])):
        expr = And(expr, Equivalent(rs[i], Xor(ra_i, rb_i, rc[i - 1])))
        expr = And(expr, Equivalent(rc[i], Or(And(ra_i, rb_i), And(rc[i - 1], Or(ra_i, rb_i)))))

    return expr


@singledispatch
def equal(_first, _second) -> Boolean:
    raise NotImplementedError("Not implemented")


@equal.register
def _(first: Number, second: Number) -> Boolean:
    clauses = []
    for i, j in zip(first.data, second.data, strict=True):
        clauses.append(Equivalent(i, j))
    return And(*clauses)


@equal.register
def _(first: Number, second: list[bool]) -> Boolean:
    clauses = []
    for element, binary in zip(first.data, second):
        if binary:
            clauses.append(element)
        else:
            clauses.append(Not(element))
    return And(*clauses)


@equal.register
def _(first: Number, number: int) -> Boolean:
    return equal(first, int_to_bin(number, len(first)))


@singledispatch
def less_than(_first, _second) -> Boolean:
    raise NotImplementedError("Not implemented")


@less_than.register
def _(first: Number, second: int) -> Boolean:
    expr = []

    for _ in range(second, 2 ** len(first.data), 1):
        expr.append(Not(equal(first, second)))
    return Or(*expr)
