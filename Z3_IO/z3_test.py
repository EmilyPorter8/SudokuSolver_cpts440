import unittest
from z3_io import sudoku_to_cnf, cnf_to_sudoku
from z3solver import solve_cnf


def solve_sudoku(grid, n=9):  # Use 9 for a 9x9 grid
    """ Solves a given Sudoku puzzle using Z3. """
    cnf = sudoku_to_cnf(grid, n)
    solution = solve_cnf(cnf)
    
    if solution:
        return cnf_to_sudoku(solution, n)
    else:
        return None

def print_sudoku(grid):
    for row in grid:
        print(" ".join(map(str, row)))

class TestSudokuSolver(unittest.TestCase):
    
    def test_solve_sudoku(self):
        # 3x3 Sudoku example (9x9 grid)
        grid = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]

        # Solve the Sudoku
        solution = solve_sudoku(grid, n=9)

        # Ensure a solution was found
        self.assertIsNotNone(solution, "Sudoku solver should return a solution")

        # Print the solution
        print("\nSolved Sudoku Grid:")
        print_sudoku(solution)

if __name__ == "__main__":
    unittest.main()