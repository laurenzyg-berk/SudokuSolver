from collections import deque

board = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]

board2 = [
    [9, 3, 0, 0, 5, 8, 4, 2, 7],
    [2, 4, 5, 9, 1, 7, 0, 8, 3],
    [0, 7, 8, 4, 3, 2, 9, 0, 5],
    [3, 5, 4, 2, 9, 0, 8, 7, 0],
    [7, 0, 2, 5, 8, 1, 3, 4, 9],
    [8, 1, 9, 7, 4, 3, 2, 5, 0],
    [4, 9, 7, 8, 0, 5, 1, 3, 2],
    [0, 2, 0, 3, 7, 0, 5, 0, 8],
    [5, 8, 3, 1, 2, 0, 7, 0, 0]
]

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
            if num != '.':
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

def fill_board(board):
    if not valid_starting_board(board):
        print("Invalid board, cannot be solved.")
        return
    print("Before:\n")
    print_board(board)
    print()
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
                        stack, board = backtrack(board, stack)
                        if len(stack) == 0:
                            print("Invalid board, cannot be solved.")
                            return
                        i, j = stack[-1][0], stack[-1][1]
            j += 1
        i += 1
        j = 0
    print("After:\n")
    print_board(board)

def backtrack(board, stack):
    if len(stack) == 0:
        return (stack, board)
    while len(stack) != 0:
        loc = stack.pop()
        i, j = loc[0], loc[1]
        cur = board[i][j]
        for k in range(cur, 10):
            if valid_board(board, i, j, k):
                board[i][j] = k
                stack.append(loc)
                return (stack, board)
        board[i][j] = 0
    return (stack, board)

fill_board(board)
