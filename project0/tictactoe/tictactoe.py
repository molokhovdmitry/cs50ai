"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy
import operator
from random import shuffle

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Count "X" and "O"
    Xcount = 0
    Ocount = 0
    for row in board:
        Xcount += row.count("X")
        Ocount += row.count("O")
    
    # Return player
    if Xcount > Ocount:
        return "O"
    else:
        return "X"


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Fill set
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i, j))
    
    # Return set
    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Validate action
    if action not in actions(board):
        raise Exception("Invalid action")
    
    # Deep copy
    boardCopy = deepcopy(board)

    # Make a move
    i = action[0]
    j = action[1]
    boardCopy[i][j] = player(board)

    return boardCopy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    Xcount = set()
    Ocount = set()
    # Check rows
    for row in board:
        Xcount.add(row.count("X"))
        Ocount.add(row.count("O"))

    # Check columns
    boardFlipped = [[col[i] for col in board] for i in range(3)]
    for row in boardFlipped:
        Xcount.add(row.count("X"))
        Ocount.add(row.count("O"))
    
    # Check diagonals
    diagonalLR = [board[i][i] for i in range(3)]
    Xcount.add(diagonalLR.count("X"))
    Ocount.add(diagonalLR.count("O"))
    
    diagonalRL = [board[i][2 - i] for i in range(3)]
    Xcount.add(diagonalRL.count("X"))
    Ocount.add(diagonalRL.count("O"))

    # Get winner
    if 3 in Xcount:
        return "X"
    elif 3 in Ocount:
        return "O"
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None or len(actions(board)) == 0:
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    w = winner(board)
    if w == "X":
        return 1
    elif w == "O":
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    """
    Pseudocode:
    check for terminal:
        if terminal:
            return none
        if not:
            for every action calculate minmax value
            if player is X:
                return action with max value
            else:
                return action with min value
    """
    # Return None if terminal board
    if terminal(board):
        return None

    # Initialize list that contains minmax values for every action in tuples
    minmaxes = []

    # If player is "X"
    if player(board) == "X":
        # Fill minmaxes list
        for action in actions(board):
            minmaxes.append((action, minValue(result(board, action), -3, 3, 0)))
        """
        Choose random action with max value.
        How to get a tuple element with max/min second value in a list: 
        https://stackoverflow.com/questions/13039192/max-second-element-in-tuples-python
        """
        shuffle(minmaxes)
        optimalAction = max(minmaxes, key=operator.itemgetter(1))[0]
        
    # If player is "O"
    else:
        # Fill minmaxes list
        for action in actions(board):
            minmaxes.append((action, maxValue(result(board, action), -3, 3, 0)))
        # Choose random action with min value
        shuffle(minmaxes)
        optimalAction = min(minmaxes, key=operator.itemgetter(1))[0]
    
    print(minmaxes)
    # Return optimal action
    return optimalAction


def maxValue(board, alpha, beta, level):
    """
    Returns max value of a board.
    'level' keeps track of how deep the function is in the tree 
    to prioritize one turn win moves.
    """
    # Update level
    level += 1
    # Return utility if terminal board or 'utility * 2' if it is a one turn win move
    if terminal(board):
        util = utility(board)
        if level == 1:
            return util * 2
        return util
    # Initialize starting value (-infinity)
    value = -3
    # Loop through actions and find max value
    for action in actions(board):
        value = max(value, minValue(result(board, action), alpha, beta, level))
        alpha = max(alpha, value)
        if alpha >= beta or value == 1:
            return value
    return value


def minValue(board, alpha, beta, level):
    """
    Returns min value of a board.
    'level' keeps track of how deep the function is in the tree 
    to prioritize one turn win moves.
    """
    # Update level
    level += 1
    # Return utility if terminal board or 'utility * 2' if it is a one turn win move
    if terminal(board):
        util = utility(board)
        if level == 1:
            return util * 2
        return util
    # Initialize starting value (infinity)
    value = 3
    # Loop through actions and find min value
    for action in actions(board):
        value = min(value, maxValue(result(board, action), alpha, beta, level))
        beta = max(beta, value)
        if beta <= alpha or value == -1:
            return value
    return value