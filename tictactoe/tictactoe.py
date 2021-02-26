"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Define win condition
    wincond = [(0,1,2),(2,5,8),(0,3,6),(0,4,8),(2,4,6),(6,7,8)]
    
    # first get board position of each player
    ##
    #board=[['X', 'X', 'O'], ['X', 'X', ''], ['O', 'O', 'X']]
    temp = []
    for d, l in enumerate(board):
        temp.append([d*3+num for num in [i for i, x in enumerate(l) if x=="X"]])
    
    boardpos_X = []
    for l in temp:
         for ele in l:
             boardpos_X.append(ele)
     
    for t in wincond:
        if set(t).issubset(boardpos_X):
            print("True")
         
        
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
