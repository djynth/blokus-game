import game_state as GameState
import move as Move
import game_utils as GameUtils
import move_utils as MoveUtils
import itertools
import random

# Number of cells away from each liberty that factor into space score
SPACE_SCORE_DISTANCE = 10

PLAYERS = [1, 2, 3, 4]

def blankMetric():
    return {1: 0, 2: 0, 3: 0, 4: 0}

def blankList():
    return {1: [], 2: [], 3: [], 4: []}

def onBoard(cell):
    return (cell[0] >= 0 and
        cell[1] >= 0 and
        cell[0] < GameUtils.ROWS and
        cell[1] < GameUtils.COLS)

# return list of (row, col) diagonally touching the cell
def diagonals(cell):
    toReturn = []
    for i, j in [(-1, -1), (-1, 1), (1, 1), (1, -1)]:
        newCell = (cell[0] + i, cell[1] + j)
        if onBoard(newCell):
            toReturn.append(newCell)
    return toReturn

def friendlyDiagonals(cell, board, player):
    toReturn = []
    for diagonal in diagonals(cell):
        if board[diagonal[0]][diagonal[1]] == player:
            toReturn.append(diagonal)
    return toReturn

# return list of (row, col) directly touching the cell
def borders(cell):
    toReturn = []
    for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        newCell = (cell[0] + i, cell[1] + j)
        if onBoard(newCell):
            toReturn.append(newCell)
    return toReturn

def friendlyBorders(cell, board, player):
    toReturn = []
    for border in borders(cell):
        if board[border[0]][border[1]] == player:
            toReturn.append(border)
    return toReturn

def printSpaceMap(spaceMap):
    for row in spaceMap:
        print(' '.join(str(c) for c in row))

def getBoardMetrics(state):
    numTiles = blankMetric()
    numLiberties = blankMetric()
    spaceScore = blankMetric()

    liberties = blankList()

    for row, col in itertools.product(range(20), range(20)):
        cell = (row, col)
        contents = state.board[row][col]
        if contents == 0:
            for player in PLAYERS:
                if (len(friendlyDiagonals(cell, state.board, player)) > 0 and
                        len(friendlyBorders(cell, state.board, player)) == 0):
                    liberties[player].append(cell)
                    numLiberties[player] += 1
        elif contents <= 4:
            numTiles[contents] += 1

    for player in PLAYERS:
        spaceMap = [[0 for i in range(GameUtils.COLS)] \
                for j in range(GameUtils.ROWS)]
        frontier = liberties[player]
        for iterNum in reversed(range(SPACE_SCORE_DISTANCE)):
            newFrontier = []
            for f in frontier:
                if spaceMap[f[0]][f[1]] == 0 and \
                        len(friendlyBorders(f, state.board, player)) == 0:
                    spaceMap[f[0]][f[1]] = iterNum
                    for n in borders(f):
                        if state.board[n[0]][n[1]] == 0:
                            newFrontier.append(n)
            frontier = newFrontier
        for row in spaceMap:
            for cell in row:
                spaceScore[player] += cell

    return (numTiles, numLiberties, spaceScore)

# Your tilesOnBoard minus averaged score of other players
def score(state, player):
    numTiles, numLiberties, spaceScore = getBoardMetrics(state)
    return numTiles[player] * 10000 + spaceScore[player]

# Aggressively tries to lower other players' scores
def weightedScore(state, player):
    myScore = score(state, player)
    otherPlayers = PLAYERS.copy()
    otherPlayers.remove(player)
    otherScores = list(map(lambda p: score(state, p), otherPlayers))
    return myScore - max(otherScores)

def getMove(state, player):
    bestMoveScore = weightedScore(state, player)
    bestMoves = []
    for move in MoveUtils.getLegalMoves(state, player):
        state.applyMove(move, player)
        moveScore = weightedScore(state, player)
        state.undoMove(move, player)
        if moveScore >= bestMoveScore:
            if moveScore > bestMoveScore:
                bestMoves = []
                bestMoveScore = moveScore
            bestMoves.append(move)
    if len(bestMoves) > 0:
        return random.choice(bestMoves)
    else:
        return None
