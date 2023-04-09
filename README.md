# SudokuSolver
Run the program from GUI.py, select the level of difficulty (1 = easy, 2 = medium, 3 = difficult, 4 = diabolical) from the popup menu, 
then the Sudoku GUI will pop up with the puzzle (the puzzle of given difficulty is retrieved from a bank of sudoku puzzles).

Once the GUI pops up, you can click on a square to fill it in, or you can move around using the arrow keys on your keyboard. You can 
hit a key from 1-9 while an empty square is selected, and the value will be pencilled into the square. (It must be an empty square - 
you cannot change the values that are already on the board) You can hit the "Delete" key on your keyboard to erase the value that is 
pencilled in, or you can hit another key (1-9) to pencil a different value in. If you would like to check if your guess is correct, 
hit "Enter" on a square that has a value pencilled in. If your guess is correct, the value will be placed there permanently; if your 
guess is incorrect, the value will be erased from the square. If you are done and would like the board to be solved, hit the space bar 
to watch the backtracking algorithm solve the board in action. If you would like to watch the board be solved as quickly as possible, 
hit the shift key to watch the board be solved. (The backtracking algorithm is fast, but updating the GUI to show each step is not fast)
