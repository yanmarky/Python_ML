"""
Tic Tac Toe Player
"""

import math
import copy
from util import Node, StackFrontier, QueueFrontier

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    
    board_position: [[(0,0), (0,1), (0,2)],
                     [(1,0), (1,1), (1,2)],
                     [(2,0), (2,1), (2,2)]]
    
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board, as "X" or "O"
    
    Logic: if board == initial_state, then X move
           elif get number of moves made by X and O, 
               if num_moves(X)=num_moves(O), X move, 
               if num_moves(X)>num_moves(O), O move
               else Error
    """
    if board == initial_state():
        return "X"
    else:
        posX =  get_position(board, "X")
        posO =  get_position(board, "O")
        if len(posX)==len(posO):
            return "X"
        elif len(posX)>len(posO):
            return "O"
        else:
            raise Exception("Invalid board state!")
            
    #raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    
    Just get all the None positions
    """
    posNone =  set(get_position(board, None))
    return posNone
    
    
    #raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    
    Need to use the player function to determine which player will make the next move
    """
    nextplayer = player(board)
    newboard = copy.deepcopy(board)
    
    if newboard[action[0]][action[1]] is None:
        newboard[action[0]][action[1]] = nextplayer
        return newboard
    else:
        raise Exception("Invalid action!")
    
    #raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    Return "X", "O", or "None"
    
    The current setup if not efficient: winner needs to be called in the 
    terminal function and again in the runner function. 
    
    """
    
    # Define win condition
    wincond = [((0,0),(0,1),(0,2)),
               ((1,0),(1,1),(1,2)),
               ((2,0),(2,1),(2,2)),
               ((0,0),(1,0),(2,0)),
               ((0,1),(1,1),(2,1)),
               ((0,2),(1,2),(2,2)),
               ((0,0),(1,1),(2,2)),
               ((0,2),(1,1),(2,0))]
    
    posX =  get_position(board, "X")
    winX = []
    posO =  get_position(board, "O")
    winO = []
    
    for t in wincond:
        winX.append(set(t).issubset(posX))
        
       # if set(t).issubset(posX):
       #     return "X"
        
    for t in wincond:
        winO.append(set(t).issubset(posO))
        
    if any(winX):
        return "X"
    elif any(winO):
        return "O"
    else:
        return None
    
    
    #raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    Potential improvement: only check the player's position who just made the move'
    """
  
     
    ##
    #board=[['X', 'X', 'O'], 
    #       ['X', 'X', ''], 
    #       ['O', 'O', 'X']]
    
    # first check if board is full
    posNone =  get_position(board, None)
    if len(posNone)==0:
        return True
    
    # Then get board position of each player and check if that player wins. 
    
    gameresults = winner(board)
        
    if gameresults is not None:
        return True
    else:
        return False
            
    #raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    gameresults = winner(board)
    if gameresults == 'X':
        return 1
    elif gameresults == 'O':
        return -1
    else:
        return 0
    
    
    
    #raise NotImplementedError


def min_value(board):
    if terminal(board):
        return utility(board)
    v = math.inf
   # print("Min",actions(board))
    for action in actions(board):
    #   print("MIN current",board)
    #   print(action)
        v = min(v, max_value(result(board,action)))
    #  print(v)
    return v

def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    #print("Max",actions(board))
    for action in actions(board):
    #   print("MAX current",board)
    #   print(action)
        v = max(v, min_value(result(board,action)))
    #   print(v)
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    If AI Plays "X", use max_value, if AI plays "O", use min_value
    
    Assumes that the game is not over yet
    """
    decisionset = dict()
    
    #frontier = StackFrontier()
    #frontier.add(board)
    
    if player(board)=="X":
        for action in actions(board):
            decisionset[action] = min_value(result(board, action))
        action = max(zip(decisionset.values(), decisionset.keys()))[1]
    else:
        for action in actions(board):
            decisionset[action] = max_value(result(board, action))
        action = min(zip(decisionset.values(), decisionset.keys()))[1]
    return action

    #raise NotImplementedError


def get_position(board,player):
    """
    Returns the board position for a given player
    """
    
    boardpos = []
    for row, l in enumerate(board):
        #temp.append([d*3+num for num in [i for i, x in enumerate(l) if x==player]])
        for col, l2 in enumerate(l):
            if l2 == player:
                boardpos.append((row,col)) 
    return boardpos
             