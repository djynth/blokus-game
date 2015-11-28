from game_state import *
from move import *
from game_utils import *
from move_utils import *
import random

def getMove(state, player):

    oksquares = getLegalSquares(state,player)

    #print("  > Found "+str(len(oksquares))+" OK squares to occupy")

    okmoves = getLegalMoves(state,player,oksquares)

    #print("  > Found "+str(len(okmoves))+" legal moves")

    mymove = None

    if len(okmoves) > 0:
      biggestsize = 0
      for move in okmoves:
        cells = move.getNumCells()
        if cells > biggestsize:
          biggestsize = cells
      biggestmoves = []
      for move in okmoves:
        cells = move.getNumCells()
        if cells == biggestsize:
          biggestmoves.append(move)
      r = random.randint(0,len(biggestmoves)-1)
      mymove = biggestmoves[r]


    return mymove
