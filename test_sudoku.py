from notgraphical import Sudoku
import sys


def test_load_sudoku_file():
    puzzle=Sudoku()
    sudoku = puzzle.load_sudoku_puzzle()
    assert len(sudoku)==9
    for i in sudoku:
        assert len(i)==9
        for k in i:
            assert (k>=0 and k<=9)

def test_first_stage():
    puzzle=Sudoku()
    sudoku = puzzle.load_sudoku_puzzle()
    sudoku = puzzle.first_stage()
    for i in range(9):
        for j in range(9):
            if isinstance(sudoku[i][j], list):
                assert sudoku[i][j]==[1,2,3,4,5,6,7,8,9]

def test_second_stage():
    puzzle=Sudoku()
    sudoku = puzzle.load_sudoku_puzzle()
    sudoku = puzzle.first_stage()
    sudoku = puzzle.second_stage()
    for i in range(9):
        for j in range(9):
            if isinstance(sudoku[i][j], int):
                #check the line
                for jj in range(9):
                    if isinstance(sudoku[i][jj], list):
                        assert sudoku[i][j] not in sudoku[i][jj]

                #check the column
                for ii in range(9):
                    if isinstance(sudoku[ii][j], list):
                        assert sudoku[i][j] not in sudoku[ii][j]

                #check the box
                boxi = int(i/3)
                boxj = int(j/3)
                for iii in range(3*boxi,3*boxi+3):
                    for jjj in range(3*boxj, 3*boxj+3):
                        if isinstance(sudoku[iii][jjj], list):
                            assert sudoku[i][j] not in sudoku[iii][jjj]
