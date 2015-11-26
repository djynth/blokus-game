from game_utils import *

GUI_BOARD_PADDING = 50
GUI_CELL_SIZE = 20
GUI_CELL_PADDING = 4

BLANK = (20, 20, 20)
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

class Gui:
    def __init__(self, state):
        # Try to allow playing even if you don't have pygame installed, by
        # doing this late import
        import pygame

        self._state = state

        pygame.init()
        # TODO(azirbel): Assumed ROWS = COLS. Should make that clear
        height = width = (GUI_BOARD_PADDING * 2) + \
            ((GUI_CELL_SIZE + GUI_CELL_PADDING) * ROWS) - \
            GUI_CELL_PADDING
        size = width, height
        self._screen = pygame.display.set_mode(size)
        self._screen.fill((100, 100, 100))

    def update(self):
        import pygame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        self._drawBoard()
        pygame.display.flip()

    def _drawBoard(self):
        import pygame

        for row in range(ROWS):
            for col in range(COLS):
                x = GUI_BOARD_PADDING + \
                    ((GUI_CELL_SIZE + GUI_CELL_PADDING) * row)
                y = GUI_BOARD_PADDING + \
                    ((GUI_CELL_SIZE + GUI_CELL_PADDING) * col)
                pygame.draw.rect(self._screen,
                    BOARD_COLOR[self._state.board[row][col]],
                    [x, y, GUI_CELL_SIZE, GUI_CELL_SIZE])
