from tictactoe import player, actions, result, winner

EMPTY = None

print(winner([["X", "X", "O"],
              ["O", "O", EMPTY],
              ["O", "X", "X"]]))