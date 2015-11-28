from game_state import *
from move import *
from game_utils import *
from move_utils import *
from player_craig.craig_utils import *
import random
import time
import math

def getMove(state, player):

    if player == 1:
      homecorner = (0,0)
    elif player == 2:
      homecorner = (0,COLS-1)
    elif player == 3:
      homecorner = (ROWS-1,COLS-1)
    else:
      homecorner = (ROWS-1,0)

    oksquares = getLegalSquares(state,player)

    okmovesandsquares = getLegalMovesAndSquares(state,player,oksquares)

#    print("  > Found "+str(len(oksquares))+" OK squares and "+str(len(okmovesandsquares))+" legal moves")

    mymove = None

    if len(okmovesandsquares) > 0:
      biggestcells = 0
      piecesquaredict = {}

      for option in okmovesandsquares:
        cells = option['move'].getNumCells()
        if cells > biggestcells:
          biggestcells = cells

        option['numcells'] = cells

        piece = option['piece']
        square = option['square']

        if piece in piecesquaredict:
          if square not in piecesquaredict[piece]:
            piecesquaredict[piece][square] = 1
        else:
          piecesquaredict[piece] = {}
          piecesquaredict[piece][square] = 1

#        print(str(option['square']) + " covered by " + str(option['move']))

#      print(piecesquaredict)
#      time.sleep(10)

      fewestspots = 1000

      for option in okmovesandsquares:
        piece = option['piece']
        numspotstoplace = len(piecesquaredict[piece])  # record number of distinct places that this piece can be put
        option['numspotstoplace'] = numspotstoplace

        if numspotstoplace < fewestspots:
          fewestspots = numspotstoplace

      bestscore = -1
      for option in okmovesandsquares:
        score = option['numcells'] / option['numspotstoplace']

        option['distancefromcorner'] = max(1,math.sqrt(math.pow(option['square'][0]-homecorner[0],2)+math.pow(option['square'][1]-homecorner[1],2)))
        score *= option['distancefromcorner']

        if 10 > 1:
          state.applyMove(option['move'], player)
          option['squaresafter'] = len(getLegalSquares(state,player))
  #        option['movesafter'] = len(getLegalMoves(state,player))
          state.undoMove(option['move'],player)
          score *= option['squaresafter']

        if 10 > 1:
          state.applyMove(option['move'], player)
          for nextplayer in range(1,5):
            if nextplayer != player:
              score = score / len(getLegalSquares(state,nextplayer))
          state.undoMove(option['move'],player)

        if score > bestscore:
          mymove = option['move']
          bestscore = score

#      print(state)

    return mymove
