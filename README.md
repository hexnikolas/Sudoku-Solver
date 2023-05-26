# Sudoku Solver

This application solves sudoku puzzles using sudoku logic (and not a backtracking algorithm).

It gets a puzzle in the form of a string like the following: ```..5..97...6.....2.1..8....6.1.7....4..7.6..3.6....32.......6.4..9..5.1..8..1....2``` where the first line of the puzzle are the nine first numbers, the second line of the puzzle are numbers 10-18 etc. Dots represent the empty cells. It returns the solved puzzle

####  Requirements:
- numpy
- Qt5 
- pytest 

```graphical.py``` returns a new graphical window that shows the solved puzzle, while ```notgraphical.py``` returns the solved puzzle in the standard output.
```test_sudoku.py``` are the unit tests of the solver.

#### Usage
```python3 graphical.py``` executes the graphical application.
```python3 notgraphical.py``` executes the not graphical application
```pytest``` executes the unit tests of the application.
