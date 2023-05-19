import numpy as np
import random
import pygame
import sys
import math
from tkinter import Tk, Label, Button, StringVar
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROWS = 6
COLUMNS = 7

PLAYER1 = 0
PLAYER2 = 1

EMPTY = 0
PLAYER1_PIECE = 1
PLAYER2_PIECE = 2

WINDOW_LENGTH = 4


def create_board():
    board = np.zeros((ROWS, COLUMNS))
    return board

def dropToken(board, row, col, token):
    board[row][col] = token

def is_valid(board, col):
    return board[ROWS - 1][col] == 0

def getNextValidRow(board, col):
    for row in range(ROWS):
        if board[row][col] == 0:
            return row
def print_board(board):
    print(np.flip(board, 0))