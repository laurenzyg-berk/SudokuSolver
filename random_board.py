# random_board.py

# Retrieves a random sudoku puzzle from a puzzle bank, and solves the puzzle.

from starter import fill_board, print_board
import requests as reqs
import random

BOARD_LEN = 9

def engine():
    level = int(input("Enter level of difficulty: \n(Easy = 1 | Medium = 2 | Hard = 3 | Diabolical = 4)\n"))
    correct_input = level == 1 or level == 2 or level == 3 or level == 4
    if not correct_input:
        while (not correct_input):
            level = input("Invalid input. Please enter a number from 1-4 corresponding to difficulty level\n1 = easiest, 4 = hardest\n")
            correct_input = level == 1 or level == 2 or level == 3 or level == 4
    
    link = ""
    if level == 1:
        link = "https://raw.githubusercontent.com/grantm/sudoku-exchange-puzzle-bank/master/easy.txt"
    elif level == 2:
        link = "https://raw.githubusercontent.com/grantm/sudoku-exchange-puzzle-bank/master/medium.txt"
    elif level == 3:
        link = "https://raw.githubusercontent.com/grantm/sudoku-exchange-puzzle-bank/master/hard.txt"
    else:
        link = "https://raw.githubusercontent.com/grantm/sudoku-exchange-puzzle-bank/master/diabolical.txt"
    
    page = reqs.get(link)
    arr = []
    for line in page.text.split('\n'):
        arr += [''.join(line)]
    # pick random line (sudoku) to retrieve
    puzzle_num = random.randint(0, len(arr) - 1)
    puzzle_line = arr[puzzle_num]
    # parse through line to get board
    board = parse_board(puzzle_line)
    fill_board(board)

def parse_board(line):
    board_line = ""
    for piece in line.split(' '):
        if len(piece) == BOARD_LEN * BOARD_LEN:
            board_line = piece
    if len(board_line) == 0:
        print("Invalid board. Please try again.")
        return [[]]
    board = []
    j = -1
    for i in range(BOARD_LEN):
        board.append([])
    for i in range(BOARD_LEN * BOARD_LEN):
        if i % BOARD_LEN == 0:
            j += 1
        board[j] += [int(board_line[i])]
    return board
        
        
engine()
    
