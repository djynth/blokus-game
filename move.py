from game_utils import *

class Move:
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

    def __str__(self):
        try:
            return 'Placeholder real move'
        except KeyError:
            raise ValueError

    @property
    def piece(self):
        return self._piece

    @property
    def numGeometry(self):
        return self._numGeometry

    @property
    def row(self):
        return self._row

    @property
    def col(self):
        return self._col

    def getGeometry(self):
        return PIECES[self.piece][self.numGeometry]

    def __str__(self):
        return self.piece + ' [' + self.numGeometry + '] at (' + self.row + ',' + self.col + ')'
