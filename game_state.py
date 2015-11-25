from game_utils import *

class GameState:
    def __init__(self):
        self._turn = 1
        self._board = [[0 for x in range(COLS)] for x in range(ROWS)]
        self._piecesLeft = {}
        for player in [1,2,3,4]:
            self._piecesLeft[player] = list(PIECES.keys())

    @property
    def turn(self):
        return self._turn
    
    @property
    def board(self):
        return self._board
    
    @property
    def piecesLeft(self):
        return self._piecesLeft
    
    def applyMove(self, move):
        self._turn += 1

        if move == None:
            return

        if not move.isLegal(self):
            raise InvalidMove
        # TODO apply the move to the board

    def __str__(self):
        return string(self.turn) # TODO
