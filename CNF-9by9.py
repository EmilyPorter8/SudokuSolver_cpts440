import itertools


def var(i, j, k, n=9):
    """ Returns a unique variable number for a given (row, column, number). """
    return i * n * n + j * n + k + 1


def generate_sudoku_cnf(n=9):
    clauses = []

    # Each cell contains at least one number
    for i in range(n):
        for j in range(n):
            clauses.append([var(i, j, k, n) for k in range(n)])

    # Each cell contains at most one number
    for i in range(n):
        for j in range(n):
            for k1, k2 in itertools.combinations(range(n), 2):
                clauses.append([-var(i, j, k1, n), -var(i, j, k2, n)])

    # Each number appears exactly once per row
    for i in range(n):
        for k in range(n):
            clauses.append([var(i, j, k, n) for j in range(n)])
            for j1, j2 in itertools.combinations(range(n), 2):
                clauses.append([-var(i, j1, k, n), -var(i, j2, k, n)])

    # Each number appears exactly once per column
    for j in range(n):
        for k in range(n):
            clauses.append([var(i, j, k, n) for i in range(n)])
            for i1, i2 in itertools.combinations(range(n), 2):
                clauses.append([-var(i1, j, k, n), -var(i2, j, k, n)])

    return clauses


def save_cnf(clauses, filename="sudoku_9x9_no_subgrid.cnf", n=9):
    num_vars = n * n * n  # total variables
    with open(filename, "w") as f:
        f.write(f"p cnf {num_vars} {len(clauses)}\n")
        for clause in clauses:
            f.write(" ".join(map(str, clause)) + " 0\n")


if __name__ == "__main__":
    cnf_clauses = generate_sudoku_cnf(n=9)
    save_cnf(cnf_clauses, filename="sudoku_9x9_no_subgrid.cnf", n=9)

