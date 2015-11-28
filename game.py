from move import Move
from game_state import GameState
from game_utils import *
from gui import Gui
import argparse
from player_gui.player import GuiPlayer
import player_matthew.player as player1 #top left
import player_matthew.player as player2 #top right
import player_matthew.player as player3 #bottom right
import player_matthew.player as player4 #bottom left
import sys
import time

parser = argparse.ArgumentParser(description='Run the blokus game.')
parser.add_argument('--gui',
    dest='gui',
    action='store_true',
    help='use the pygame gui')
args = parser.parse_args()

passes = 0
state = GameState()

if args.gui:
    gui = Gui(state)
    # Upgrade console players to GUI players in GUI mode
    if player1.__name__ == 'player_console.player':
        player1 = GuiPlayer(gui)
    if player2.__name__ == 'player_console.player':
        player2 = GuiPlayer(gui)
    if player3.__name__ == 'player_console.player':
        player3 = GuiPlayer(gui)
    if player4.__name__ == 'player_console.player':
        player4 = GuiPlayer(gui)

t0 = time.clock()

while passes < 4:
    player = state.getPlayer()

    if args.gui:
        gui.refresh(True)

    print('Player ' + str(player) + '\'s turn!')
    if player == 1:
        move = player1.getMove(state.clone(), player)
    elif player == 2:
        move = player2.getMove(state.clone(), player)
    elif player == 3:
        move = player3.getMove(state.clone(), player)
    elif player == 4:
        move = player4.getMove(state.clone(), player)

    if move == None:
        passes += 1
    else:
        passes = 0

    time.sleep(0) #increase to increase time between moves
    if state.applyMove(move, player):
        print('  > Move made: ' + str(move))
    else:
        print('  > Invalid move!')

print(state)
totalCells = getTotalCells()
winners = []
minCells = ROWS*COLS
for player in [1,2,3,4]:
    remaining = totalCells - state.getCellsOnBoard(player)
    if remaining < minCells:
        winners = [player]
        minCells = remaining
    elif remaining == minCells:
        winners.append(player)
    print('Player ' + str(player) + ' has ' + str(remaining) + ' cells remaining.')

print()
if len(winners) == 1:
    print('Player ' + str(winners[0]) + ' wins!')
elif len(winners) > 1:
    print('Tie between ' + str(winners) + '!')

print("Game took " + str(time.clock() - t0) + " seconds")

if args.gui:
    gui.waitForQuit()
else:
    time.sleep(100)
