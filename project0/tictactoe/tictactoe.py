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
    for col in boardFlipped:
        Xcount.add(col.count("X"))
        Ocount.add(col.count("O"))
    
    # Check diagonals
    diagonal1 = [board[i][i] for i in range(3)]
    Xcount.add(diagonal1.count("X"))
    Ocount.add(diagonal1.count("O"))
    diagonal2 = [board[i][2 - i] for i in range(3)]
    Xcount.add(diagonal2.count("X"))
    Ocount.add(diagonal2.count("O"))

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
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
