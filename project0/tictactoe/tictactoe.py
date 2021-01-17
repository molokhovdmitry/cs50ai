"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

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

    # Initialize dictionary that contains minmax value for every action
    minmaxes = {}

    # If player is "X"
    if player(board) == "X":
        # Fill minmaxes dictionary
        for action in actions(board):
            minmaxes[action] = minValue(result(board, action))
        """
        Choose action with max value.
        How to get a key with max/min value from a dictionary: 
        https://stackoverflow.com/questions/18296755/python-max-function-using-key-and-lambda-expression
        """
        optimalAction = max(minmaxes, key=lambda key:minmaxes[key])
    # If player is "O"
    else:
        # Fill minmaxes dictionary
        for action in actions(board):
            minmaxes[action] = maxValue(result(board, action))
        # Choose action with min value
        optimalAction = min(minmaxes, key=lambda key:minmaxes[key])
    
    # Return optimal action
    return optimalAction


def maxValue(board):
    """
    Returns max value of a board.
    """
    # Return utility if terminal board
    if terminal(board):
        return utility(board)
    # Initialize starting value (-infinity)
    value = -2
    # Loop through actions and find max value
    for action in actions(board):
        value = max(value, minValue(result(board, action)))
    return value


def minValue(board):
    """
    Returns min value of a board.
    """
    # Return utility if terminal board
    if terminal(board):
        return utility(board)
    # Initialize starting value (infinity)
    value = 2
    # Loop through actions and find min value
    for action in actions(board):
        value = min(value, maxValue(result(board, action)))
    return value