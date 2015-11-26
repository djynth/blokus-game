from game_state import *
from move import *
from game_utils import *

class GuiPlayer:
    def __init__(self, gui):
        self.gui = gui

    def getMove(self, state, player):
        return self.gui.getMoveForPlayer(player, state.piecesLeft[player])
