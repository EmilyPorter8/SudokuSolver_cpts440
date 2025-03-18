#Inputs a CNF file containing the solution to the sudoku problem. Outputs it as a grid.
#As of right now, is set to a 9x9 for base case
def parse_miniSat_output(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    
    if lines[0].strip() != "SAT":
        return None #No solution present
    
    assignments = map(int, lines[1].split())
    grid = [[0]*9 for _ in range(9)]
    
    for var in assignments:
        if var > 0:
            x = var - 1
            r = x // 81 + 1
            c = (x % 81) // 9 + 1
            v = (x % 9) + 1
            grid[r - 1][c - 1] = v
            
    return grid

def print_sudoku(grid):
    for row in grid:
        print( " ".join(map(str, row)))
         
#Test Case:
sudoku_solution = parse_miniSat_output(r"SAT_IO\sudoku.out")
if sudoku_solution:
    print_sudoku(sudoku_solution)
else:
    print("No solution found.")