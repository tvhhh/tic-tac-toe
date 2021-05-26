# Author: tvhhh

import numpy as np

def encodeBoard(board):
    if isinstance(board, np.ndarray):
        return board
    
    encodedBoard = []
    for row in board:
        encodedRow = []
        for ceil in row:
            if ceil == 'X':
                encodedRow.append(1)
            elif ceil == 'O':
                encodedRow.append(-1)
            else:
                encodedRow.append(0)
        encodedBoard.append(encodedRow)
    return np.array(encodedBoard)

def decodeBoard(board):
    decodedBoard = []
    for row in board:
        decodedRow = []
        for ceil in row:
            if ceil == 1:
                decodedRow.append('X')
            elif ceil == -1:
                decodedRow.append('O')
            else:
                decodedRow.append(' ')
        decodedBoard.append(decodedRow)
    return decodedBoard

def checkBlock(block):
    if len(block.shape) != 2 or block.shape[0] != block.shape[1]:
        raise 'Must be a square block'
    
    n = block.shape[0]
    
    # Check rows
    for row in block:
        turn = row[0]
        if turn != 0 and np.all(row == [row[0]]*n):
            return True, turn
    
    # Check columns
    for col in block.T:
        turn = col[0]
        if turn != 0 and np.all(col == [col[0]]*n):
            return True, turn

    # Check diagonals
    turn = block[0][0]
    if turn != 0 and np.all(np.diag(block) == [turn]*n):
        return True, turn
    
    turn = block[0][n-1]
    if turn != 0 and np.all(np.diag(np.fliplr(block)) == [turn]*n):
        return True, turn
    
    return False, None
