import math
import random
import numpy as np
import time

# number of rows on the board
ROWS = 6
# number of columns on the board
COLUMNS = 7
# player's turn number
PLAYER = 1
# AI's turn number
AI = 2
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
DEPTH = 100
# the time per AI move
TIME = 5

# creates the initial board
def createBoard():
    board = np.zeros((ROWS, COLUMNS))
    return board

# drops a piece into a designated location
def drop(board, row, col, piece):
    board[row][col] = piece

# determines whether a column is full
def validColumn(board, col):
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

# heuristic function for minimax
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
    return win(board, PLAYER_PIECE) or win(board, AI_PIECE) or len(getValidColumns(board)) == 0

# minimax function
def minimax(board, depth, alpha, beta, maxPlayer):
    valid = getValidColumns(board)
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
def getValidColumns(board):
    valid = []
    for c in range(COLUMNS):
        if validColumn(board, c):
            valid.append(c)
    return valid

# determines the best move based on heuristic functions
def moveSelect(board, piece):
    valid = getValidColumns(board)
    bestScore = -10000
    bestCol = random.choice(valid)
    for c in valid:
        global NODES
        NODES += 1
        r = nextOpenRow(board, c)
        boardCopy = board.copy()
        drop(boardCopy, r, c, piece)
        curr_score = scorePos(boardCopy, piece)
        if curr_score > bestScore:
            bestScore = curr_score
            bestCol = c

    return bestCol

# Node class for MCTS
class Node:
    # Class initialization
    def __init__(self, parent, board, turn):
        # Parent node
        self.parent = parent
        # Board state of node
        self.board = board
        # Flip turn
        if turn == PLAYER:
            self.turn = AI
        else:
            self.turn = PLAYER
        # Total outcomes
        self.outcomes = 0 
        # Number of visits
        self.visits = 0 
        # Undiscovered children
        self.children = []
        # Not yet expanded
        self.expanded = False
        # Terminal node or not
        self.terminal = isTerminal(self.board)

        # Add child to node
    def addChild(self):
        # node already expanded
        if self.expanded:
            return
        # get board of every child
        childBoard = list()
        for child in self.children:
            childBoard.append(child.board)
        # find new child
        valid = getValidColumns(self.board)
        # For all valid columns
        for c in valid:
            for r in range(ROWS): # Not using nextOpenRow method because it gave issues
                if self.board[r, c] == 0:
                    boardCopy = self.board.copy()
                    if self.turn == PLAYER:
                        drop(boardCopy, r, c, AI) # create child state
                        if childBoard:
                            if not self.compare(boardCopy, childBoard):
                                self.children.append(Node(self, boardCopy, PLAYER)) # add child node
                                return
                            else:
                                break
                        else:
                            self.children.append(Node(self, boardCopy, PLAYER))
                            return
                    else:
                        drop(boardCopy, r, c, PLAYER)
                        if childBoard:
                            if not self.compare(boardCopy, childBoard):
                                self.children.append(Node(self, boardCopy, AI))
                                return
                            else:
                                break
                        else:
                            self.children.append(Node(self, boardCopy, AI))
                            return
        # no children found
        self.expanded = True
        return

    # Checks if states are equal
    def compare(self, new, children):
        for c in children:
            if (new == c).all():
                return True
        return False

# Checks if all of a node's children are visited
def fullyExpanded(node):
    visited = True
    if len(getValidColumns(node.board)) == len(node.children):
        for child in node.children:
            if child.visits == 0:
                visited = False
        return visited
    else:
        return False
    
# Updates the number of visits and outcomes of each node
def backpropagate(node, outcome):
    # add when AI wins
    if node.turn == AI_PIECE:
        node.outcomes += outcome
    # subtract when AI loses
    else:
        node.outcomes -= outcome
    node.visits += 1
    # stop at the top of the tree
    if node.parent is None:
        return
    else:
        backpropagate(node.parent, outcome)

# Simulates moves from a given node and returns outcome
def rollout(node):
    board = node.board
    turn = node.turn
    if not node.terminal:
        while(True):
            # flip turn
            if turn == 1:
                turn = 2
            else:
                turn = 1
            moves = getMoves(board, turn) # possible board positions from node
            if moves:
                board = random.choice(moves) # randomly selects move
                if (win(board, AI_PIECE)):
                    return 1
                elif (win(board, PLAYER_PIECE)):
                    return -1
            # no moves left
            else:
                return calcOutcome(board)
    # node is terminal
    else:
        return calcOutcome(board)
    
# Return outcome
def calcOutcome(board):
    if (win(board, AI_PIECE)):
        return 1
    elif (win(board, PLAYER_PIECE)):
        return -1
    else:
        return 0
    
# Returns possible moves from board given turn
def getMoves(board, turn):
    moves = list()
    valid = getValidColumns(board)
    for c in valid:
        r = nextOpenRow(board, c)
        boardCopy = board.copy()
        if turn == AI:
            drop(boardCopy, r, c, PLAYER_PIECE)
        else:
            drop(boardCopy, r, c, AI_PIECE)
        moves.append(boardCopy)
        break
    return moves

# Chooses an unexplored child
def pick(children):
    for child in children:
        if child.visits == 0:
            return child
        
# Return the child with best UCT value
def selectUCT(node):
    bestUCT = -10000000
    best_node = None
    for child in node.children:
        uct = (child.outcomes/child.visits) + 2*math.sqrt((math.log(node.visits))/child.visits)
        if uct > bestUCT:
            bestUCT = uct
            best_node = child
    if best_node is None:
        return node
    else:
        return best_node

# Selection of nodes 
def select(node):
    while(fullyExpanded(node)):
        new = selectUCT(node)
        if new == node:
            break
        else:
            node = new
    if node.terminal:
        return node
    else:
        node.addChild()
        global NODES
        NODES += 1
        if node.children:
            return pick(node.children)
        else:
            return node

# Runs the monte carlo algorithm
def monteCarlo(root):
    start = time.time()
    while(time.time() - start) < TIME:
        # selection and expansion
        leaf = select(root)
        # simulation
        result = rollout(leaf)
        # backpropogation
        backpropagate(leaf, result)

    return bestMove(root)
            
# Returns best move
def bestMove(node):
    maxVisit = 0
    best = None
    for child in node.children:
        if child.visits > maxVisit:
            maxVisit = child.visits
            best = child
    for r in range(ROWS):
        for c in range(COLUMNS):
            if best.board[r][c] != node.board[r][c]:
                return c

# create initial board
board = createBoard()
# random first turn
turn = random.randint(PLAYER, AI)
gameOver = False

# game loop
while not gameOver:
    # player's turn
    if turn == PLAYER:
        printBoard(board)
        # player inputs column
        col = int(input("Make your Selection (0-6):"))

        # processes a turn
        if validColumn(board, col):
            row = nextOpenRow(board, col)
            drop(board, row, col, PLAYER_PIECE)
            if turn == AI:
                turn = PLAYER
            else:
                turn = AI
            
            # processes a winning move
            if win(board, PLAYER_PIECE):
                printBoard(board)
                print("GOAT status achieved. Respect.")
                gameOver = True
                break

    # AI's turn
    if turn == AI:
        # nodes explored in a turn
        NODES = 0
        # column determined as best move
        col = 0
        # minimax score of placing the piece in column
        minimaxScore = 0
        # max depth explored in a turn
        maxDepth = 0

        # uncomment below lines to play with minimax

        # timer start
        # start = time.time()
        # # iterates depth until time limit passes
        # for i in range(DEPTH):
        #     end = time.time()
        #     if (end - start < TIME):
        #         col, minimaxScore = minimax(board, i, -math.inf, math.inf, True)
        #         maxDepth = i
        # print("Max depth: " + str(maxDepth))
        
        # comment out below lines to play with minimax

        # initialize root node
        root = Node(None, board, AI)
        col = monteCarlo(root)

        # uncomment this line to play with the basic AI agent
        # col = moveSelect(board, AI_PIECE)

        print("Total nodes searched: " + str(NODES))

        # processes a turn 
        if validColumn(board, col):
            row = nextOpenRow(board, col)
            drop(board, row, col, AI_PIECE)
            if turn == AI:
                turn = PLAYER
            else:
                turn = AI

            # processes a winning move
            if win(board, AI_PIECE):
                printBoard(board)
                print("You lost to the AI :( Better luck next time!)")
                gameOver = True
                break
        