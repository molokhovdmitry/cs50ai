from minesweeper import Sentence

height, width, mines = 8, 8, 8

board = []
for i in range(height):
            row = []
            for j in range(width):
                row.append(False)
            board.append(row)

# Add mines
board[2][2] = True
board[7][4] = True

print(*board, sep='\n')

cell = (2, 0)
cells = set()
for i in range(cell[0] - 1, cell[0] + 2):
    for j in range(cell[1] - 1, cell[1] + 2):
        if (i, j) != cell:
            if 0 <= i < height and 0 <= j < width:
                cells.add((i, j))

print(cells)