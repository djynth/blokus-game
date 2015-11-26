from game_state import *
from move import *
from game_utils import *
import random

def getMove(state, player):

    print(state)
    print(player)

    if state.turn < 5:          # this is my first turn
      if player == 1:
        oksquares = [(0,0)]
      elif player == 2:
        oksquares = [(0,COLS-1)]
      elif player == 3:
        oksquares = [(ROWS-1,COLS-1)]
      else:
        oksquares = [(ROWS-1,0)]

    else:
      oksquares = []
      board = state.board
      for row in range(1,ROWS-1):
        for col in range(1,COLS-1):
          if board[row][col] == 0:
            if board[row-1][col-1] == player or board[row-1][col+1] == player or board[row+1][col-1] == player or board[row+1][col+1] == player:
              if board[row-1][col] != player and board[row+1][col] != player and board[row][col-1] != player and board[row][col+1] != player:
                oksquares.append((row,col))

      row = 0
      for col in range(1,COLS-1):
        if board[row][col] == 0:
          if board[row+1][col-1] == player or board[row+1][col+1] == player:
            if board[row+1][col] != player:
              oksquares.append((row,col))

      row = ROWS-1
      for col in range(1,COLS-1):
        if board[row][col] == 0:
          if board[row-1][col-1] == player or board[row-1][col+1] == player:
            if board[row-1][col] != player:
              oksquares.append((row,col))

      col = 0
      for row in range(1,ROWS-1):
        if board[row][col] == 0:
          if board[row-1][col+1] == player or board[row+1][col+1] == player:
            if board[row][col+1] != player:
              oksquares.append((row,col))

      col = COLS-1
      for row in range(1,ROWS-1):
        if board[row][col] == 0:
          if board[row-1][col-1] == player or board[row+1][col-1] == player:
            if board[row][col-1] != player:
              oksquares.append((row,col))

      if board[0][0] == 0 and board[1][1] == player:
        oksquares.append((0,0))

      if board[0][COLS-1] == 0 and board[1][COLS-2] == player:
        oksquares.append((0,COLS-1))

      if board[ROWS-1][0] == 0 and board[ROWS-2][1] == player:
        oksquares.append((ROWS-1,0))

      if board[ROWS-1][COLS-1] == 0 and board[ROWS-2][COLS-2] == player:
        oksquares.append((ROWS-1,COLS-1))


    print("Found "+str(len(oksquares))+" OK squares to occupy")

    okmoves = []

    for oksquare in oksquares:
      for piece in state.piecesLeft[player]:
        for geom in range(0,len(PIECES[piece])):
          p = PIECES[piece][geom]                 # the actual pattern for this piece
          for a in range(0,len(p)):               # go through rows of this piece and geometry
            for b in range(0,len(p[0])):          # go through columns of this piece and geometry
              if p[a][b]:                         # if this piece has an X at this location
                row = oksquare[0]-a               # what row and column this piece could be put at
                col = oksquare[1]-b
                if row >= 0 and row < ROWS and col >= 0 and col < COLS:
                  newstate = state.clone()
                  move = Move(piece,geom,row,col)

                  try:
                    newstate.applyMove(move, player)
                    okmoves.append(move)
                  except:
                    c = 1

    print("Found "+str(len(okmoves))+" legal moves")

    if len(okmoves) > 0:
      r = random.randint(0,len(okmoves)-1)
      mymove = okmoves[r]
    else:
      mymove = None

    return mymove
