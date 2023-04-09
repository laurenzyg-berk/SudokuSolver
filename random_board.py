# random_board.py

from starter import fill_board, print_board
import requests as reqs
import random

BOARD_LEN = 9
NUM_LEVELS = 4
MASTER_ARR = []
LINK_ARR = ["https://raw.githubusercontent.com/grantm/sudoku-exchange-puzzle-bank/master/easy.txt",
            "https://raw.githubusercontent.com/grantm/sudoku-exchange-puzzle-bank/master/medium.txt",
            "https://raw.githubusercontent.com/grantm/sudoku-exchange-puzzle-bank/master/hard.txt",
            "https://raw.githubusercontent.com/grantm/sudoku-exchange-puzzle-bank/master/diabolical.txt"]

"""
engine:
    Retrieves the desired level of difficulty from the user, gets the sudoku board corresponding to that difficulty level, and solves the board.
"""
def engine():
    level = int(input("Enter level of difficulty: \n(Easy = 1 | Medium = 2 | Hard = 3 | Diabolical = 4)\n"))
    correct_input = level == 1 or level == 2 or level == 3 or level == 4
    if not correct_input:
        while (not correct_input):
            level = input("Invalid input. Please enter a number from 1-4 corresponding to difficulty level\n1 = easiest, 4 = hardest\n")
            correct_input = level == 1 or level == 2 or level == 3 or level == 4
    
    # get a random sudoku board from the link corresponding to the requested difficulty level
    board = get_board(level)
    # solve the board
    fill_board(board)

"""
get_board:
    Retrieves a random sudoku puzzle of a given difficulty from a link to a puzzle bank, and returns the unsolved puzzle.
"""
def get_board(level):
    link = ""
    if MASTER_ARR == []:
        for i in range(NUM_LEVELS):
            MASTER_ARR.append([])

    # zero-indexing
    level -= 1

    if MASTER_ARR[level] == []:
        link = LINK_ARR[level]
        MASTER_ARR[level] = retrieve_arr(link)
    # pick random line (sudoku) to retrieve
    puzzle_num = random.randint(0, len(MASTER_ARR[level]) - 1)
    puzzle_line = (MASTER_ARR[level])[puzzle_num]
    # parse through puzzle line, return board
    return parse_board(puzzle_line)

"""
retrieve_arr:
    Helper function for get_board.
    Retrieves and returns an array of sudoku puzzles from a given link.
"""
def retrieve_arr(link):
    page = reqs.get(link)
    arr = []
    for line in page.text.split('\n'):
        arr += [''.join(line)]
    return arr

"""
parse_board:
    Parses through a line containing a sudoku board, and returns the board as a 2D array.
"""
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
