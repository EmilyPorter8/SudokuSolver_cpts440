import tksheet
from tksheet import Sheet
import tkinter as tk
import Sudoku_Generator as Sudoku_Generator 
import CNF
import Z3_IO 
import z3solver

root = tk.Tk()
root.title("Sudoku Solver")

input_frame = tk.Frame(root)
input_frame.pack()

selected_solver = tk.StringVar()
selected_solver.set("Z3")
solvers = ["Z3", "DFS", "Whatever else"]

boardsize = tk.IntVar()
slider = tk.Scale( input_frame, variable = boardsize,  
           from_ = 3, to = 9,  
           orient = tk.HORIZONTAL) 
slider.pack()

board_frame = tk.Frame(root, width=5000, height = 5000)
board_frame.pack(expand =True, fill = "both")
sheet = tksheet.Sheet(board_frame)
sheet.grid()
BackendBoard = None

def generateboard():
    size = boardsize.get()
   # reset_board()

    board_frame.pack(expand =True, fill = "both")
    sheet = tksheet.Sheet(board_frame)
    sheet.grid()
    create_sudoku_sheet()
    solve_board_bt['state'] = tk.NORMAL
    #sheet.pack(expand = True, fill = "both")
    #board = Sudoku_Generator.run(size)

def generatesolvedboard(solved_board):
    if(solved_board):
        sheet.set_sheet_data(solved_board)
        sheet.set_all_cell_sizes_to_text()
    else:
        #show unsolvable
        print("Board cannot be solved")


make_board = tk.Button(input_frame, text="make the board", command=generateboard)
make_board.pack()

def z3_solve():
    # cnf_clauses = CNF.generate_sudoku_cnf(boardsize*boardsize) #call shampurna's cnf
    # CNF.save_cnf(cnf_clauses)
    print("Solving board for Z3...")
    cnf = Z3_IO.z3_io.sudoku_to_cnf(BackendBoard, boardsize*boardsize)
    # cnf_clauses = CNF.generate_sudoku_cnf(boardsize*boardsize) #call shampurna's cnf
    # # CNF.save_cnf(cnf_clauses)
    solution = z3solver.solve_cnf(cnf)
    if solution:
        return Z3_IO.z3_io.cnf_to_sudoku(solution, boardsize*boardsize)
    else:
        return None


def solveboard():
    solve_board_bt['state'] = tk.DISABLED #reset button
    print(selected_solver)
    if selected_solver.get() == "Z3":
        print("Solving board for Z3...")
        solved_board = z3_solve()
        generatesolvedboard(solved_board)
    elif selected_solver.get() == "DFS":
        print("Solving board for DFS...")
    return

select_solver_menu = tk.OptionMenu(input_frame, selected_solver, *solvers)
select_solver_menu.pack()
solve_board_bt = tk.Button(input_frame, text = "Solve the board", state = tk.DISABLED,command = solveboard)
solve_board_bt.pack()

def create_sudoku_sheet():
    global sheet, BackendBoard
    size = boardsize.get()
    if not sheet:
        print("sheet did not create for some reason")
        return

    actual_size = size * size
    BackendBoard = Sudoku_Generator.run(size)
    test_data = [[
    " " if BackendBoard.valueReturn(cj, ri) == 0 else f"{BackendBoard.valueReturn(cj, ri)}"
    for cj in range(actual_size)] for ri in range(actual_size)]
    sheet.set_sheet_data(test_data)
    sheet.set_all_cell_sizes_to_text()


    try:
        sheet.enable_bindings(("arrowkeys", "right", "left", "up", "down"))
    except Exception as e:
        print(f"error adding bindings to sheet: {e}")



def reset_board():
    for child in board_frame.winfo_children():
        child.destroy()

    

#create_sudoku_table()
root.mainloop()
