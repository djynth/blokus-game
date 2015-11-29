from move import Move
from game_state import GameState
from game_utils import *
from gui import Gui
from player_gui.player import GuiPlayer
import sys
import time

# Returns array of winners (array of player numbers)
def runGame(players, logger, slowMode=False, gui=False):
    passes = 0
    state = GameState()

    if gui:
        gui = Gui(state)
        # Upgrade console players to GUI players in GUI mode
        for idx, player in enumerate(players):
            if player.__name__ == 'player_console.player':
                players[idx] = GuiPlayer(gui)

    player1 = players[0]
    player2 = players[1]
    player3 = players[2]
    player4 = players[3]

    t0 = time.clock()

    while passes < 4:
        player = state.getPlayer()

        if gui:
            gui.refresh(True)

        logger.log('Player ' + str(player) + '\'s turn!')
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

        if state.applyMove(move, player):
            logger.log('  > Move made: ' + str(move))
        else:
            logger.log('  > Invalid move!')

        if slowMode:
            time.sleep(.5)

    logger.log(state)
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
        logger.log('Player ' + str(player) + ' has ' + str(remaining) + ' cells remaining.')

    logger.log('')
    if len(winners) == 1:
        logger.log('Player ' + str(winners[0]) + ' wins!')
    elif len(winners) > 1:
        logger.log('Tie between ' + str(winners) + '!')

    logger.log("Game took " + str(time.clock() - t0) + " seconds")

    if gui:
        gui.waitForQuit()
    elif slowMode:
        time.sleep(5)

    return winners
