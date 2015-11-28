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

# Return (move, score)
# Lookahead simply means number of turns of the current player
def bestMove(state, player, lookahead):
    bestMoveScore = score(state, player)
    bestMoves = []
    for move in MoveUtils.getLegalMoves(state, player):
        state.applyMove(move, player)
        if lookahead == 0:
            moveScore = score(state, player)
        else:
            # List of (move, player)
            otherPlayerMoves = []
            for i in range(3):
                otherPlayer = (player + i + 1) % 4
                otherPlayerMove, _ = bestMove(state, otherPlayer, 0)
                otherPlayerMoves.append((otherPlayerMove, otherPlayer))
                state.applyMove(otherPlayerMove, otherPlayer)
            moveScore = bestMove(state, player, lookahead - 1)[1]
            for otherPlayerMove, otherPlayer in reversed(otherPlayerMoves):
                state.undoMove(otherPlayerMove, otherPlayer)
        state.undoMove(move, player)
        if moveScore >= bestMoveScore:
            if moveScore > bestMoveScore:
                bestMoves = []
                bestMoveScore = moveScore
            bestMoves.append(move)

    toReturn = None
    if len(bestMoves) > 0:
        toReturn = random.choice(bestMoves)

    return (toReturn, bestMoveScore)

def getMove(state, player):
    return bestMove(state, player, 1)[0]
