from game_utils import *

# Defines a single move made on the board.
class Move:
    # Creates a new Move from the given parameters.
    # This constructor checks that the parameters are valid (i.e. the piece name
    #  is an actual piece) and raises a ValueError if they are invalid.
    # Accessed via Move(_,_,_,_), not move.__init__(_,_,_,_).
    def __init__(self, piece, numGeometry, row, col):
        try:
            geometries = PIECES[piece]
            if 0 > numGeometry or numGeometry >= len(geometries):
                raise ValueError
            if not isOnBoard(row, col):
                raise ValueError

            self._piece = piece
            self._numGeometry = numGeometry
            self._row = row
            self._col = col
        except KeyError:
            raise ValueError

    # The name of the piece which was placed.
    @property
    def piece(self):
        return self._piece

    # The index of the geometry (i.e. rotation/flip) of the piece.
    # This is a reference to the list returned by PIECES[self.piece].
    @property
    def numGeometry(self):
        return self._numGeometry

    # The row at which the top-left corner of this Move was played.
    @property
    def row(self):
        return self._row

    # The col at which the top-left corner of this Move was played.
    @property
    def col(self):
        return self._col

    # The geometry of the placed piece as a 2D boolean array (true if a cell is
    #  at that row/column, false otherwise)
    def getGeometry(self):
        return PIECES[self.piece][self.numGeometry]

    # Gets the total number of cells placed by this Move.
    def getNumCells(self):
        p = PIECES[self.piece][0]
        cells = 0
        for i in range(0,len(p)):
            for j in range(0,len(p[0])):
                if p[i][j]:
                    cells += 1
        return cells

    # Converts this Move into a human-readable string.
    # Accessed via str(move), not move.__str__().
    def __str__(self):
        return self.piece + ' [' + str(self.numGeometry) + '] at (' + str(self.row) + ',' + str(self.col) + ')'
