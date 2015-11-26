from game_state import *
from move import *
from game_utils import *
import random

def getMove(state, player):

    print("Craig's turn!")

    print(state)

    print(player)

    mymove = None

    if state.turn < 5:          # this is my first turn
      if player == 1:
        oksquares = [(0,0)]
        mymove = Move("square", 0, oksquares[0][0], oksquares[0][0])
      elif player == 2:
        oksquares = [(0,COLS-1)]
#        mymove = Move("square", 0, oksquares[0][0], oksquares[0][0]-1)
      elif player == 3:
        oksquares = [(ROWS-1,COLS-1)]
#        mymove = Move("square", 0, oksquares[0][0]-1, oksquares[0][0]-1)
      else:
        oksquares = [(ROWS-1,0)]
#        mymove = Move("square", 0, oksquares[0][0]-1, oksquares[0][0])

    else:
      oksquares = []

    okmoves = []

    for row in range(0,ROWS):
      for col in range(0,COLS):
        for piece in state.piecesLeft[player]:
          for geom in range(0,len(PIECES[piece])):
            newstate = state.clone()
            move = Move(piece,geom,row,col)
            try:
              newstate.applyMove(move, player)
              okmoves.append(move)
#              print(str(move))
            except:
              b = 1

    print("Found "+str(len(okmoves))+" legal moves")

    if len(okmoves) > 0:
      r = random.randint(0,len(okmoves)-1)
      mymove = okmoves[r]
    else:
      mymove = None

    return mymove
