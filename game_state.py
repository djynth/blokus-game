from game_utils import *

# Represents the state of the game at a single turn.
class GameState:
    # Creates a new GameState from the given parameters.
    # This constructor checks that the turn is strictly positive and raises a
    #  ValueError if it is not.
    # Accessed via GameState(_,_,_), not state.__init__(_,_,_).
    # @param turn       int               the current turn (must be positive)
    # @param board      int [][]          the board where each cell is the
    #                                     player who has a piece there, or 0
    #                                     for empty
    # @param piecesLeft {int -> string[]} the pieces each player has not yet
    #                                     played, as a dictionary from the
    #                                     player number to a list of the names
    #                                     of the remaining pieces
    # @param moves      Move []           the Moves which have been made, in
    #                                     order
    # @return GameState
    def __init__(self, turn=1, board=None, piecesLeft=None, moves=[]):
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

        # possibly should check that each move in the sequence is legal given
        #  the previous ones, and that they have all indeed been played in the
        #  board
        self._moves = []
        for move in moves:
            self._moves.append(move.clone())

    # The current turn of the game, starting from 1 for the first turn.
    # @return int
    @property
    def turn(self):
        return self._turn

    # The current board as a 2D array of integers, with 0 if no tile has been
    #  placed at a given location, or the player number (1-4) of the tile if one
    #  has been placed.
    # @return int [][]
    @property
    def board(self):
        return self._board

    # Gets the pieces not yet placed by all the players as a dictionary with
    #  keys being the player numbers (1-4) and values being the list of the
    #  names of the pieces left for that player.
    # @return {int -> string[]}
    @property
    def piecesLeft(self):
        return self._piecesLeft

    # The moves which have been played in this game, from the beginning in orer.
    # @return Move []
    @property
    def moves(self):
        return self._moves

    # Gets the player whose turn it currently is as their number, 1-4.
    # @return int
    def getPlayer(self):
        return ((self.turn - 1) % 4) + 1

    # Gets the number of tiles placed by the given player currently on the
    #  board.
    # @param player int the player whose cells should be counted
    # @return int
    def getCellsOnBoard(self, player):
        cells = 0
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] == player:
                    cells += 1
        return cells

    # Determines whether the given Move by the given player is legal, i.e. is on
    #  the board, is not edge-on with another piece, is connected via a corner,
    #  etc.
    # @param move   Move the Move to check
    # @Param player int  the player who would be making the Move
    # @return Boolean
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
                            onBoard = isOnBoard(row, col)
                            if edgeX == 0 and edgeY == 0:
                                if not onBoard or self.board[row][col] != 0:
                                    return False
                                if isCornerTile(row, col, player):
                                    onCorner = True
                            elif edgeX == 0 or edgeY == 0:
                                if onBoard and self.board[row][col] == player:
                                    return False
                            else:
                                if onBoard and self.board[row][col] == player:
                                    onCorner = True
        return onCorner

    # Checks whether the given Move has been played by the given player at any
    #  time in the past.
    # @param move   Move the Move to check
    # @param player int  the player to check
    # @return Boolean
    def hasMoveBeenPlayed(self, move, player):
        geometry = move.getGeometry()
        for i in range(len(geometry)):
            for j in range(len(geometry[i])):
                if geometry[i][j] and self.board[move.row + i][move.col + j] != player:
                    return False
        return True

    # Exectures a Move by the given player on this game.
    # This game itself will be updated to reflect the Move.
    # @param move   Move the Move to play, or None to pass
    # @param player int  the player who should play the Move
    # @return Boolean true if the move was player, false if it was not
    def applyMove(self, move, player):
        self._turn += 1

        if move != None:
            if not self.isMoveValid(move, player):
                self._moves.append(None)
                return False

            geometry = move.getGeometry()
            for i in range(len(geometry)):
                for j in range(len(geometry[i])):
                    if geometry[i][j]:
                        self._board[move.row + i][move.col + j] = player

            self._piecesLeft[player].remove(move.piece)

        self._moves.append(move)
        return True

    # Undoes a move by the given player (no matter of how long ago it was
    #  played).
    # @param move   Move the Move to be undone
    # @param player int  the player whose Move should be reversed
    # @return Boolean whether the Move was successfully undone (false if it had
    #                 never occurred and so could not be reversed)
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
        self._moves.remove(move)
        return True

    # Undoes the most recently played Move.
    # @return Boolean true if there was a move to undo, false otherwise
    def undoLastMove(self):
        if len(self._moves):
            return undoMove(self._moves.pop(), ((self.turn - 2) % 4) + 1)
        return False

    # Creates a new GameState exactly mirroring this one which can be modified
    #  without affecting the current one.
    # @return GameState
    def clone(self):
        return GameState(self.turn, self.board, self.piecesLeft, self.moves)

    # Converts this GameState into a human-readable string.
    # Accessed via str(state), not state.__str__().
    # @return string
    def __str__(self):
        s = 'Turn ' + str(self.turn) + '\n'
        s += gridToString(self.board)
        s += 'Pieces Remaining:\n'
        for player in [1,2,3,4]:
            s += '   Player ' + str(player) + ': '
            s += str(self.piecesLeft[player]) + '\n'
        return s
