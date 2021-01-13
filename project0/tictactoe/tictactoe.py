"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class QueueFrontier():
    def __init__(self):
        self.frontier = []
    
    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node


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
    1. Check for terminal board.
    2. Initialize frontier with a starting node.
    3. Loop:
        - check if frontier is empty (every action explored)
            if it is empty return action with max utility
        - 
        
    """
    if terminal(board):
        return None

    # Starting node
    start = Node(state=board, parent=None, action=None)

    # Initialize frontier with a starting node
    frontier = QueueFrontier()
    frontier.add(start)

    # Initialize utils dictionary that contains utility value for every action
    utils = {}

    # Loop until action is found
    while True:

        # If nothing left in frontier, return action
        if frontier.empty():
            # Get action with max/min utility
            if player(board) == "X":
                action = max(utils, key=lambda key: utils[key])
            else:
                action = min(utils, key=lambda key: utils[key])
            return action

        # Remove node
        node = frontier.remove()
        
        # Add actions to frontier
        for action in actions(board):
            