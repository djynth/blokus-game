#!/usr/bin/python3

from move import Move
from game_state import GameState
from game_utils import *
import player_dominic.player as player1
import player_random.player as player2
import player_random.player as player3
import player_random.player as player4

passes = 0
state = GameState()
while passes < 4:
    player = state.getPlayer()

    # TODO rotate the board so the player sees themself as top-left
    if player == 1:
        move = player1.getMove(state.clone())
    elif player == 2:
        move = player2.getMove(state.clone())
    elif player == 3:
        move = player3.getMove(state.clone())
    elif player == 4:
        move = player4.getMove(state.clone())

    if move == None:
        passes += 1
    else:
        passes = 0

    print('Player ' + str(player) + ' move:')
    if move:
        print(move)
    else:
        print('Pass')
    print()
    
    try:
        state.applyMove(move, player)
    except InvalidMove:
        print('Invalid move!')
        # TODO what now?

print(state)
# TODO scoring
