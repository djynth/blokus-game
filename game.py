#!/usr/bin/python3

from move import Move
from game_state import GameState
from game_utils import *

passes = 0
state = GameState()
while passes < 4:
    player = state.turn % 4
    move = None # TODO get player move
    if move == None:
        passes += 1
    else:
        passes = 0
    
    try:
        state.applyMove(move)
    except InvalidMove:
        print('Invalid move by player ', player)

# TODO scoring
