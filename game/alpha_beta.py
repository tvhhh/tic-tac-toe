# Author: tvhhh
# Alpha-Beta algorithm

import time

POS_INF = float('inf')
NEG_INF = float('-inf')

def display_exec_time(func):
    def wrapper(self, *args, **kwargs):
        start = time.time()
        ret_val = func(self, *args, **kwargs)
        end = time.time()
        print(f"Execution time: {(end-start):.3f}s")
        return ret_val
    return wrapper

class AlphaBetaAgent:
    
    @display_exec_time
    def search(self, state):
        _, action = self.__maximin(state, NEG_INF, POS_INF)
        return action
    
    def __maximin(self, state, alpha, beta):
        if self.__terminal_test(state):
            return self.__utility(state), None
        
        successorCost = NEG_INF
        successorAction = None
        actions = state.getLegalMoves()
        
        for action in actions:
            nextState = state.getNextState(action)
            cost, _ = self.__minimax(nextState, alpha, beta)
            if cost > successorCost:
                successorCost = cost
                successorAction = action
            if successorCost >= beta:
                return successorCost, action # pruning
            alpha = max(successorCost, alpha)
        
        return successorCost, successorAction

    def __minimax(self, state, alpha, beta):
        if self.__terminal_test(state):
            return self.__utility(state), None

        successorCost = POS_INF
        successorAction = None
        actions = state.getLegalMoves()

        for action in actions:
            nextState = state.getNextState(action)
            cost, _ = self.__maximin(nextState, alpha, beta)
            if cost < successorCost:
                successorCost = cost
                successorAction = action
            if successorCost <= alpha: 
                return successorCost, action # pruning
            beta = min(successorCost, beta)
        
        return successorCost, successorAction

    def __terminal_test(self, state):
        return state.isGameOver()

    def __utility(self, state):
        if state.isWin():
            return 1
        elif state.isLose():
            return -1
        elif state.isDraw():
            return 0
        else:
            raise 'Game still in progress'
