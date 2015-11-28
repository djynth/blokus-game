from game_state import *
from move import *
from game_utils import *
from move_utils import *
import random

print('Matthew wins!')

def getMove(state, player):
    
	if state.turn < 5:
		if player == 1:
			move = Move('bump-on-a-log', 1, 0, 0) #this defines the variable move
			return move #move is then sent back to game.py
		if player == 2:
			move = Move('bump-on-a-log', 5, 0, 18) #see line 9
			return move #see line 10
		if player == 3:
			move = Move('bump-on-a-log', 4, 18, 16)
			return move
		if player == 4:
			move = Move('bump-on-a-log', 2, 18, 0)
			return move

	legalMoves = getLegalMoves(state, player)
	
	if len(legalMoves) > 0:
		return legalMoves[random.randint(0,len(legalMoves)-1)]
	else:
		return None

