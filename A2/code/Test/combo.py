def valuate(number):
    print(f"HI: {number[0]}")
    arr = [7,2,6,3,1,12,5,9,4,8]
    val = arr[number[0]]
    number[0] += 1
    return val

def minimax_min_node(node, count):

    if not node:
        return valuate(count)
    
        #must flip as, we want the terminal_score relative to the maximizer (so we can make the right choice)

    
    if not node.left and not node.right:
        all_moves = [node.left, node.right]
    elif not node.left:
        all_moves = [node.right]
    elif not node.right:
        all_moves = [node.left]
    else:
        all_moves = [node.left, node.right]

    min_val = float("inf")
    for move in all_moves:
        #make the move
        pot_min = minimax_max_node(move, count)
        #update move based on lowest value possible

        if pot_min and pot_min < min_val:
            min_val = pot_min

    #cache results
    print(f"Returning Node: {node.name}, Value: {min_val}")
    return min_val


def minimax_max_node(node, count): #returns highest possible utility
    #color is AI's color, want to maximize
    if not node:
        return valuate(count) 


    if not node.left and not node.right:
        all_moves = [node.left, node.right]
    elif not node.left:
        all_moves = [node.right]
    elif not node.right:
        all_moves = [node.left]
    else:
        all_moves = [node.left, node.right]

    max_val = -1*float("inf")    
    # all_possible = []
    for move in all_moves:
        ##flip the color, min's turn, pick highest value that min returns
        ##pot_max = minimax_min_node(new_board, flip_color(color), limit-1, caching)
        #do not flip color
        pot_max = minimax_min_node(move, count)
        #update move based on highest value possible
        if pot_max and pot_max > max_val:
            max_val = pot_max

    #cache results
    print(f"Returning Node: {node.name}, Value: {max_val}")
    return max_val


def select_move_minimax():
    g = Node("G", None, None)
    h = Node("H", None, None)
    i = Node("I", None, None)
    j = Node("J", None, None)
    k = Node("K", None, None)

    d = Node("D", g, h)
    e = Node("E", i, j)
    f = Node("F", None, k)

    b = Node("B", d, None)
    c = Node("C", e, f)

    root = Node("A", b, c)

    return minimax_max_node(root, [0])


class Node:
    def __init__(self, name, left_kid, right_kid):
        self.name = name
        self.left = left_kid
        self.right = right_kid
    def set_left(self, left):
        self.left = left
    def set_right(self, right):
        self.right = right

select_move_minimax()