from game_state import *
from move import *
from game_utils import *

def getMove(state, player):
    print(str(state))

    piece = None
    while not piece in state.piecesLeft[player]:
        print('Available pieces:')
        print(state.piecesLeft[player])
        piece = input('Select a piece to place [or \'pass\']: ')

        if piece == 'pass':
            return None

    geometries = PIECES[piece]
    numGeometry = -1
    while 0 > numGeometry or numGeometry >= len(geometries):
        print('Possible geometries:')
        for geo in range(len(geometries)):
            print('##### ' + str(geo) + ' #####')
            print(gridToString(geometries[geo]))
            print()

        numGeometry = int(input('Select a geometry: '))

    row = -1
    col = -1
    while not isOnBoard(row, col):
        row = int(input('Select a row: '))
        col = int(input('Select a col: '))

    return Move(piece, numGeometry, row, col)
        