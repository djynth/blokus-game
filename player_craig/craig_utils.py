from game_state import *
from move import *
from game_utils import *
from move_utils import *

def getLegalMovesAndSquares(state,player,oksquares=None):

  if not oksquares:
    oksquares = getLegalSquares(state,player)

  okmovesandsquares = []
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
                  option = {}
                  option['move'] = move
                  option['square'] = oksquare
                  option['row'] = row
                  option['col'] = col
                  option['piece'] = piece
                  option['geometry'] = geom
                  okmovesandsquares.append(option)

  return okmovesandsquares

