import random
import numpy as np

# number of rows on the board
ROWS = 6
# number of columns on the board
COLUMNS = 7
# player's turn number
PLAYER = 0
# AI's turn number
AI = 1
# empty spot on board
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
# number of pieces in a row for a win
WINDOW_LENGTH = 4

# creates the initial board
def createBoard():
    board = np.zeros((ROWS, COLUMNS))
    return board

# drops a piece into a designated location
def drop(board, row, col, piece):
    board[row][col] = piece

# determines whether a column is full
def validLocation(board, col):
    return board[ROWS - 1][col] == 0

# determines the next open row in a column
def nextOpenRow(board, col):
    for r in range(ROWS):
        if board[r][col] == 0:
            return r

# prints the board onto the console
def printBoard(board):
    print(np.flip(board, 0))

# checks whether a player has won
def win(board, piece):
    # horizontal
    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True
    
    # vertical
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True
    
    # positive diagonal
    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True
            
    # negative diagonal
    for c in range(COLUMNS - 3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True

# heuristic function
def scorePos(board, piece):
    score = 0
    # horizontal score
    for r in range(ROWS):
        rowArr = [int(i) for i in list(board[r, :])]
        for c in range(COLUMNS - 3):
            window = rowArr[c : c + WINDOW_LENGTH]
            score += windowEval(window, piece)
    
    # vertical score
    for c in range(COLUMNS):
        colArr = [int(i) for i in list(board[:, c])]
        for r in range(ROWS - 3):
            window = colArr[r : r + WINDOW_LENGTH]
            score += windowEval(window, piece)

    # positive diagonal score
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += windowEval(window, piece)
    
    # negative diagonal score
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += windowEval(window, piece)
                
    return score

# evaluates a score based on the number of pieces in a given window
def windowEval(window, piece):
    score = 0
    opp_Piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_Piece = AI_PIECE
    
    # checks for four pieces in a row
    if window.count(piece) == 4:
        score += 100
    # checks for three pieces with an available spot for a third
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 10
    # checks for two pieces with available spots for two more
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 5

    # checks if opponent has three pieces in a row with a spot for another
    if window.count(opp_Piece) == 3 and window.count(EMPTY) == 1:
        score -= 80
    
    return score

# determines all valid columns on a board
def getValidLocations(board):
    valid = []
    for c in range(COLUMNS):
        if validLocation(board, c):
            valid.append(c)
    return valid

# determines the best move based on heuristic functions
def bestMove(board, piece):
    valid = getValidLocations(board)
    bestScore = -10000
    bestCol = random.choice(valid)
    for c in valid:
        r = nextOpenRow(board, c)
        tempBoard = board.copy()
        drop(tempBoard, r, c, piece)
        curr_score = scorePos(tempBoard, piece)
        if curr_score > bestScore:
            bestScore = curr_score
            bestCol = c
    
    return bestCol

board = createBoard()
gameOver = False
turn = random.randint(PLAYER, AI)

# game loop
while not gameOver:
    # player's turn
    if turn == PLAYER:
        printBoard(board)
        # player inputs column
        col = int(input("Player 1 Make your Selection (0-6):"))

        # processes a turn
        if validLocation(board, col):
            row = nextOpenRow(board, col)
            drop(board, row, col, PLAYER_PIECE)
            turn += 1
            turn = turn % 2
            
            # processes a winning move
            if win(board, PLAYER_PIECE):
                printBoard(board)
                print("Player 1 GOAT status achieved. Respect.")
                gameOver = True
                break

    # AI's turn
    if turn == AI:
        col = bestMove(board, AI_PIECE)

        # processes a turn 
        if validLocation(board, col):
            row = nextOpenRow(board, col)
            drop(board, row, col, AI_PIECE)
            turn += 1
            turn = turn % 2

            # processes a winning move
            if win(board, AI_PIECE):
                printBoard(board)
                print("Player 2 GOAT status achieved. Respect.")
                gameOver = True
                break
        