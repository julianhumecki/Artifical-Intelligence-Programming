"""
HEURISTIC DESCRIPTION:

I made use of the existing compute_utility function, and the number of moves available to the agent.
Then, I accounted for moves that have a heavy weight. I.E the corners and the pieces surrounding the corners.
"""

import random
import sys
import time

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

#use board state to cache
#if encountered again, return cached value, but only if cache=1
#CONSIDER TWO SEPARATE CACHES, ONE FOR MIN, OTHER FOR MAX
previously_seen_states = dict()

def eprint(*args, **kwargs): #you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)
    
# Method to compute utility value of terminal state
def compute_utility(board, color):
    #(# of dark, # of light) get returned from get score
    #1 is dark, 2 is light
    
    counts = get_score(board)
    if color == 1:
        return counts[0] - counts[1]
    else:
        return counts[1] - counts[0]
    

# Better heuristic value of board, designed for even dimensions
def compute_heuristic(board, color): 
    board_size = len(board)
    heur = compute_utility(board, color)
    #fixed weight matrices
    eight_by_eight = [  [1000 ,-350,120, 0, 0, 120,-350, 1000],
                        [-350,-600,-70,-60,-60,-70,-600, -350],
                        [120, -70,  8,  2,  2,  8, -70,   120],
                        [0,  -60,  2,  4,  4,  2, -60,    0 ],
                        [0,  -60,  2,  4,  4,  2, -60,    0 ],
                        [120, -70,  8,  2,  2,  8,  -70,  120],
                        [-350,-600, -70,-60,-60,-70,-600,-350],
                        [1000,-350, 120,0, 0, 120, -350, 1000]]

    four_by_four = [
        [1000,0,0,1000],
        [0, 2,2, 0],
        [0, 2,2, 0],
        [1000,0,0,1000]]
    
    six_by_six = [
        [1000,-350, 50, 50,-350,1000],
        [-350,-500,-60,-60,-500,-350],
        [50,  -60, 4,  4,  -60,   50],
        [50, -60,  4,  4,  -60,   50],
        [-350,-500,-60,-60,-500,-350],
        [1000,-350,50,50, -350, 1000]]
    
    if board_size == 8:
        heur += convolve(board, eight_by_eight, color)
    elif board_size == 6:
        heur += convolve(board, six_by_six, color)
    elif board_size == 4:
        heur += convolve(board, four_by_four, color)
    
    return heur
    
def convolve(board, weights, color):
    board_size = len(board)
    total = 0
    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] == color:
                total += 1*weights[i][j]
            elif board[i][j] == flip_color(color):
                total += -1*weights[i][j]
    return total


############ MINIMAX ###############################
#MAX'S COLOR IS ALWAYS PASSED IN TO BOTH MIN AND MAX, then you flip it when passing in color for min's move
def minimax_min_node(board, color, limit, caching = 0):
    
    if limit == 0:
        #must flip as, we want the terminal_score relative to the maximizer (so we can make the right choice)
        return (None, compute_utility(board, color))
    
    #check if cache is enabled
    if caching == 1:
        #check if state has been cached
        if board in previously_seen_states:
            return previously_seen_states[board]

    all_moves = get_possible_moves(board, flip_color(color))
    if len(all_moves) == 0:
        return (None, compute_utility(board, color))
    
    min_val = float("inf")
    min_move = None
    for move in all_moves:
        #make the move
        new_board = play_move(board, flip_color(color), move[0], move[1])
        # #flip the color, max's turn, pick lowest value that max returns
        # #pot_min = minimax_max_node(new_board, flip_color(color), limit-1, caching)
        pot_min = minimax_max_node(new_board, color, limit-1, caching)
        #update move based on lowest value possible
        if pot_min[1] < min_val:
            min_val = pot_min[1]
            min_move = move

    #cache results
    if caching == 1:
        previously_seen_states[board] = (min_move,min_val)
    return (min_move, min_val)


def minimax_max_node(board, color, limit, caching = 0): #returns highest possible utility
    #color is AI's color, want to maximize
    if limit == 0:
        return (None, compute_utility(board, color))
    #check if cache is enabled
    if caching == 1:
        #check if state has been cached
        if board in previously_seen_states:
            return previously_seen_states[board]

    all_moves = get_possible_moves(board, color)
    if len(all_moves) == 0:
        return (None, compute_utility(board, color))
    
    max_val = -1*float("inf")    
    max_move = None
    # all_possible = []
    for move in all_moves:
        #make the move
        new_board = play_move(board, color, move[0], move[1])
        ##flip the color, min's turn, pick highest value that min returns
        ##pot_max = minimax_min_node(new_board, flip_color(color), limit-1, caching)
        #do not flip color
        pot_max = minimax_min_node(new_board, color, limit-1, caching)
        #update move based on highest value possible
        if pot_max[1] > max_val:
            max_val = pot_max[1]
            max_move = move

    #cache results
    if caching == 1:
        previously_seen_states[board] = (max_move,max_val)
    return (max_move,max_val)


#flip color, change turn
def flip_color(color):
    if color == 1:
        return 2
    else:
        return 1

def select_move_minimax(board, color, limit, caching = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    """
    #return best move
    return minimax_max_node(board, color, limit, caching)[0]





############ ALPHA-BETA PRUNING #####################
#MAX'S COLOR IS ALWAYS PASSED IN TO BOTH MIN AND MAX, then you flip it once making the move
def alphabeta_min_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    if limit == 0:
        #must flip as, we want the terminal_score relative to the maximizer (so we can make the right choice)
        return (None, compute_utility(board, color))
    if caching == 1:
        #check if state has been cached
        if board in previously_seen_states:
            return previously_seen_states[board]

    all_moves = get_possible_moves(board, flip_color(color))
    if len(all_moves) == 0:
        return (None, compute_utility(board, (color)))
    
    min_val = float("inf")
    min_move = None
    updated_beta = beta

    #sort based on smallest value first
    #flip color, as we want to calculate value with respect to maximization
    if ordering == 1:
        all_moves = sorted(all_moves, key=lambda move: compute_utility(play_move(board, flip_color(color), move[0], move[1]), color), reverse=False)
        # all_moves = sorted(all_moves, key=lambda move: compute_heuristic(play_move(board, flip_color(color), move[0], move[1]), color), reverse=False)

    for move in all_moves:
        #if true, we stop, pruning unnecessary paths
        if updated_beta <= alpha:
            break

        #make the move
        new_board = play_move(board, flip_color(color), move[0], move[1])

        #flip the color, max's turn, pick lowest value that max returns
        pot_min = alphabeta_max_node(new_board, (color), alpha, updated_beta, limit-1, caching)

        #update the value of updated beta
        if pot_min[1] < updated_beta:
            updated_beta = pot_min[1]
        
        #update move based on lowest value possible
        if pot_min[1] < min_val:
            min_val = pot_min[1]
            min_move = move

    #cache results
    if caching == 1:
        previously_seen_states[board] = (min_move,min_val)
    return (min_move, min_val)

def alphabeta_max_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    if limit == 0:
        return (None, compute_utility(board, color))

    if caching == 1:
        #check if state has been cached
        if board in previously_seen_states:
            return previously_seen_states[board]
  
    all_moves = get_possible_moves(board, color)
    if len(all_moves) == 0:
        return (None, compute_utility(board, color))
    
    max_val = -1*float("inf")    
    max_move = None

    #want beta to be as small as possible and alpha to be as large as possible
    #update alpha in max nodes and update beta in min nodes, prune if beta <= alpha
    updated_alpha = alpha

    #sort based on smallest value first
    #do not flip color!
    if ordering == 1:
        # sort from highest to lowest utility value of the move
        all_moves = sorted(all_moves, key=lambda move: compute_utility(play_move(board, color, move[0], move[1]), color), reverse=True)
        # all_moves = sorted(all_moves, key=lambda move: compute_heuristic(play_move(board, color, move[0], move[1]), color), reverse=True)

    for move in all_moves:
        #prune if lower beta was found somewhere else
        if beta <= updated_alpha:
            break
        
        #make the move
        new_board = play_move(board, color, move[0], move[1])
        #DO NOT::: flip the color, min's turn, pick highest value that min returns
        pot_max = alphabeta_min_node(new_board, (color), updated_alpha, beta ,limit-1, caching)
        
        #update alpha if a higher value was found
        if pot_max[1] > updated_alpha:
            updated_alpha = pot_max[1]
        #update move based on highest value possible
        if pot_max[1] > max_val:
            max_val = pot_max[1]
            max_move = move
    
    #cache results
    if caching == 1:
        previously_seen_states[board] = (max_move,max_val)
    return (max_move,max_val)


def select_move_alphabeta(board, color, limit, caching = 0, ordering = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations. 
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations. 
    """
    return alphabeta_max_node(board, color, alpha=-1*float("inf"), beta=float("inf"), limit=limit, caching=caching, ordering=ordering)[0]


####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    eprint("Othello AI") # First line is the name of this AI
    arguments = input().split(",")
    
    color = int(arguments[0]) #Player color: 1 for dark (goes first), 2 for light. 
    limit = int(arguments[1]) #Depth limit
    minimax = int(arguments[2]) #Minimax or alpha beta
    caching = int(arguments[3]) #Caching 
    ordering = int(arguments[4]) #Node-ordering (for alpha-beta only)

    if (minimax == 1): eprint("Running MINIMAX")
    else: eprint("Running ALPHA-BETA")

    if (caching == 1): eprint("State Caching is ON")
    else: eprint("State Caching is OFF")

    if (ordering == 1): eprint("Node Ordering is ON")
    else: eprint("Node Ordering is OFF")

    if (limit == -1): eprint("Depth Limit is OFF")
    else: eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1): #run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else: #else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)
            
            eprint("{} {}".format(movei, movej))

if __name__ == "__main__":
    run_ai()
