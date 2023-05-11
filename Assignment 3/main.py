# Define the dimensions of the board

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

def WinningMove(board,token):
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == token and board[row][col + 1] == token and board[row][col + 2] == token and \
                    board[row][col + 3] == token:
                return True

        # Check vertical locations for win
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if board[row][col] == token and board[row + 1][col] == token and board[row + 2][col] == token and \
                    board[row + 3][col] == token:
                return True

        # Check positively sloped diagonals for win
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == token and board[row + 1][col + 1] == token and board[row + 2][col + 2] == token and \
                    board[row + 3][col + 3] == token:
                return True

        # Check negatively sloped diagonals for win
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == token and board[row - 1][col + 1] == token and board[row - 2][col + 2] == token and \
                    board[row - 3][col + 3] == token:
                return True

    return False

def DropToken(y,token):
    for i in range(ROWS):
        if(board[ROWS-i-1][y] == 0):
            board[ROWS-i-1][y] = token
            return WinningMove(board,token)

while(True):
    token1=int(input("Player1 -> Enter a number from 0 to 6 "))
    if(DropToken(token1,YellowToken)):
        print("Player2 won!!")
        break
    printBoard()
    token2=int(input("Player2 -> Enter a number from 0 to 6"))
    if(DropToken(token2,RedToken)):
        print("Player1 won!!")
        break
    printBoard()






