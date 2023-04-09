# starter.py

# Helper functions for Sudoku GUI

from collections import deque

"""
print_board:
    Prints a nicely formatted Sudoku board for visualization. 
    Does not return anything.
"""
def print_board(board):
    rows, cols = len(board), len(board[0])
    for i in range(rows):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - ")
        for j in range(cols):
            if j % 3 == 0 and j != 0:
                print("| ", end="")
            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")

"""
valid_starting_board:
    Checks that thes starting Sudoku board is valid.
    Returns True if the board is valid; returns False otherwise.
"""
def valid_starting_board(board):
    length = len(board)
    rows_list, cols_list, quads_list = [], [], []
    for i in range(length):
        rows_list.append([])
        cols_list.append([])
        quads_list.append([])
    for i in range(length):
        for j in range(length):
            num = board[i][j]
            if num != 0:
                if num in rows_list[i]:
                    return False
                elif num in cols_list[j]:
                    return False
                elif num in quads_list[(3 * (i // 3) + (j // 3))]:
                    return False
                rows_list[i].append(num)
                cols_list[j].append(num)
                quads_list[(3 * (i // 3) + (j // 3))].append(num)
    return True

"""
valid_board:
    Checks that it is a valid move to place num at location [i, j] on the current board. 
    Returns True if move is valid; returns False otherwise.
"""
def valid_board(board, i, j, num):
    rows, cols = len(board), len(board[0])
    # check values in row
    for k in range(cols):
        if num == board[i][k]:
            return False
    # check values in column
    for k in range(rows):
        if num == board[k][j]:
            return False
    # check values in quadrant
    # figure out quadrant
    if i <= 2:
        rows = range(3)
    elif i <= 5:
        rows = range(3, 6)
    else:
        rows = range(6, 9)
    if j <= 2:
        cols = range(3)
    elif j <= 5:
        cols = range(3, 6)
    else:
        cols = range(6, 9)
    for ii in rows:
        for jj in cols:
            if num == board[ii][jj]:
                return False
    return True

"""
fill_board:
    Solves the given Sudoku board.
    Returns True if the board is able to be solved; returns False otherwise.
"""
def fill_board(board):
    if not valid_starting_board(board):
        return False
    rows, cols = len(board), len(board[0])
    stack = deque()
    i, j = 0, 0
    while i < rows:
        while j < cols:
            if board[i][j] == 0:
                for k in range(1, 10):
                    if valid_board(board, i, j, k):
                        board[i][j] = k
                        stack.append((i, j))
                        break
                    if k == 9:
                        # backtrack
                        board, stack = backtrack(board, stack)
                        if len(stack) == 0:
                            return False
                        i, j = stack[-1][0], stack[-1][1]
            j += 1
        i += 1
        j = 0
    return True

"""
backtrack:
    Helper function for fill_board.
    Backtracks through a stack of locations until a new valid move is found; returns the new board and stack.
"""
def backtrack(board, stack):
    if len(stack) == 0:
        return (board, stack)
    while len(stack) != 0:
        loc = stack.pop()
        i, j = loc[0], loc[1]
        cur = board[i][j]
        for k in range(cur, 10):
            if valid_board(board, i, j, k):
                board[i][j] = k
                stack.append(loc)
                return (board, stack)
        board[i][j] = 0
    return (board, stack)
