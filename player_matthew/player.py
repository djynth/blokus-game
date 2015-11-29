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
			
	if state.turn < 9:
		if player ==1:
			move = Move('plus', 0, 3, 1)
			return move
		if player ==2:
			move = Move('plus', 0, 3, 16)
			return move
		if player ==3:
			move = Move('plus', 0, 16, 14)
			return move
		if player ==4:
			move = Move('plus', 0, 16, 3)
			return move

	if state.turn < 13:
		if player == 1:
			move = Move('wubba', 0, 5, 4)
			return move
		if player == 2:
			move = Move('wubba', 1, 5, 13)
			return move
		if player == 3:
			move = Move('wubba', 0, 13, 12)
			return move
		if player == 4:
			move = Move('wubba', 1, 13, 5)
			return move


	legalMoves = getLegalMoves(state, player)


	bestMove = None
	bestScore = -1

	for move in legalMoves:
		state.applyMove(move, player)
		moveScore = len(getLegalMoves(state, player))

		moveScore += move.getNumCells() * 1000

		if moveScore > bestScore:
			bestScore = moveScore
			bestMove = move
		state.undoMove(move, player)

	return bestMove
	
