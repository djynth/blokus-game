from game_utils import PIECES

class Move:
    def __init__(self, piece):
        if piece in PIECES:
            self._piece = piece
        else:
            raise ValueError(piece)

    @property
    def piece(self):
        return self._piece
