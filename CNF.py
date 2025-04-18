import itertools

def var(i, j, k, n=9):
    """
    Map (row i, column j, number k) to a unique SAT variable number (starting from 1).
    i, j, k are 0-based (0 to 8).
    """
    return i * n * n + j * n + k + 1

def generate_sudoku_cnf(n=9):
    clauses = []

    # Each cell must have at least one number
    for i in range(n):
        for j in range(n):
            clauses.append([var(i, j, k, n) for k in range(n)])

    # Each cell must have at most one number (no two numbers in one cell)
    for i in range(n):
        for j in range(n):
            for k1, k2 in itertools.combinations(range(n), 2):
                clauses.append([-var(i, j, k1, n), -var(i, j, k2, n)])

    # Each number must appear exactly once in each row
    for i in range(n):
        for k in range(n):
            clauses.append([var(i, j, k, n) for j in range(n)])
            for j1, j2 in itertools.combinations(range(n), 2):
                clauses.append([-var(i, j1, k, n), -var(i, j2, k, n)])

    # Each number must appear exactly once in each column
    for j in range(n):
        for k in range(n):
            clauses.append([var(i, j, k, n) for i in range(n)])
            for i1, i2 in itertools.combinations(range(n), 2):
                clauses.append([-var(i1, j, k, n), -var(i2, j, k, n)])

    # Each number must appear exactly once in each 3x3 subgrid
    block_size = int(n ** 0.5)
    assert block_size * block_size == n, "n must be a perfect square (like 9)."

    for k in range(n):
        for block_row in range(0, n, block_size):
            for block_col in range(0, n, block_size):
                cells = []
                for i in range(block_size):
                    for j in range(block_size):
                        cells.append(var(block_row + i, block_col + j, k, n))
                clauses.append(cells)  # at least once in subgrid
                for c1, c2 in itertools.combinations(cells, 2):
                    clauses.append([-c1, -c2])  # at most once in subgrid

    return clauses

def save_cnf(clauses, filename="sudoku_9x9.cnf", n=9):
    num_vars = n * n * n
    with open(filename, "w") as f:
        f.write(f"p cnf {num_vars} {len(clauses)}\n")
        for clause in clauses:
            f.write(" ".join(map(str, clause)) + " 0\n")

if __name__ == "__main__":
    cnf_clauses = generate_sudoku_cnf(n=9)
    save_cnf(cnf_clauses, filename="sudoku_9x9.cnf", n=9)
    print(" CNF file generated: sudoku_9x9.cnf")
