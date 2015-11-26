from piece_utils import *

ROWS = 20
COLS = 20
PIECES = importGeometries('pieces.txt')

class InvalidMove(Exception):
    pass

def isOnBoard(row, col):
    if row < 0 or col < 0:
        return False
    if row >= ROWS or col >= COLS:
        return False
    return True

def getTotalCells():
    cells = 0
    for piece in PIECES:
        geometry = piece[0]
        for row in range(len(geometry)):
            for col in range(len(geometry[row])):
                if geometry[row][col]:
                    cells += 1
    return cells

def defaultToString(val):
    if not val:
        return ' '
    if isInstance(val, bool):
        return 'X'
    return str(val)

def gridToString(grid, cellToString=defaultToString):
    s = ''

    if not grid:
        return s

    for i in range(len(grid[0]) + 2):
        s += '-'
    s += '\n'

    for i in range(len(grid)):
        s += '|'
        for j in range(len(grid[i])):
            s += cellToString(grid[i][j])
        s += '|\n'

    for i in range(len(grid[0]) + 2):
        s += '-'
    s += '\n'

    return s
