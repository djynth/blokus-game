from game_state import *
from move import *
from game_utils import *

def getLegalSquares(state,player):

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

  return oksquares

# This function returns a list of legal moves for player

def getLegalMoves(state,player,oksquares=None):

  if not oksquares:
    oksquares = getLegalSquares(state,player)

  okmoves = []
  board = state.board

  for oksquare in oksquares:                    # go through all open diagonal squares
    for piece in state.piecesLeft[player]:      # consider each remaining piece
      for geom in range(0,len(PIECES[piece])):  # consider each geometry for this piece
        p = PIECES[piece][geom]                 # the actual pattern for this piece
        height = len(p)                         # height of this geometry for this piece
        width  = len(p[0])                      # width of this geometry for this piece
        for a in range(0,height):               # go through rows of this piece and geometry
          for b in range(0,width):              # go through columns of this piece and geometry
            if p[a][b]:                         # if this piece has a square at this location
              row = oksquare[0]-a               # what row and column this piece could be put at
              col = oksquare[1]-b
              if row >= 0 and row+height <= ROWS and col >= 0 and col+width <= COLS: # whole piece fits on the board
                fits = True                     # start with the idea that this piece fits here
                for i in range(0,height):       # go through all *other* squares in this piece
                  for j in range(0,width):
                    if p[i][j]:                 # if the piece has a square here
                      s = row+i                 # row of this square on the board
                      t = col+j                 # column of this square on the board
                      if board[s][t] != 0:      # something else is already here
                        fits = False
                      elif s > 0 and board[s-1][t] == player: # adjacent piece above
                        fits = False
                      elif s < ROWS-1 and board[s+1][t] == player: # adjacent piece below
                        fits = False
                      elif t > 0 and board[s][t-1] == player: # adjacent piece to the left
                        fits = False
                      elif t < COLS-1 and board[s][t+1] == player: # adjacent piece to the right
                        fits = False
                if fits:
                  move = Move(piece,geom,row,col)
                  okmoves.append(move)

  return okmoves

# An alternative way to retrieve a list of legal moves, but it runs slower than getLegalMoves

def getLegalMovesTwo(state,player,oksquares):
  okmoves = []

  for oksquare in oksquares:                    # go through all open diagonal squares
    for piece in state.piecesLeft[player]:      # consider each remaining piece
      for geom in range(0,len(PIECES[piece])):  # consider each geometry for this piece
        p = PIECES[piece][geom]                 # the actual pattern for this piece
        height = len(p)                         # height of this geometry for this piece
        width  = len(p[0])                      # width of this geometry for this piece
        for a in range(0,height):               # go through rows of this piece and geometry
          for b in range(0,width):              # go through columns of this piece and geometry
            if p[a][b]:                         # if this piece has a square at this location
              row = oksquare[0]-a               # what row and column this piece could be put at
              col = oksquare[1]-b

              try:
                move = Move(piece,geom,row,col)
                if state.isMoveValid(move,player):
                  okmoves.append(move)
              except:
                b = 1
  return okmoves
