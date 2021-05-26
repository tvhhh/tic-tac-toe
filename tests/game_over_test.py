import sys
import os
dir_name = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_name, '../'))

from game.tictactoe import TicTacToeState
import unittest

class GameOverTest(unittest.TestCase):
    
    def test_first_row(self):
        board = TicTacToeState([
            ['X', 'X', 'X'],
            [' ', ' ', ' '],
            [' ', ' ', ' ']
        ])
        isOver = board.isGameOver()
        winner = board.getWinner()
        self.assertTrue(isOver and winner == 'X')

if __name__ == "__main__":
    unittest.main()
