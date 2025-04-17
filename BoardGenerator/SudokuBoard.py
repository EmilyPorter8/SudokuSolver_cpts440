import csv
import random
import numpy as np
import math

#need these files in same directory to run
filenames = ['BoardGenerator/sudoku_9x9.csv', 'BoardGenerator/sudoku_16x16_shuffled.csv', 'BoardGenerator/sudoku_25x25.csv', 'BoardGenerator/sudoku_36x36.csv', 'BoardGenerator/Sudoku_49x49_Board.csv', 'BoardGenerator/64x64_Sudoku_Board.csv', 'BoardGenerator/sudoku_81x81.csv' ,'BoardGenerator/Shuffled_100x100_Sudoku_Board.csv']
size = 0

def generate_puzzle_from_csv(filename, remove):

    with open(filename, 'r') as f:
        reader = csv.reader(f)
        board = [list(map(int, row)) for row in reader]

    board = np.array(board)
    size = board.shape[0]
    total = size * size

    # Randomly choose cells to remove
    indices = random.sample(range(total), remove)
    for idx in indices:
        r, c = divmod(idx, size)
        board[r, c] = 0

    # Print the puzzle
    for row in board:
        print(' '.join(f"{val:2}" for val in row))

    return board

def test():
    index = int(input('Please enter the size of your desired board, 3 for 9x9, 4 for 16x16 ... 10 for 100x100: '))
    #adjustable difficulty as prof suggested
    difficulty = int(input('Please enter the desired difficulty, 0 easy, 1 medium, 2 hard: '))

    size = index**4

    index -= 3


    if difficulty == 0:
        num_remove = int(size * 0.2)#removes 20% of squares
    elif difficulty == 1:
        num_remove = int(size * 0.6)#removes 60% of squares
    else:
        num_remove = int(size * 0.8)#removes 80% of squares

    board = generate_puzzle_from_csv(filenames[index], num_remove)

#emilys attempt
def run(block_size, selected_difficulty):
    global size    
    size = block_size**4
    index = block_size-3

    if selected_difficulty == 0:
        remove = int(size * 0.2)#removes 20% of squares
    elif selected_difficulty == 1:
        remove = int(size * 0.6)#removes 60% of squares
    else:
        remove = int(size * 0.8)#removes 80% of squares
    filename = filenames[index]  # ← Fix here

    board = generate_puzzle_from_csv(filename, remove)

    # board.fill_diagonal_boxes()
    # board.fill_remaining_bands()

    # removal_ratio = 0.5  # Adjust this value to control puzzle difficulty
    # removal_count = int(board.size * board.size * removal_ratio)
    # board.dig_holes(removal_count)
    return board
