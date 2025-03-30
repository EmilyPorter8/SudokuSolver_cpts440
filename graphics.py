import plotly.figure_factory as ff
import SudokuSolver_cpts440.Sudoku_Generator as Sudoku_Generator 


fig = ff.create_table(data, colorscale='Blues')
fig.show()

def generateboard(self):
    Sudoku_Generator.SudokuBoard