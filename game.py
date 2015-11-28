import argparse
import player_matthew.player as player1 #top left
import player_matthew.player as player2 #top right
import player_matthew.player as player3 #bottom right
import player_matthew.player as player4 #bottom left
import game_runner as GameRunner
from game_logger import Logger

parser = argparse.ArgumentParser(description='Run the blokus game.')
parser.add_argument('--gui',
    dest='gui',
    action='store_true',
    help='use the pygame gui')
parser.add_argument('--runs', default=1, type=int,
    help='if set to more than 1, suppress output and run many games')
args = parser.parse_args()

if args.runs == 1:
    logger = Logger(3)
    players = [player1, player2, player3, player4]
    GameRunner.runGame(players, logger, False, args.gui)
else:
    logger = Logger(2)
    players = [player1, player2, player3, player4]
    winCount = [0, 0, 0, 0]
    for i in range(args.runs):
        print('Playing game ' + str(i + 1) + ' of ' + str(args.runs))
        winners = GameRunner.runGame(players, logger, False, args.gui)
        for winner in winners:
            winCount[winner - 1] += 1
        print('Winners: ' + str(winCount))

    for playerNum, count in enumerate(winCount):
        print('Player ' + str(playerNum + 1) + ' won ' + str(count) + ' times.')
