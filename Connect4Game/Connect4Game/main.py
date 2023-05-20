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

def winning_move(board, token):
    # Check horizontal locations for win
    for col in range(COLUMNS - 3):
        for row in range(ROWS):
            if board[row][col] == token and board[row][col + 1] == token and board[row][col + 2] == token and board[row][
                col + 3] == token:
                return True

    # Check vertical locations for win
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if board[row][col] == token and board[row + 1][col] == token and board[row + 2][col] == token and board[row + 3][
                col] == token:
                return True

    # Check positively sloped diaganols
    for col in range(COLUMNS - 3):
        for row in range(ROWS - 3):
            if board[row][col] == token and board[row + 1][col + 1] == token and board[row + 2][col + 2] == token and board[row + 3][
                col + 3] == token:
                return True

    # Check negatively sloped diaganols
    for col in range(COLUMNS - 3):
        for row in range(3, ROWS):
            if board[row][col] == token and board[row - 1][col + 1] == token and board[row - 2][col + 2] == token and board[row - 3][
                col + 3] == token:
                return True
def evaluate_window(window, token):
    score = 0
    opp_token = PLAYER1_PIECE
    if token == PLAYER1_PIECE:
        opp_token = PLAYER2_PIECE

    if window.count(token) == 4:
        score += 100
    elif window.count(token) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(token) == 2 and window.count(EMPTY) == 2:
        score += 2
    if window.count(opp_token) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

def score_position(board, token):
    score = 0

    ## Score center column
    center_array = [int(i) for i in list(board[:, COLUMNS // 2])]
    center_count = center_array.count(token)
    score += center_count * 3

    ## Score Horizontal
    for row in range(ROWS):
        row_array = [int(i) for i in list(board[row, :])]
        for col in range(COLUMNS - 3):
            window = row_array[col:col + WINDOW_LENGTH]
            score += evaluate_window(window, token)

    ## Score Vertical
    for col in range(COLUMNS):
        col_array = [int(i) for i in list(board[:, col])]
        for row in range(ROWS - 3):
            window = col_array[row:row + WINDOW_LENGTH]
            score += evaluate_window(window, token)

    ## Score posiive sloped diagonal
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            window = [board[row + i][col + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, token)

    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            window = [board[row + 3 - i][col + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, token)

    return score

def is_terminal_node(board):
    return winning_move(board, PLAYER1_PIECE) or winning_move(board, PLAYER2_PIECE) or len(getValidLocations(board)) == 0


def getValidLocations(board):
    validLocations = []
    for col in range(COLUMNS):
        if is_valid(board, col):
            validLocations.append(col)
    return validLocations

def pick_random_move(board):
    valid_locations = getValidLocations(board)
    return random.choice(valid_locations)

def pick_best_move(board, token):
    validLocations = getValidLocations(board)
    best_score = -10000
    best_col = random.choice(validLocations)
    for col in validLocations:
        row = getNextValidRow(board, col)
        temp_board = board.copy()
        dropToken(temp_board, row, col, token)
        score = score_position(temp_board, token)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col
