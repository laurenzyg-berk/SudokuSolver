# GUI.py
# Adapted from Sudoku GUI from https://www.techwithtim.net/
"""
Run the program, select the level of difficulty (from 1-4) from the popup menu, and then the Sudoku GUI will pop up with the puzzle.
You can click on a square to fill it in, or move around with arrow keys. You can select a value from 1-9 to put in an empty square,
and the value will be pencilled in. You can hit the "Delete" key on your keyboard to erase the value that is pencilled in, or you can
hit another key (1-9) to pencil a different value in. If you would like to check a guess, hit "Enter" on a square that has a value 
pencilled in. If your guess is correct, the value will be placed there permanently; if your guess is incorrect, the value will be 
erased from the square. If you are done and would like the board to be solved, hit the space bar to watch the backtracking algorithm
solve the board. If you would like to just solve the board as quickly as possible, hit the shift key to watch the board be solved.
(The backtracking algorithm is fast, but updating the GUI to show each step is not fast)
"""

import pygame
import time
pygame.font.init()
from tkinter import *
from random_board import get_board
from starter import fill_board, valid_board, valid_starting_board
from collections import deque

ROOT = Tk()
LABEL = Label(ROOT, text = " ")
CLICKED = StringVar()

class Grid:
    # set a default board; actual board will be set when constructor is called
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

    def __init__(self, board, rows, cols, width, height):
        self.board = board
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None
    
    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.update_model()
            if valid_board(self.model, row, col, val):
                self.cubes[row][col].set(val)
                self.update_model()
                if fill_board(self.model):
                    return True
                else:
                    self.cubes[row][col].set(0)
                    self.cubes[row][col].set_temp(0)
                    self.update_model()
                    return False
        
    def place_temp(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.update_model()
            if valid_board(self.model, row, col, val):
                self.cubes[row][col].set(val)
                self.update_model()
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False
            
    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self, win):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)
    
    def select(self, row, col):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None
    
    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True
    
class Cube:
    rows = 9
    cols = 9
    locations = []
    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)
        for loc in Cube.locations:
            i, j = loc
            x = j * gap
            y = i * gap
            pygame.draw.rect(win, (0,255,0), (x + 1, y + 1, gap - 1 ,gap - 1), 3)

    def set(self, value):
        self.value = value
    
    def set_temp(self, temp_value):
        self.temp = temp_value

def redraw_window(win, board, time):
    win.fill((255,255,255))
    # Draw time
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + format_time(time), 1, (0,0,0))
    win.blit(text, (540 - 220, 560 - 20))
    # Draw grid and board
    board.draw(win)


def format_time(secs):
    sec = secs%60
    minute = secs//60
    hour = minute//60

    mat = " " + str(minute) + ":" + str(sec)
    return mat

def final_solve_fast(bo, win, start):
    board = bo.board
    if not valid_starting_board(board):
        return False
    rows, cols = len(board), len(board[0])
    stack = deque()
    i, j = 0, 0
    while i < rows:
        while j < cols:
            if bo.cubes[i][j].value == 0:
                bo.select(i, j)
                for k in range(1, 10):
                    # check if k works in the current board, and a solution can be found with k in the current location
                    if bo.place(k):
                        stack.append((i, j))
                        Cube.locations = stack
                        break
            redraw_window(win, bo, round(time.time() - start))
            pygame.display.update()
            j += 1
        i += 1
        j = 0
    Cube.locations = []
    return True

def final_solve(bo, win, start):
    board = bo.board
    if not valid_starting_board(board):
        return False
    rows, cols = len(board), len(board[0])
    stack = deque()
    i, j = 0, 0
    while i < rows:
        while j < cols:
            if bo.cubes[i][j].value == 0:
                bo.select(i, j)
                for k in range(1, 10):
                    # check if k works in the current board (doesn't check if board can be solved with k in current spot)
                    if bo.place_temp(k):
                        stack.append((i, j))
                        Cube.locations = stack
                        break
                    if k == 9:
                        # backtrack
                        stack = backtrack(bo, stack, win, start)
                        if len(stack) == 0:
                            return False
                        i, j = stack[-1][0], stack[-1][1]
            redraw_window(win, bo, round(time.time() - start))
            pygame.display.update()
            j += 1
        i += 1
        j = 0
    Cube.locations = []
    return True

def backtrack(bo, stack, win, start):
    if len(stack) == 0:
        return stack
    while len(stack) != 0:
        loc = stack.pop()
        i, j = loc
        Cube.locations = stack
        bo.select(i, j)
        cur = bo.cubes[i][j].value
        bo.cubes[i][j].set(0)
        bo.update_model()
        redraw_window(win, bo, round(time.time() - start))
        pygame.display.update()
        for k in range(cur + 1, 10):
            # check if board can be solved with k in current place
            if bo.place_temp(k):
                stack.append(loc)
                Cube.locations = stack
                redraw_window(win, bo, round(time.time() - start))
                pygame.display.update()
                return stack
        redraw_window(win, bo, round(time.time() - start))
        pygame.display.update()
    return stack
        

def main():
    ROOT.geometry("300x80")
    CLICKED.set("1")

    options = ["1", "2", "3", "4"]

    drop = OptionMenu(ROOT, CLICKED, *options)
    drop.pack()

    select_button = Button(ROOT, text = "Select a level (1 = easiest, 4 = hardest), then click me", command = ROOT.destroy).pack()
    LABEL.pack()
    ROOT.mainloop()
    
    board = get_board(int(CLICKED.get()))

    win = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku")
    board = Grid(board, 9, 9, 540, 540)
    key = None
    run = True
    start = time.time()
    final_time = round(time.time() - start)
    last_pos = None

    while run:

        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            board.clear()
                        key = None

                        if board.is_finished():
                            print("Game over")
                            run = False
                if event.key == pygame.K_SPACE:
                    # solve board using backtracking algorithm
                    final_solve(board, win, start)
                    final_time = round(time.time() - start)
                
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    # solve board quickly
                    final_solve_fast(board, win, start)
                    final_time = round(time.time() - start)

                if event.key == pygame.K_DOWN or event.key == pygame.K_UP or event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    if last_pos is None:
                        pos = pygame.mouse.get_pos()
                        last_pos = board.click(pos)
                    last_clicked = last_pos
                    if last_clicked:
                        if event.key == pygame.K_DOWN:
                            if last_clicked[0] == (board.rows - 1):
                                board.select(last_clicked[0], last_clicked[1])
                            else:
                                board.select(last_clicked[0] + 1, last_clicked[1])
                        elif event.key == pygame.K_UP:
                            if last_clicked[0] == 0:
                                board.select(last_clicked[0], last_clicked[1])
                            else:
                                board.select(last_clicked[0] - 1, last_clicked[1])
                        elif event.key == pygame.K_RIGHT:
                            if last_clicked[1] == (board.cols - 1):
                                board.select(last_clicked[0], last_clicked[1])
                            else:
                                board.select(last_clicked[0], last_clicked[1] + 1)
                        else:
                            if last_clicked[1] == 0:
                                board.select(last_clicked[0], last_clicked[1])
                            else:
                                board.select(last_clicked[0], last_clicked[1] - 1)
                        key = None
                        print(last_clicked[0], " ", last_clicked[1])
                        last_pos = board.selected
                    else:
                        board.select(0, 0)
                        last_pos = board.selected

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                last_pos = clicked
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key)

        if board.is_finished():
            redraw_window(win, board, final_time)
        else:
            redraw_window(win, board, play_time)
        pygame.display.update()



main()
pygame.quit()
