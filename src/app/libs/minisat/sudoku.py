import itertools

from sympy import symbols, satisfiable
from sympy import Or, And, Not
from sympy.logic.boolalg import to_cnf

from app.libs.minisat import NumberSymbol


def select(elements: list, number: int):
    clauses = []
    for items in itertools.combinations(elements, len(elements) - number + 1):
        clauses.append(Or(*items))

    for items in itertools.combinations(elements, number + 1):
        clauses.append(Or(*[Not(item) for item in items]))
    return And(*clauses)


def solve_sudoku_sympy2(board):
    def P(r, c, v):
        np, np_expr = NumberSymbol.allocate(f"P_{r}_{c}", 3)

        return symbols(f"P_{r}_{c}_{v}")

    clauses = []

    for r in range(9):
        for c in range(9):
            clauses.append(select([P(r, c, v) for v in range(1, 10)], 1))

    for r in range(9):
        for v in range(1, 10):
            variables = []
            for c in range(9):
                variables.append(P(r, c, v))
            clauses.append(select(variables, 1))

    for c in range(9):
        for v in range(1, 10):
            variables = []
            for r in range(9):
                variables.append(P(r, c, v))
            clauses.append(select(variables, 1))

    for br in range(3):
        for bc in range(3):
            cells = [(br * 3 + r, bc * 3 + c) for r in range(3) for c in range(3)]

            for r, c in cells:
                variables = []
                for v in range(1, 10):
                    variables.append(P(r, c, v))
                clauses.append(select(variables, 1))

    for r in range(9):
        for c in range(9):
            if board[r][c] != 0:
                clauses.append(P(r, c, board[r][c]))

    expr = And(*clauses)
    cnf_expr = to_cnf(expr)
    solution = satisfiable(cnf_expr)
    if not solution:
        return None

    result = [[0] * 9 for _ in range(9)]
    for r in range(9):
        for c in range(9):
            for v in range(1, 10):
                if solution.get(P(r, c, v)):
                    result[r][c] = v
                    break
    return result


def solve_sudoku_sympy(board):
    def P(r, c, v):
        return symbols(f"P_{r}_{c}_{v}")

    clauses = []

    for r in range(9):
        for c in range(9):
            clauses.append(select([P(r, c, v) for v in range(1, 10)], 1))

    for r in range(9):
        for v in range(1, 10):
            variables = []
            for c in range(9):
                variables.append(P(r, c, v))
            clauses.append(select(variables, 1))

    for c in range(9):
        for v in range(1, 10):
            variables = []
            for r in range(9):
                variables.append(P(r, c, v))
            clauses.append(select(variables, 1))

    for br in range(3):
        for bc in range(3):
            cells = [(br * 3 + r, bc * 3 + c) for r in range(3) for c in range(3)]

            for r, c in cells:
                variables = []
                for v in range(1, 10):
                    variables.append(P(r, c, v))
                clauses.append(select(variables, 1))

    for r in range(9):
        for c in range(9):
            if board[r][c] != 0:
                clauses.append(P(r, c, board[r][c]))

    expr = And(*clauses)
    cnf_expr = to_cnf(expr)
    solution = satisfiable(cnf_expr)
    if not solution:
        return None

    result = [[0] * 9 for _ in range(9)]
    for r in range(9):
        for c in range(9):
            for v in range(1, 10):
                if solution.get(P(r, c, v)):
                    result[r][c] = v
                    break
    return result


def main():
    # Ma trận lấy trực tiếp từ màn hình của bạn
    grid = [
        [5, 0, 0, 0, 0, 0, 0, 0, 0],
        [3, 0, 2, 0, 4, 6, 0, 8, 0],
        [0, 0, 1, 5, 0, 7, 2, 0, 0],
        [0, 0, 0, 7, 0, 0, 8, 0, 0],
        [9, 4, 0, 3, 0, 2, 0, 1, 5],
        [0, 0, 3, 0, 0, 4, 0, 0, 0],
        [0, 0, 5, 6, 0, 9, 4, 0, 0],
        [0, 1, 0, 4, 5, 0, 3, 0, 2],
        [0, 0, 0, 0, 0, 0, 0, 9, 0],
    ]

    solution = solve_sudoku_sympy(grid)

    if solution:
        for row in solution:
            print(row)
    else:
        print("Không tìm thấy lời giải.")


if __name__ == "__main__":
    main()
