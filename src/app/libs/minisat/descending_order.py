import itertools
from dataclasses import dataclass
from typing import Any

from sympy import And, Not, Symbol, satisfiable, to_cnf

from app.libs.minisat import group_by, select


@dataclass
class DescendingOrderItem:
    input_index: int
    target_index: int
    value: Any
    symbol: Symbol


class DescendingOrder:
    @staticmethod
    def create_symbols(text: str) -> list[DescendingOrderItem]:
        items: list[DescendingOrderItem] = []
        for i, v in enumerate(text):
            for j in range(0, len(text), 1):
                items.append(
                    DescendingOrderItem(
                        input_index=i, value=v, symbol=Symbol(f"sym{i}-{j}"), target_index=j
                    )
                )
        return items

    @staticmethod
    def create_rules(items: list[DescendingOrderItem]):
        clauses = []
        for _, group in group_by(items, key=lambda x: x.input_index):
            expr = select([i.symbol for i in group], 1)
            clauses.append(expr)

        for _, group in group_by(items, key=lambda x: x.target_index):
            expr = select([i.symbol for i in group], 1)
            clauses.append(expr)

        for f, s in itertools.combinations(items, 2):
            if int(f.value) > int(s.value):
                if f.target_index > s.target_index:
                    expr = Not(And(f.symbol, s.symbol))
                    clauses.append(expr)
                else:
                    pass
            else:
                if s.target_index > f.target_index:
                    expr = Not(And(f.symbol, s.symbol))
                    clauses.append(expr)
                else:
                    pass

        expr = And(*clauses)
        return expr

    @classmethod
    def satisfy(cls, text: str):
        items = cls.create_symbols(text)
        expr = cls.create_rules(items)
        cnf_expr = to_cnf(expr)
        solution = satisfiable(cnf_expr)

        if not solution:
            return None

        result = []
        for item in items:
            if solution.get(item.symbol):
                result.append((item.target_index, item.value))
        return result


def main():
    result = DescendingOrder.satisfy("145263")
    print(result)


if __name__ == "__main__":
    main()
