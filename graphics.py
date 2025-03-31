import tksheet
from tksheet import Sheet
import tkinter as tk
import Sudoku_Generator as Sudoku_Generator 

root = tk.Tk()
root.title("Sudoku Solver")

input_frame = tk.Frame(root)
input_frame.pack()


boardsize = tk.IntVar()
slider = tk.Scale( input_frame, variable = boardsize,  
           from_ = 3, to = 9,  
           orient = tk.HORIZONTAL) 
slider.pack()
sheet = None
board_frame = tk.Frame(root)
board_frame.pack(expand =True, fill = "both")
sheet = tksheet.Sheet(board_frame)
sheet.grid()

def generateboard():
    size = boardsize.get()
   # reset_board()


    board_frame.pack(expand =True, fill = "both")
    sheet = tksheet.Sheet(board_frame)
    sheet.grid()

    create_sudoku_sheet()
    board = Sudoku_Generator.run(size)

make_board = tk.Button(input_frame, text="make the board", command=generateboard)
make_board.pack()

def create_sudoku_sheet():
    global sheet
    size = boardsize.get()
    if not sheet:
        print("sheet did not create for some reason")
        return

    actual_size = size * size

#replace with actual data
    test_data = [[f"{ri},{cj}" for cj in range(actual_size)] for ri in range(actual_size)]
    sheet.set_sheet_data(test_data)

    try:
        sheet.enable_bindings(("arrowkeys", "right", "left", "up", "down"))
    except Exception as e:
        print(f"error adding bindings to sheet: {e}")



def reset_board():
    for child in board_frame.winfo_children():
        child.destroy()

#old funciton
def create_sudoku_table():
    reset_board()
    size = boardsize.get()
    actual_size = size * size
    for i in range(actual_size):
        for j in range(actual_size):
            entry = tk.Entry(board_frame, width=4, font=('Helvetica', 8), justify='center')
            entry.grid(row=i, column=j, padx=2, pady=2)


#create_sudoku_table()
root.mainloop()
