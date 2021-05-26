import sys
import os
dir_name = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_name, '../'))

from game.tictactoe import TicTacToeState
from game.alpha_beta import AlphaBetaAgent

def botMoveFirst():
    board = [[' '] * 3] * 3
    gameState = TicTacToeState(board, bot='X')
    while not gameState.isGameOver():
        print("Bot turn")
        action = AlphaBetaAgent().search(gameState)
        gameState = gameState.getNextState(action)
        print(str(gameState))
        if gameState.isGameOver(): break
        x, y = input("Your turn (x y): ").split()
        gameState = gameState.getNextState((int(x),int(y)))
        print(str(gameState))
    if gameState.isWin():
        print("me pro, you noob")
    elif gameState.isLose():
        print("me black, you lucky")
    elif gameState.isDraw():
        print("ggwp")

def botMoveLater():
    board = [[' '] * 3] * 3
    gameState = TicTacToeState(board, bot='O')
    print(str(gameState))
    while not gameState.isGameOver():
        x, y = input("Your turn (x y): ").split()
        gameState = gameState.getNextState((int(x),int(y)))
        print(str(gameState))
        if gameState.isGameOver(): break
        print("Bot turn")
        action = AlphaBetaAgent().search(gameState)
        gameState = gameState.getNextState(action)
        print(str(gameState))
    if gameState.isWin():
        print("me pro, you noob")
    elif gameState.isLose():
        print("me black, you lucky")
    elif gameState.isDraw():
        print("ggwp")

if __name__ == "__main__":
    botMoveFirst()
