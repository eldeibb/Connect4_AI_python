import numpy as np
import random
import pygame
import sys
import math
from tkinter import Tk, Label, Button, StringVar, Checkbutton

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
root = Tk()
root.title("Connect Four - Difficulty Level")

difficulty = StringVar(root)
algorithm = StringVar(root)

def set_difficulty(selected):
    difficulty.set(selected)
    root.destroy()

def set_algorithm(Selected):
    algorithm.set(Selected)
    root.destroy()

label_algorithm = Label(root, text="Choose the algorithm:")
label_algorithm.pack()

algorithm_type = StringVar(root)

checkbox_algorithm1 = Checkbutton(root, text="Minimax", variable=algorithm_type, onvalue="Minimax", offvalue="")
checkbox_algorithm1.pack()

checkbox_algorithm2 = Checkbutton(root, text="Alpha-beta", variable=algorithm_type, onvalue="Alpha-beta", offvalue="")
checkbox_algorithm2.pack()


label = Label(root, text="Choose the difficulty level:")
label.pack()

button1 = Button(root, text="Easy", command=lambda: set_difficulty("Easy"))
button1.pack()

button2 = Button(root, text="Medium", command=lambda: set_difficulty("Medium"))
button2.pack()

button3 = Button(root, text="Hard", command=lambda: set_difficulty("Hard"))
button3.pack()


root.mainloop()
selected_difficulty = difficulty.get()


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

    
def selectDepth(selected_difficulty):
    if (selected_difficulty == "Easy"):
        return 3
    elif (selected_difficulty == "Medium"):
        return 5
    elif (selected_difficulty == "Hard"):
        return 7
    
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

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = getValidLocations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, PLAYER2_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER1_PIECE):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, PLAYER2_PIECE))


    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = getNextValidRow(board, col)
            b_copy = board.copy()
            dropToken(b_copy, row, col, PLAYER2_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value


    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = getNextValidRow(board, col)
            b_copy = board.copy()
            dropToken(b_copy, row, col, PLAYER1_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def draw_board(board):
    for col in range(COLUMNS):
        for row in range(ROWS):
            pygame.draw.rect(screen, BLUE, (col * SQUARESIZE, row * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
            int(col * SQUARESIZE + SQUARESIZE / 2), int(row * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for col in range(COLUMNS):
        for row in range(ROWS):
            if board[row][col] == PLAYER1_PIECE:
                pygame.draw.circle(screen, RED, (
                int(col * SQUARESIZE + SQUARESIZE / 2), height - int(row * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[row][col] == PLAYER2_PIECE:
                pygame.draw.circle(screen, YELLOW, (
                int(col * SQUARESIZE + SQUARESIZE / 2), height - int(row * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

board = create_board()
print_board(board)
game_over = False

pygame.init()

SQUARESIZE = 100

width = COLUMNS * SQUARESIZE
height = (ROWS + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

turn = random.randint(PLAYER1, PLAYER2)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER1:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            # print(event.pos)
            # Ask for Player 1 Input
            if turn == PLAYER1:
                #depth = selectDepth(selected_difficulty)
                col, minimax_score = minimax(board, 2, -math.inf, math.inf, True)

                if is_valid(board, col):
                    # pygame.time.wait(500)
                    row = getNextValidRow(board, col)
                    dropToken(board, row, col, PLAYER1_PIECE)

                    if winning_move(board, PLAYER1_PIECE):
                        label = myfont.render("Player 1 wins!!", True, RED)
                        screen.blit(label, (40, 10))
                        game_over = True

                    print_board(board)
                    draw_board(board)

                    turn += 1
                    turn = turn % 2
    # # Ask for Player 2 Input
    if turn == PLAYER2 and not game_over:

        # col = random.randint(0, COLUMN_COUNT-1)
        # col = pick_best_move(board, AI_PIECE)
        depth = selectDepth(selected_difficulty)
        col, minimax_score = minimax(board, depth, -math.inf, math.inf, True)

        if is_valid(board, col):
            # pygame.time.wait(500)
            row = getNextValidRow(board, col)
            dropToken(board, row, col, PLAYER2_PIECE)

            if winning_move(board, PLAYER2_PIECE):
                label = myfont.render("Player 2 wins!!",True, YELLOW)
                screen.blit(label, (40, 10))
                game_over = True

            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2

    if game_over:
        pygame.time.wait(3000)
