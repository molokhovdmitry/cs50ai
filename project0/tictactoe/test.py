from project0.tictactoe.tictactoe import player, actions, result, winner, terminal, utility, minimax, maxValue, minValue
import operator

EMPTY = None

board = [["X", EMPTY, EMPTY],
         ["O", "O", EMPTY],
         ["X", EMPTY, "X"]]

print(maxValue([["X", EMPTY, EMPTY],
                ["O", "O", "O"],
                ["X", EMPTY, "X"]], -3, 3, 1))

print(maxValue([["X", EMPTY, EMPTY],
                ["O", "O", EMPTY],
                ["X", EMPTY, "X"]], -3, 3, 1))

print(minimax(board))