# Define the dimensions of the board
import numpy as np

ROWS = 6
COLUMNS = 7
RedToken = 1
YellowToken = 2

def createBoard() :
    board = [[0 for j in range(COLUMNS)] for i in range(ROWS)]
    return board

board = createBoard()
def printBoard():
    for ROWS in board:
        print(ROWS)

def CheckPlace(x,y):
    return board[ROWS - x - 1][y]==0

def DropToken(y,token):
    for i in range(ROWS):
        if(board[ROWS-i-1][y] == 0):
            board[ROWS-i-1][y] = token
            break

DropToken(1,RedToken)
DropToken(2,YellowToken)
DropToken(1,RedToken)
DropToken(2,YellowToken)
DropToken(2,RedToken)
printBoard()





