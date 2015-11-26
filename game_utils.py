from piece_utils import *

# Variables and functions in this file are meant to be globally accessible and
#  should not be modified.

# The total number of rows on the board.
ROWS = 20
# The total number of columns on the board.
COLS = 20
# The pieces available to be played as a dictionary with keys as piece names
#  and values being a list of possible geometries, each of which is a 2D array
#  of boolean values, true if there is a cell, false otherwise.
PIECES = importGeometries('pieces.txt')

# Determines whether the given row, column coordinates are on the board.
def isOnBoard(row, col):
    if row < 0 or col < 0:
        return False
    if row >= ROWS or col >= COLS:
        return False
    return True

# Determines whether the given row, column coordinates are the corner of the
#  board belonging to the given player.
def isCornerTile(row, col, player):
    if player == 1:
        return row == 0 and col == 0
    if player == 2:
        return row == 0 and col == COLS-1
    if player == 3:
        return row == ROWS-1 and col == COLS-1
    if player == 4:
        return row == ROWS-1 and col == 0
    return False

# Gets the total number of tiles which can be placed by a player in the game,
#  i.e. the number of cells in all the pieces.
def getTotalCells():
    cells = 0
    for piece in PIECES:
        geometry = PIECES[piece][0]
        for row in range(len(geometry)):
            for col in range(len(geometry[row])):
                if geometry[row][col]:
                    cells += 1
    return cells

# Converts a grid (i.e. the board or a piece geometry) to a human-readable
#  string.
# Note that this string may be multiple lines long.
def gridToString(grid):
    s = ''

    if not grid:
        return s

    for i in range(len(grid[0]) + 2):
        s += '-'
    s += '\n'

    for i in range(len(grid)):
        s += '|'
        for j in range(len(grid[i])):
            if not val:
                s += ' '
            elif isinstance(val, bool):
                s += 'X'
            else s += str(val)
        s += '|\n'

    for i in range(len(grid[0]) + 2):
        s += '-'
    s += '\n'

    return s
