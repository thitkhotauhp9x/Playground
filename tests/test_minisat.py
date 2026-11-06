import pytest
from sympy import And, Not, Or, satisfiable, symbols, to_cnf

from app.libs.minisat import NumberSymbol, allocate, auto_n, equal, read_number, select


def test_number() -> None:
    with pytest.raises(ValueError):
        equal([], 2)

    expr1 = equal([symbols("1"), symbols("2")], 2)
    assert expr1 == And(symbols("1"), Not(symbols("2")))

    expr2 = equal([symbols("1"), symbols("2"), symbols("3"), symbols("4")], 2)
    assert expr2 == And(Not(symbols("1")), Not(symbols("2")), symbols("3"), Not(symbols("4")))


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
