def valuate(node, alpha, beta, reversing):
    min_v = float("inf")

    updated_beta = beta
    if not reversing:
        for v in node.nodes:
            if updated_beta <= alpha:
                print(f"Pruned: term_node {v.name}")
                continue

            min_v = min(min_v, v.value)
            updated_beta = min(updated_beta, v.value) 
    else:
        for v in node.reverse_nodes():
            if updated_beta <= alpha:
                print(f"Pruned: term_node {v.name}")
                continue

            min_v = min(min_v, v.value)
            updated_beta = min(updated_beta, v.value) 

    return min_v

def all_terminal(node):
    for n in node.nodes:
        if not isinstance(n, Terminal):
            return False
    return True

def minimax_min_node(node, count, alpha, beta,reversing=False):

    if not node:
        return
    if all_terminal(node):
        return valuate(node, alpha, beta, reversing)
    
        #must flip as, we want the terminal_score relative to the maximizer (so we can make the right choice)

    
    if not reversing:
        all_moves = node.nodes
    else:
        all_moves = node.reverse_nodes()

    updated_beta = beta

    min_val = float("inf")
    for move in all_moves:

        if updated_beta <= alpha:
            print(f"Pruned: from Node {node.name} to Node {move.name}")
            break

        #make the move
        pot_min = minimax_max_node(move, count, alpha, updated_beta, reversing)
        #update move based on lowest value possible

        if pot_min and pot_min < updated_beta:
            updated_beta = pot_min

        if pot_min and pot_min < min_val:
            min_val = pot_min

    #cache results
    print(f"Returning Node: {node.name}, Value: {min_val}")
    return min_val


def minimax_max_node(node, count, alpha, beta, reversing=False): #returns highest possible utility
    if not node:
        return

    #color is AI's color, want to maximize
    if all_terminal(node):
        return valuate( node, alpha, beta, reversing)


    if not reversing:
        all_moves = node.nodes
    else:
        all_moves = node.reverse_nodes()

    updated_alpha = alpha

    max_val = -1*float("inf")    
    # all_possible = []
    for move in all_moves:

        if beta <= updated_alpha:
            print(f"Pruned: from Node {node.name} to Node {move.name}")
            break

        ##flip the color, min's turn, pick highest value that min returns
        ##pot_max = minimax_min_node(new_board, flip_color(color), limit-1, caching)
        #do not flip color
        pot_max = minimax_min_node(move, count, updated_alpha, beta, reversing)
        #update move based on highest value possible
        if pot_max and pot_max > updated_alpha:
            updated_alpha = pot_max
        
        if pot_max and pot_max > max_val:
            max_val = pot_max

    #cache results
    print(f"Returning Node: {node.name}, Value: {max_val}")
    return max_val


def select_move_minimax():

  

    h = Node("H",nodes=[Terminal("e14",4)])
    i = Node("I",nodes=[Terminal("e15",3)])
    j = Node("J",nodes=[Terminal("e16",3), Terminal("e17",2), Terminal("e18",4)])
    k = Node("K",nodes=[Terminal("e19",2), Terminal("e20",1)])
    l = Node("L",nodes=[Terminal("e21",3), Terminal("e22",4)])
    m = Node("M",nodes=[Terminal("e23",4), Terminal("e24",1)])
    n = Node("N",nodes=[Terminal("e25",2), Terminal("e26",3)])

    d = Node("D", nodes= [h, None])
    e = Node("E", nodes= [i, j])
    f = Node("F", nodes= [k, l])
    g = Node("G", nodes= [m, n])

    b = Node("B", nodes=[d, e])
    c = Node("C", nodes=[f, g])

    root = Node("A", nodes=[b, c])

    return minimax_max_node(root, [0], alpha=-1*float("inf"), beta=float("inf"), reversing=False)


class Terminal:
    def __init__(self, name, size):
        self.name = name
        self.value = size


class Node:
    def __init__(self, name, nodes):
        self.name = name
        self.nodes = nodes
    def reverse_nodes(self):
        value = []
        for i in range(len(self.nodes)-1,-1,-1):
            value.append(self.nodes[i])
        return value


select_move_minimax()