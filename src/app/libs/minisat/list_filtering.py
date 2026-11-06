from dataclasses import dataclass
from typing import Any

from sympy import And, Not, Symbol, satisfiable, to_cnf


@dataclass
class ListFilteringItem:
    value: Any
    index: int
    symbol: Symbol


class ListFiltering:
    @staticmethod
    def create_symbols(data: list[Any]) -> list[ListFilteringItem]:
        items = []

        for index, item in enumerate(data):
            items.append(ListFilteringItem(index=index, value=item, symbol=Symbol(f"sym{index}")))
        return items

    @staticmethod
    def create_filtering_expr(items: list[ListFilteringItem]):
        clauses = []
        for item in items:
            if isinstance(item.value, int):
                clauses.append(item.symbol)
            else:
                clauses.append(Not(item.symbol))
        return And(*clauses)

    @classmethod
    def solve(cls, data: list[Any]):
        items = cls.create_symbols(data)
        expr = cls.create_filtering_expr(items)
        cnf_expr = to_cnf(expr)
        solution = satisfiable(cnf_expr)

        if not solution:
            return None

        result = []
        for item in items:
            if solution.get(item.symbol):
                result.append(item.value)

        return result


def main():
    result = ListFiltering.solve([1, 2, "a", "b"])
    assert result == [1, 2]


if __name__ == "__main__":
    main()
