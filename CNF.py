import itertools

#changed this from 100 to 9
def var(i, j, k, n=9):
    """ Returns a unique variable number for a given (row, column, number). """
    return i * n * n + j * n + k + 1

# changed this from 100 to 9
def generate_sudoku_cnf(n=9):
    """ Generate CNF constraints for a 100x100 Sudoku puzzle. """
    clauses = []

    # Each cell contains at least one number (1 to n)
    for i in range(n):
        for j in range(n):
            clauses.append([var(i, j, k, n) for k in range(n)])

    # Each number appears at most once per row
    for i in range(n):
        for k in range(n):
            for j1, j2 in itertools.combinations(range(n), 2):
                clauses.append([-var(i, j1, k, n), -var(i, j2, k, n)])

    # Each number appears at most once per column
    for j in range(n):
        for k in range(n):
            for i1, i2 in itertools.combinations(range(n), 2):
                clauses.append([-var(i1, j, k, n), -var(i2, j, k, n)])

    return clauses

def save_cnf(clauses, filename="sudoku_9x9.cnf"):
    """ Save CNF formula to a DIMACS format file. """
    with open(filename, "w") as f:
        #f.write(f"p cnf {100*100*100} {len(clauses)}\n")
        f.write(f"p cnf {9*9*9} {len(clauses)}\n")
        for clause in clauses:
            f.write(" ".join(map(str, clause)) + " 0\n")

# Generate CNF for 100x100 Sudoku
cnf_clauses = generate_sudoku_cnf()
save_cnf(cnf_clauses)

print("CNF file generated: sudoku_nxn.cnf")
