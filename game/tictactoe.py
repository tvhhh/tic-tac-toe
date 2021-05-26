# Author: tvhhh
# Board state of Tic-Tac-Toe

from game.utils import encodeBoard, decodeBoard, checkBlock
import numpy as np

class TicTacToeState:
    def __init__(self, board, bot='X'):
        self.board = encodeBoard(board)

        # 1 is X, -1 is O
        if bot == 'X':
            self.bot = 1
        elif bot == 'O':
            self.bot = -1
        else:
            raise 'Undefined character, expected either X or O'
        self.opponent = -self.bot
        
        self.winner = None
        self.streak = min(len(self.board), 5)
    
    def getBoard(self):
        return decodeBoard(self.board)
    
    def getWinner(self):
        if self.winner == 1:
            return 'X'
        elif self.winner == -1:
            return 'O'
        return None
    
    def getLegalMoves(self):
        h, w = self.board.shape
        moves = []
        for i in range(h):
            for j in range(w):
                if self.board[i,j] == 0:
                    moves.append((i,j))
        return moves
    
    def getNextState(self, move):
        x = np.sum(self.board == 1)
        o = np.sum(self.board == -1)
        turn = -1 if x > o else 1

        board = self.board.copy()
        if board[move] == 0:
            board[move] = turn
        else:
            raise 'Invalid move'
        return TicTacToeState(board, 'X' if self.bot == 1 else 'O')
    
    def isGameOver(self):
        for i in range(len(self.board)-self.streak+1):
            for j in range(len(self.board)-self.streak+1):
                isOver, winner = checkBlock(self.board[i:i+self.streak,j:j+self.streak])
                if isOver:
                    self.winner = winner
                    return True
        if not np.any(self.board == 0):
            self.winner = 0
            return True
        return False
    
    def isWin(self):
        return self.winner == self.bot
    
    def isLose(self):
        return self.winner == self.opponent
    
    def isDraw(self):
        return self.winner == 0
    
    def __eq__(self, other):
        return np.all(self.board == other.board)
    
    def __hash__(self):
        return hash(str(self.board))
    
    def __str__(self):
        lines = []
        horizontalLine = ('-' * (4*self.board.shape[1]+1))
        lines.append(horizontalLine)
        for row in self.board:
            rowLine = '|'
            for col in row:
                if col == 0:
                    col = ' '
                elif col == 1:
                    col = 'X'
                elif col == -1:
                    col = 'O'
                rowLine = rowLine + ' ' + col.__str__() + ' |'
            lines.append(rowLine)
            lines.append(horizontalLine)
        return '\n'.join(lines)
