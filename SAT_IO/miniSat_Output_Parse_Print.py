#Inputs a CNF file containing the solution to the sudoku problem. Outputs it as a grid.
#As of right now, is set to a 9x9 for base case
def parse_miniSat_output(filename, n=100):
    with open(filename, "r") as f:
        lines = f.readlines()
    
    if lines[0].strip() != "SAT":
        return None #No solution present
    
    assignments = map(int, lines[1].split())
    grid = [[0]*n for _ in range(n)]
    
    for var in assignments:
        if var > 0:
            x = var - 1
            r = x // (n*n) + 1
            c = (x % (n*n)) // n + 1
            v = (x % n) + 1
            grid[r - 1][c - 1] = v
            
    return grid

def print_sudoku(grid):
    for row in grid:
        print( " ".join(map(str, row)))
         
#Test Case:
sudoku_solution = parse_miniSat_output(r"SAT_IO\sudoku.out", n=100)
if sudoku_solution:
    print_sudoku(sudoku_solution)
else:
    print("No solution found.")