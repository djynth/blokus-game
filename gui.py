import sys
from game_utils import *
from move import Move

CELL_SIZE = 20
CELL_PADDING = 2

BLANK = (150, 150, 150)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

BOARD_COLOR = {
    0: BLANK,
    1: BLUE,
    2: YELLOW,
    3: RED,
    4: GREEN
}

class GuiBoard:
    # box is a list of [x, y, width, height]
    def __init__(self, box, screen, board):
        self._box = box
        self._screen = screen

        self.loadBoard(board)

    def loadBoard(self, board):
        self._colorGrid = []
        for i, row in enumerate(board):
            self._colorGrid.append([])
            for cell in row:
                color = BLANK
                if cell in BOARD_COLOR:
                    color = BOARD_COLOR[cell]
                self._colorGrid[i].append(color)

    def boardCoordsToScreen(self, boardCoords):
        return (boardCoords[0] + self._box[0], boardCoords[1] + self._box[1])

    def screenCoordsToBoard(self, screenCoords):
        return (screenCoords[0] - self._box[0], screenCoords[1] - self._box[1])

    def draw(self):
        import pygame

        for i, colorGridRow in enumerate(self._colorGrid):
            for j, cellColor in enumerate(colorGridRow):
                # 2px padding
                y = CELL_SIZE * i + CELL_PADDING
                x = CELL_SIZE * j + CELL_PADDING

                screenX, screenY = self.boardCoordsToScreen((x, y))

                pygame.draw.rect(self._screen,
                    cellColor,
                    [
                        screenX,
                        screenY,
                        CELL_SIZE - CELL_PADDING * 2,
                        CELL_SIZE - CELL_PADDING * 2
                    ])

    # return (row, col) tuple
    def getGridLocation(self, screenCoords):
        boardCoords = self.screenCoordsToBoard(screenCoords)
        col = boardCoords[0] // CELL_SIZE
        row = boardCoords[1] // CELL_SIZE
        return (row, col)

    # location is a (row, col) tuple
    def overrideCellColor(self, location):
        pass

    def clearOverrideColors(self):
        pass

class GuiPieceChooser:
    def __init__(self, box, screen, player=1, pieces=[]):
        self._box = box
        self._screen = screen
        self._player = player
        self._pieces = pieces

        # Room for even the biggest piece
        self.PIECE_PADDING = 10
        self.PIECE_SIZE = (CELL_SIZE * 5) + self.PIECE_PADDING
        self.PIECES_PER_COLUMN = 4

    # TODO(azirbel): Duplicated
    def chooserCoordsToScreen(self, chooserCoords):
        return (chooserCoords[0] + self._box[0], chooserCoords[1] + self._box[1])

    # TODO(azirbel): Duplicated
    def screenCoordsToChooser(self, screenCoords):
        return (screenCoords[0] - self._box[0], screenCoords[1] - self._box[1])

    # TODO(azirbel): Just set the props directly
    def setPieces(self, pieces):
        self._pieces = pieces

    def setPlayer(self, player):
        self._player = player

    def draw(self):
        import pygame

        # Clear the board
        pygame.draw.rect(self._screen, (200, 200, 200), self._box)

        for pieceNum, piece in enumerate(self._pieces):
            pieceRow = pieceNum // self.PIECES_PER_COLUMN
            pieceCol = pieceNum % self.PIECES_PER_COLUMN

            chooserPieceCoords = (pieceRow * self.PIECE_SIZE,
                pieceCol * self.PIECE_SIZE)
            screenPieceCoords = self.chooserCoordsToScreen(chooserPieceCoords)

            screenPieceBox = [
                screenPieceCoords[0],
                screenPieceCoords[1],
                self.PIECE_SIZE,
                self.PIECE_SIZE
            ]

            geometry = PIECES[piece][0]
            fullGeometry = []
            for i in range(5):
                row = []
                for j in range(5):
                    if len(geometry) > i and len(geometry[i]) > j and geometry[i][j]:
                        row.append(self._player)
                    else:
                        row.append(0)
                fullGeometry.append(row)
            pieceBoard = GuiBoard(screenPieceBox, self._screen, fullGeometry)
            pieceBoard.draw()

    # clickCoords must be relative to the chooser's box
    def getPieceFromCoords(self, screenCoords):
        chooserCoords = self.screenCoordsToChooser(screenCoords)
        col = chooserCoords[1] // self.PIECE_SIZE
        row = chooserCoords[0] // self.PIECE_SIZE
        pieceNum = row * self.PIECES_PER_COLUMN + col
        if len(self._pieces) <= pieceNum:
            return None
        return self._pieces[pieceNum]

class Gui:
    def __init__(self, state):
        import pygame

        self._state = state

        pygame.init()

        self.GUI_BOARD_BOX = [50, 50, 400, 400]
        self.GUI_PIECE_CHOOSER_BOX = [500, 50, 650, 430]
        self._screen = pygame.display.set_mode((1200, 550))
        self._screen.fill((200, 200, 200))

        self.guiBoard = \
            GuiBoard(self.GUI_BOARD_BOX, self._screen, state.board)
        self.guiPieceChooserBox = \
            GuiPieceChooser(self.GUI_PIECE_CHOOSER_BOX, self._screen)

    def refresh(self):
        import pygame

        self.guiBoard.loadBoard(self._state.board)
        self.guiBoard.draw()
        self.guiPieceChooserBox.draw()
        pygame.display.flip()

    def getMoveForPlayer(self, player, pieces):
        import pygame

        self.guiPieceChooserBox.setPlayer(player)
        self.guiPieceChooserBox.setPieces(pieces)

        selectedPiece = None

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect(self.GUI_BOARD_BOX).collidepoint(event.pos):
                        if selectedPiece:
                            location = self.guiBoard.getGridLocation(event.pos)
                            return Move(selectedPiece, 0, location[0], location[1])
                        else:
                            return None
                    else:
                        selectedPiece = self.guiPieceChooserBox.getPieceFromCoords(event.pos)
            self.refresh()

    def _drawBoard(self):
        import pygame

