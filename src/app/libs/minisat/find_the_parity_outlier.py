from dataclasses import dataclass

from sympy import And, Or, Symbol, satisfiable
from sympy.logic.boolalg import to_cnf

from app.libs.minisat import select


def find_outlier(integers):
    @dataclass
    class Item:
        index: int
        value: int
        symbol: Symbol

    items: list[Item] = []

    for i, v in enumerate(integers):
        item = Item(index=i, value=v, symbol=Symbol(f"sym-{i}"))
        items.append(item)

    even_numbers = []
    odd_numbers = []

    for item in items:
        if item.value % 2 == 0:
            even_numbers.append(item.symbol)
        else:
            odd_numbers.append(item.symbol)

    clauses = And(
        Or(select(even_numbers, len(even_numbers)), select(even_numbers, 0)),
        Or(select(odd_numbers, len(odd_numbers)), select(odd_numbers, 0)),
        Or(select(even_numbers, 1), select(odd_numbers, 1)),
    )
    cnf_expr = to_cnf(clauses)
    solution = satisfiable(cnf_expr)

    if not solution:
        return None

    for item in items:
        if solution.get(item.symbol):
            return item.value
    return None


def main():
    print(find_outlier([2, 4, 0, 100, 4, 11, 2602, 36]))
    print(find_outlier([160, 3, 1719, 19, 11, 13, -21]))


if __name__ == "__main__":
    main()
