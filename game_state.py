from game_utils import *

class GameState:
    def __init__(self, turn = 1, board = None, piecesLeft = None):
        if turn < 1:
            raise ValueError
        self._turn = turn

        self._board = [[0 for x in range(COLS)] for x in range(ROWS)]
        if board:
            for row in range(ROWS):
                for col in range(COLS):
                    if 0 > board[row][col] or board[row][col] > 4:
                        raise ValueError
                    self._board[row][col] = board[row][col]

        self._piecesLeft = {}
        if piecesLeft:
            for player in [1,2,3,4]:
                self._piecesLeft[player] = list(piecesLeft[player])
        else:
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

    def getPlayer(self):
        return ((self.turn - 1) % 4) + 1

    def getCellsOnBoard(self, player):
        cells = 0
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] == player:
                    cells += 1
        return cells

    def isMoveValid(self, move, player):
        if not move.piece in self._piecesLeft[player]:
            return False

        geometry = move.getGeometry()

        onCorner = False
        for i in range(len(geometry)):
            for j in range(len(geometry[i])):
                if geometry[i][j]:
                    for edgeX in [-1, 0, 1]:
                        for edgeY in [-1, 0, 1]:
                            row = move.row + i + edgeY
                            col = move.col + j + edgeX
                            if edgeX == 0 and edgeY == 0:
                                if not isOnBoard(row, col) or self.board[row][col] != 0:
                                    return False
                                if isCornerTile(row, col, player):
                                    onCorner = True
                            elif edgeX == 0 or edgeY == 0:
                                if isOnBoard(row, col) and self.board[row][col] == player:
                                    return False
                            else:
                                if isOnBoard(row, col) and self.board[row][col] == player:
                                    onCorner = True
        if not onCorner:
            return False
        return True

    def hasMoveBeenPlayed(self, move, player):
        geometry = move.getGeometry()
        for i in range(len(geometry)):
            for j in range(len(geometry[i])):
                if geometry[i][j] and self.board[move.row + i][move.col + j] != player:
                    return False
        return True

    def applyMove(self, move, player):
        self._turn += 1

        if move == None:
            return True

        if not self.isMoveValid(move, player):
            return False

        geometry = move.getGeometry()
        for i in range(len(geometry)):
            for j in range(len(geometry[i])):
                if geometry[i][j]:
                    self._board[move.row + i][move.col + j] = player

        self._piecesLeft[player].remove(move.piece)
        return True

    def undoMove(self, move, player):
        self._turn -= 1

        if move == None:
            return True

        if not self.hasMoveBeenPlayed(move, player):
            return False

        geometry = move.getGeometry()
        for i in range(len(geometry)):
            for j in range(len(geometry[i])):
                if geometry[i][j]:
                    self._board[move.row + i][move.col + j] = 0

        self._piecesLeft[player].append(move.piece)
        return True

    def clone(self):
        return GameState(self.turn, self.board, self.piecesLeft)

    def __str__(self):
        s = 'Turn ' + str(self.turn) + '\n'
        s += gridToString(self.board)
        s += 'Pieces Remaining:\n'
        for player in [1,2,3,4]:
            s += '   Player ' + str(player) + ': ' + str(self.piecesLeft[player]) + '\n'
        return s
