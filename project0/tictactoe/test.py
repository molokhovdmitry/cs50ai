from tictactoe import player, actions, result, winner, terminal, utility, minimax

EMPTY = None

board = [["O", "X", "X"],
         [EMPTY, "X", "O"],
         [EMPTY, "O", "X"]]

actions = actions(board)
utils = {}
for action in actions:
    utils[action] = -2

print(*result(board, minimax(board)), sep='\n')