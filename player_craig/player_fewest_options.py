from game_state import *
from move import *
from game_utils import *
from move_utils import *
from player_craig.craig_utils import *
import random
import time

def getMove(state, player):

    oksquares = getLegalSquares(state,player)

    #print("  > Found "+str(len(oksquares))+" OK squares to occupy")

    okmovesandsquares = getLegalMovesAndSquares(state,player,oksquares)

    #print("  > Found "+str(len(okmovesandsquares))+" legal moves")

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

      biggestmoves = []
      for option in okmovesandsquares:
        if option['numcells'] == biggestcells and option['numspotstoplace'] == fewestspots:
          biggestmoves.append(option['move'])
#          print("Time to play " + option['piece'] + " which has " + str(option['numspotstoplace']) + " places to go and size " + str(option['numcells']))

      if len(biggestmoves) == 0:
        for option in okmovesandsquares:
          if option['numspotstoplace'] == fewestspots:
            biggestmoves.append(option['move'])

      r = random.randint(0,len(biggestmoves)-1)
      mymove = biggestmoves[r]

    return mymove
