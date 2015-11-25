ROWS = 20
COLS = 20
PIECES = {
    'singleton' : [
        [[True]]
    ],
}

class InvalidMove(Exception):
    pass

def isOnBoard(row, col):
    if row < 0 or col < 0:
        return False
    if row >= ROWS or col >= COLS:
        return False
    return True
