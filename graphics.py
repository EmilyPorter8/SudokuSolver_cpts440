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

def generateboard():
    size = boardsize.get()
    create_sudoku_table()
    board = Sudoku_Generator.run(size)

make_board = tk.Button(input_frame, text="make the board", command=generateboard)
make_board.pack()

board_frame = tk.Frame(root)
board_frame.pack()

def create_sudoku_table():
    size = boardsize.get()
    actual_size = size * size
    for i in range(actual_size):
        for j in range(actual_size):
            entry = tk.Entry(board_frame, width=4, font=('Helvetica', 8), justify='center')
            entry.grid(row=i, column=j, padx=2, pady=2)


#create_sudoku_table()
root.mainloop()
