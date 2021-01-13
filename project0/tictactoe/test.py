from tictactoe import player, actions, result, winner, terminal, utility

EMPTY = None

board = [["O", EMPTY, "X"],
         ["X", "O", "O"],
         ["X", EMPTY, EMPTY]]

actions = actions(board)
utils = {}
for action in actions:
    utils[action] = -2
print(utils)

utils[(2, 1)] = 1
print(utils)

print(max(utils, key=lambda key: utils[key]))