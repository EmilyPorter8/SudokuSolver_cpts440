import itertools
from z3 import Solver, Bool, Or, And, Not, sat

# Define n=9
n = 9

# Create variable for (row, col, num)
def var(i, j, k):
    return Bool(f"cell_{i}_{j}_{k}")

# Generate Z3 variables
variables = [[[var(i, j, k) for k in range(n)] for j in range(n)] for i in range(n)]

solver = Solver()

# Each cell must have exactly one number
for i in range(n):
    for j in range(n):
        solver.add(Or([variables[i][j][k] for k in range(n)]))  # At least one number
        for k1, k2 in itertools.combinations(range(n), 2):
            solver.add(Or(Not(variables[i][j][k1]), Not(variables[i][j][k2])))  # At most one

# Each number appears exactly once per row
for i in range(n):
    for k in range(n):
        solver.add(Or([variables[i][j][k] for j in range(n)]))  # At least once in row
        for j1, j2 in itertools.combinations(range(n), 2):
            solver.add(Or(Not(variables[i][j1][k]), Not(variables[i][j2][k])))  # At most once

# Each number appears exactly once per column
for j in range(n):
    for k in range(n):
        solver.add(Or([variables[i][j][k] for i in range(n)]))  # At least once in column
        for i1, i2 in itertools.combinations(range(n), 2):
            solver.add(Or(Not(variables[i1][j][k]), Not(variables[i2][j][k])))  # At most once

# Each number appears exactly once per 3x3 subgrid
block_size = 3
for k in range(n):
    for block_row in range(block_size):
        for block_col in range(block_size):
            cells = []
            for i in range(block_size):
                for j in range(block_size):
                    cells.append(variables[block_row * block_size + i][block_col * block_size + j][k])
            solver.add(Or(cells))  # At least once in block
            for c1, c2 in itertools.combinations(cells, 2):
                solver.add(Or(Not(c1), Not(c2)))  # At most once

# Now solve!
if solver.check() == sat:
    model = solver.model()
    board = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if model.evaluate(variables[i][j][k]):
                    board[i][j] = k + 1  # k=0 means number 1, etc.

    # Print the board
    for row in board:
        print(" ".join(str(num) for num in row))
else:
    print("No solution found.")
