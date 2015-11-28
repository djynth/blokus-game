import game_state as GameState
import move as Move
import game_utils as GameUtils
import move_utils as MoveUtils
import random

# Return (tiles keyed be player number, totalTiles)
def tilesOnBoard(state):
    tilesByPlayer = {1: 0, 2: 0, 3: 0, 4: 0}
    totalTiles = 0
    for row in state.board:
        for cell in row:
            if 1 <= cell and cell <= 4:
                tilesByPlayer[cell] += 1
                totalTiles += 1
    return (tilesByPlayer, totalTiles)

# Your tilesOnBoard minus averaged score of other players
def score(state, player):
    tilesByPlayer, totalTiles = tilesOnBoard(state)
    playerTiles = tilesByPlayer[player]
    return playerTiles - ((totalTiles - playerTiles) / 3)

def getMove(state, player):
    bestMoveScore = score(state, player)
    bestMoves = []
    for move in MoveUtils.getLegalMoves(state, player):
        state.applyMove(move, player)
        moveScore = score(state, player)
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
