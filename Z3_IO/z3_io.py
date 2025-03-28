from CNF import generate_sudoku_cnf, var

# Turning sudoku grid into a CNF format:
def sudoku_to_cnf(grid, n):
    """Converts a given Sudoku grid into CNF format, including prefilled values.

    Args:
        grid (list of lists): Sudoku Grid.
        n (int, optional): Size of the grid. Defaults to 100.

    Returns:
        list: CNF representation of the Sudoku puzzle.
    """
    print("[INFO] Generating base CNF constraints...")
    cnf = generate_sudoku_cnf(n)
    
    print("[INFO] Adding prefilled values to CNF...")
    prefilled_count = 0
    for i in range(n):
        for j in range(n):
            if grid[i][j] != 0:
                k = grid[i][j] - 1  # Converts to a zero-based index
                cnf.append([var(i, j, k, n)])  # Enforces value in the CNF
                prefilled_count += 1
        if i % 10 == 0:
            print(f"[DEBUG] Processed {i}/{n} rows for prefilled values...")

    print(f"[SUCCESS] Added {prefilled_count} prefilled values to CNF.")
    return cnf

# Turning CNF Solution into a grid:
def cnf_to_sudoku(assignment, n):
    """Converts the completed CNF solution into a Sudoku grid.

    Args:
        assignment (dict): CNF solution.
        n (int, optional): Grid size. Defaults to 100.

    Returns:
        list of lists: Sudoku grid.
    """
    print("[INFO] Converting CNF assignment to Sudoku grid...")
    grid = [[0] * n for _ in range(n)]
    
    true_count = 0
    for var_str, val in assignment.items():
        if val:  # If variable is true in the model
            var_num = int(var_str[1:])  # Extract index
            x = var_num - 1
            r = x // (n * n)
            c = (x % (n * n)) // n
            v = (x % n) + 1
            grid[r][c] = v
            true_count += 1
        if true_count % 1000 == 0 and true_count > 0:
            print(f"[DEBUG] Processed {true_count} variables in CNF solution...")

    print(f"[SUCCESS] Sudoku grid reconstruction complete with {true_count} values assigned.")
    return grid
