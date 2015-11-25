from game_utils import *

class Move:
    def __init__(self, piece, geometry, row, col):
        try:
            geometries = PIECES[piece]
            if 0 > geometry or geometry >= len(geometries):
                raise ValueError
            if not isOnBoard(row, col):
                raise ValueError

            self._piece = piece
            self._geometry = geometry
            self._row = row
            self._col = col
        except KeyError:
            raise ValueError

    @property
    def piece(self):
        return self._piece

    @property
    def geometry(self):
        return self._geometry

    @property
    def row(self):
        return self._row

    @property
    def col(self):
        return self._col

    def isLegal(self, state):
        return True # TODO

    def __str__(self):
        return self.piece
