from tictactoe import player, actions, result, winner, terminal, utility, minimax

EMPTY = None

board = [[EMPTY, "X", "O"],
         ["O", "X", EMPTY],
         ["X", EMPTY, "O"]]

actions = actions(board)
utils = {}
for action in actions:
    utils[action] = -2

print(minimax(board))
#print(*result(board, minimax(board)), sep='\n')