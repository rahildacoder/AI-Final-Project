import math
import random
import numpy as np
import time

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
# represents the player's piece on the board
PLAYER_PIECE = 1
# represents the AI's piece on the board
AI_PIECE = 2
# number of pieces in a row for a win
WINDOW_LENGTH = 4
# the number of nodes traversed in a move
NODES = 0
# the depth for the minimax
DEPTH = 10

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
        score += 5
    # checks for two pieces with available spots for two more
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    # checks if opponent has three pieces in a row with a spot for another
    if window.count(opp_Piece) == 3 and window.count(EMPTY) == 1:
        score -= 4
    
    return score

# heuristic function
def scorePos(board, piece):
    score = 0

    # center column score
    centerArr = [int(i) for i in list(board[:, COLUMNS//2])]
    centerCount = centerArr.count(piece)
    score += centerCount * 3

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

# determines whether a certain move is terminal
def isTerminal(board):
    return win(board, PLAYER_PIECE) or win(board, AI_PIECE) or len(getValidLocations(board)) == 0

# minimax function
def minimax(board, depth, alpha, beta, maxPlayer):
    valid = getValidLocations(board)
    terminal = isTerminal(board)
    if depth == 0 or terminal:
        global NODES
        NODES += 1
        if terminal:
            if win(board, AI_PIECE):
                return (None, 10000000000000)
            elif win(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else:
                # no valid moves left, game over
                return (None, 0) 
        else: 
            return (None, scorePos(board, AI_PIECE))
    if maxPlayer:
        currScore = -math.inf
        bestCol = random.choice(valid)
        for c in valid:
            NODES += 1
            r = nextOpenRow(board, c)
            boardCopy = board.copy()
            drop(boardCopy, r, c, AI_PIECE)
            newScore = minimax(boardCopy, depth - 1, alpha, beta, False)[1]
            if newScore > currScore:
                currScore = newScore
                bestCol = c
            alpha = max(alpha, currScore)
            if alpha >= beta:
                break
        return bestCol, currScore
    
    else:
        currScore = math.inf
        bestCol = random.choice(valid)
        for c in valid:
            NODES += 1
            r = nextOpenRow(board, c)
            boardCopy = board.copy()
            drop(boardCopy, r, c, PLAYER_PIECE)
            newScore = minimax(boardCopy, depth - 1, alpha, beta, True)[1]
            if newScore < currScore:
                currScore = newScore
                bestCol = c
            beta = min(beta, currScore)
            if alpha >= beta:
                break
        return bestCol, currScore

# determines all valid columns on a board
def getValidLocations(board):
    valid = []
    for c in range(COLUMNS):
        if validLocation(board, c):
            valid.append(c)
    return valid

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
        NODES = 0
        col = 0
        minimaxScore = 0
        # col = bestMove(board, AI_PIECE)
        start = time.time()
        for i in range(DEPTH):
            end = time.time()
            if (end - start < 5):
                col, minimaxScore = minimax(board, i, -math.inf, math.inf, True)
        print("Total nodes searched: " + str(NODES))

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
        