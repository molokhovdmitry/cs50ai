from tictactoe import player, actions, result, winner, terminal, utility, minimax, maxValue, minValue
import operator

EMPTY = None

board = [["X", EMPTY, EMPTY],
         ["O", "O", EMPTY],
         ["X", EMPTY, "X"]]

print(maxValue([["X", EMPTY, EMPTY],
                ["O", "O", EMPTY],
                ["X", "O", "X"]], -2, 2))

