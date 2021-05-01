#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

import os
from search import * #for search engines
from snowman import SnowmanState, Direction, snowman_goal_state #for snowball specific classes
from test_problems import PROBLEMS #20 test problems

def heur_manhattan_distance(state):
#IMPLEMENT
    '''admissible sokoban puzzle heuristic: manhattan distance'''
    '''INPUT: a snowman state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #We want an admissible heuristic, which is an optimistic heuristic.
    #It must never overestimate the cost to get from the current state to the goal.
    #The sum of the Manhattan distances between each snowball that has yet to be stored and the storage point is such a heuristic.
    #When calculating distances, assume there are no obstacles on the grid.
    #You should implement this heuristic function exactly, even if it is tempting to improve it.
    #Your function should return a numeric value; this is the estimate of the distance to the goal.
    # print(dir(state))
    # print(type(state.obstacles))
    print(state.obstacles)
    print(state.action)
    # print(state.robot)
    # print(state.destination)
    # print(state.snowballs)
    # print()
    # print(state.width)
    # print(state.height)
    # print()
    
    # state.print_state()
    total_manhattan = 0
    #loop over all snow balls and sum their manhattan distances from the destination
    for snowball in state.snowballs:
      total_manhattan += abs(snowball[0] - state.destination[0]) + abs(snowball[1] - state.destination[1])
    return total_manhattan


#HEURISTICS
def trivial_heuristic(state):
  '''trivial admissible snowball heuristic'''
  '''INPUT: a snowball state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state (# of moves required to get) to the goal.'''   
  return len(state.snowballs)

def heur_alternate(state):
  snowballs_on_board = {0: ['b', False],1: ['m', False], 2: ['s', False], 3: ['A', False], 4: ['B', False], 5: ['C', False], 6:['G',False]}
  inverse_mapping = dict()

  #table to figure out which states exist
  for snowball in state.snowballs:
    value_indicator = state.snowballs[snowball]
    snowballs_on_board[value_indicator][1] = True
    inverse_mapping[value_indicator] = snowball
      
  #get small's position, get medium's pos, get big's pos
  small_pos = get_position(snowballs_on_board, inverse_mapping, indices=[2,4,5,6])
  medium_pos = get_position(snowballs_on_board, inverse_mapping, indices=[1,3,4,6])
  big_pos = get_position(snowballs_on_board, inverse_mapping, indices=[0,3,5,6])
  goal_pos = state.destination

  blocks_to_goal = 0
  #new approach = one block at a time

  # if big_pos != goal_pos:
  #     blocks_to_goal += 3**man_distance(state.robot, big_pos)
  
  # # blocks_to_goal += 3**man_distance(big_pos, goal_pos) 
  # if medium_pos != goal_pos:    
  #   blocks_to_goal += 2**man_distance(state.robot, medium_pos)
  
  # # blocks_to_goal += 2**man_distance(medium_pos, goal_pos) 
  
  # if small_pos != goal_pos:
  #   blocks_to_goal += man_distance(state.robot, small_pos)

  # # blocks_to_goal += man_distance(small_pos, goal_pos) 

  #now we want to keep our snowballs away from the obstacles
  all_balls = [small_pos, medium_pos, big_pos]
  #define width and height
  width = state.width
  height = state.height


  bad_spots = dict()
  all_obs = dict()
  #all this does is penalize spots beside obstacles, not accounting for tunnels or goal spots
  for obs in state.obstacles:
    # if not ((obs[0]+1, obs[1]+1) in bad_spots):
    #   bad_spots[(obs[0]+1, obs[1]+1)] = 1
    # else:
    #   bad_spots[(obs[0]+1, obs[1]+1)] += 1
    #   bad_spots[(obs[0]+1, obs[1]+1)] %= 2
    #checks corners
    # bad_spots[(obs[0]+1, obs[1]+1)] = 1
    # bad_spots[(obs[0]-1, obs[1]+1)] = 1
    # bad_spots[(obs[0]+1, obs[1]-1)] = 1
    # bad_spots[(obs[0]-1, obs[1]-1)] = 1
    all_obs[obs] = 1
    #Mark danger spots above and below & left and right of obstacle, not corners
    if (obs[0]+1, obs[1]) != goal_pos:
      bad_spots[(obs[0]+1, obs[1])] = 1
    if (obs[0]-1, obs[1]) != goal_pos:
      bad_spots[(obs[0]-1, obs[1])] = 1
    if (obs[0], obs[1]+1) != goal_pos:
      bad_spots[(obs[0], obs[1]+1)] = 1
    if (obs[0], obs[1]-1) != goal_pos:
      bad_spots[(obs[0], obs[1]-1)] = 1


  #goodspots =========================================================================================
  good_spots = dict()
  #all good left spots are from goal left until and obstacle is hit
  s_left = goal_pos[0]
  while not ((s_left, goal_pos[1]) in all_obs) and s_left >= 0:
    good_spots[s_left, goal_pos[1]] = 1
    s_left -= 1
  
  s_right = goal_pos[0]
  while not ((s_right, goal_pos[1]) in all_obs) and s_right < width:
    good_spots[s_right, goal_pos[1]] = 1
    s_right += 1

  s_top = goal_pos[1]
  while not ((goal_pos[0], s_top) in all_obs) and s_top >= 0:
    good_spots[(goal_pos[0], s_top)] = 1
    s_top -= 1
  
  s_bot = goal_pos[1]
  while not ((goal_pos[0], s_bot) in all_obs) and s_bot < height:
    good_spots[(goal_pos[0], s_bot)] = 1
    s_bot += 1
  
  #remove good from bad
  for g_b in good_spots:
    if g_b in bad_spots:
      del bad_spots[g_b] 

  #extend the good states
  # extend_good_spots(goal_pos, good_spots, all_obs, dict(), width, height)
  visited = dict()
  secondary_good_spots = dict()
  # for spot in good_spots:
  #   extend_good_spots_left(spot, secondary_good_spots, all_obs, visited, width, height)
  #   extend_good_spots_right(spot, secondary_good_spots, all_obs, visited, width, height)
  #   extend_good_spots_up(spot, secondary_good_spots, all_obs, visited, width, height)
  #   extend_good_spots_down(spot, secondary_good_spots, all_obs, visited, width, height)

  #distance of robot to packages
  if big_pos != goal_pos:
    blocks_to_goal += 3**man_distance(state.robot, big_pos)

  if medium_pos != goal_pos:    
    blocks_to_goal += 2**man_distance(state.robot, medium_pos)
  
  if small_pos != goal_pos:
    blocks_to_goal += man_distance(state.robot, small_pos)

  #getting block to goal is more important
  big_hh = hh_helper(good_spots, big_pos, goal_pos, width, height) 
  if big_pos != goal_pos:
    blocks_to_goal += 3**big_hh
  med_hh = hh_helper(good_spots, medium_pos, goal_pos, width, height)
  if medium_pos != goal_pos:
    blocks_to_goal += 2**med_hh
  small_hh = hh_helper(good_spots, small_pos, goal_pos, width, height)
  if small_pos != goal_pos:
    blocks_to_goal += small_hh


  #punish based on not being able to move 
  #let's update this to not punish if the curr pos is a good_spot
  #without good_spots check include, solved 17/20, 16 better than bench mark
  # if big_pos != goal_pos and not (big_pos in good_spots):
  if big_pos != goal_pos:
    blocks_to_goal += degrees_of_freedom(3, big_pos, big_hh, all_obs, goal_pos, width, height)
  # if medium_pos != goal_pos and not (medium_pos in good_spots):
  if medium_pos != goal_pos:
    blocks_to_goal += degrees_of_freedom(2, medium_pos, med_hh, all_obs, goal_pos, width, height)
  # if small_pos != goal_pos and not (small_pos in good_spots):
  if small_pos != goal_pos:
    blocks_to_goal += degrees_of_freedom(1, small_pos, small_hh, all_obs, goal_pos, width, height)

  # #up
  # if state.action[0].lower() == 'u':
  #   #blocked from above
  #   if big_pos[0],big_pos[1]-1 in all_obs:
  #     blocks_to_goal += 3*big_hh


  # #down
  # if state.action[0].lower() == 'd':

  # #left
  # if state.action[0].lower() == 'l':

  # #right
  # if state.action[0].lower() == 'r':

  # if big_pos in bad_spots:
  #   blocks_to_goal += 2*big_hh
  # if med_hh in bad_spots:
  #   blocks_to_goal += 1.5*med_hh
  # if small_hh in bad_spots:
  #   blocks_to_goal += small_hh


  #if neither are true, penalize big time




  # print(bad_spots)


  # for ball in all_balls:
  #   penalty = 0
  #   for obstacle in state.obstacles:
  #     #count how many obstacles we are close to (without being surrounded [if one is directly to our left])->return 4**nummber
  #     if abs(obstacle[0] - ball[0]) == 1:
  #       #sometimes its necessary to be beside an obstacle (shouldnt be penalized when necessary)
  #       num = obstacle[0] - ball[0]
  #       #obstacle is to the right of ball, check left
  #       if num > 0:
  #         #check if other side of block is beside another obstacle or game boundary
  #         #if it is, you shouldnt get penalized, as you can go anywhere else
  #         if ((ball[0]-1,ball[1]) in bad_spots or (ball[0]-1 < 0)) or ((ball[0]-2,ball[1]) in bad_spots or (ball[0]-2 < 0)):
  #           #no penalty
  #           continue
  #       else:
  #         #obstacle is to the left of ball, check right
  #         if ((ball[0]+1,ball[1]) in bad_spots or (ball[0]+1 >= width)) or ((ball[0]+2,ball[1]) in bad_spots or (ball[0]+2 >= width)):
  #           #no penalty
  #           continue
  #       penalty += 10

  #     if abs(obstacle[1] - ball[1]) == 1:
  #       #sometimes its necessary to be beside an obstacle (shouldnt be penalized when necessary), include game boundaries in these checks
  #       num = obstacle[1] - ball[1]
  #       #obstacle is to the below the ball, check above
  #       if num > 0:
  #         if ((ball[0],ball[1]-1) in bad_spots or (ball[1]-1 < 0)) or ((ball[0],ball[1]-2) in bad_spots or (ball[1]-2 < 0)):
  #           #no penalty
  #           continue
  #       else:
  #         #obstacle is to the above the ball, check below
  #         if ((ball[0],ball[1]+1) in bad_spots or (ball[1]+1 >= height)) or ((ball[0],ball[1]+2) in bad_spots or (ball[1]+2 >= height)):
  #           #no penalty
  #           continue
  #       penalty += 10

  #     #add the penalty, very harsh penalty  
  #     blocks_to_goal += 2**penalty 
  # #loop over all obstacles an mark all positions directly beside them as aids (stay away from)

  # -----------------------------------------------------------------------------------------------------
  # bad_spots = dict()
  # #all this does is penalize spots beside obstacles, not accounting for tunnels or goal spots
  # for obs in state.obstacles:
  #   bad_spots[(obs[0]+1, obs[1]+1)] = 1
  #   bad_spots[(obs[0]-1, obs[1]+1)] = 1
  #   bad_spots[(obs[0]+1, obs[1]-1)] = 1
  #   bad_spots[(obs[0]-1, obs[1]-1)] = 1
  
  # if big_pos in bad_spots:
  #   blocks_to_goal += 4**10
  # if medium_pos in bad_spots:
  #   blocks_to_goal += 4**10
  # if small_pos in bad_spots:
  #   blocks_to_goal += 4**10

  blocks_to_goal += check_for_dead_ends(big_pos, all_obs, state.width, state.height, goal_pos)
  blocks_to_goal += check_for_dead_ends(medium_pos, all_obs, state.width, state.height, goal_pos)
  blocks_to_goal += check_for_dead_ends(small_pos, all_obs, state.width, state.height, goal_pos)
  
  return blocks_to_goal

def extend_good_spots_left(curr_pos, good_spots, all_obs, visited, width, height):
  if curr_pos[0] < 0 or curr_pos[0] >= width:
    return
  elif curr_pos[1] < 0 or curr_pos[1] >=height:
    return
  elif curr_pos in all_obs:
    return
  elif curr_pos in visited:
    return
  else:
    visited[curr_pos] = 1
    good_spots[curr_pos] = 1
    #explore up, down, left, right
    extend_good_spots_left((curr_pos[0]-1, curr_pos[1]),good_spots, all_obs, visited, width, height)
    return

def extend_good_spots_right(curr_pos, good_spots, all_obs, visited, width, height):
  if curr_pos[0] < 0 or curr_pos[0] >= width:
    return
  elif curr_pos[1] < 0 or curr_pos[1] >=height:
    return
  elif curr_pos in all_obs:
    return
  elif curr_pos in visited:
    return
  else:
    visited[curr_pos] = 1
    good_spots[curr_pos] = 1
    #explore up, down, left, right
    extend_good_spots_right((curr_pos[0]+1, curr_pos[1]),good_spots, all_obs, visited, width, height)
    return

def extend_good_spots_up(curr_pos, good_spots, all_obs, visited, width, height):
  if curr_pos[0] < 0 or curr_pos[0] >= width:
    return
  elif curr_pos[1] < 0 or curr_pos[1] >=height:
    return
  elif curr_pos in all_obs:
    return
  elif curr_pos in visited:
    return
  else:
    visited[curr_pos] = 1
    good_spots[curr_pos] = 1
    #explore up, down, left, right
    extend_good_spots_up((curr_pos[0], curr_pos[1]-1),good_spots, all_obs, visited, width, height)
    return

def extend_good_spots_down(curr_pos, good_spots, all_obs, visited, width, height):
  if curr_pos[0] < 0 or curr_pos[0] >= width:
    return
  elif curr_pos[1] < 0 or curr_pos[1] >=height:
    return
  elif curr_pos in all_obs:
    return
  elif curr_pos in visited:
    return
  else:
    visited[curr_pos] = 1
    good_spots[curr_pos] = 1
    #explore up, down, left, right
    extend_good_spots_down((curr_pos[0], curr_pos[1]+1),good_spots, all_obs, visited, width, height)
    return

# def extend_good_spots(curr_pos, good_spots, all_obs, visited, width, height):
#   if curr_pos[0] < 0 or curr_pos[0] >= width:
#     return
#   elif curr_pos[1] < 0 or curr_pos[1] >=height:
#     return
#   elif curr_pos in all_obs:
#     return
#   elif curr_pos in visited:
#     return
#   else:
#     visited[curr_pos] = 1
#     good_spots[curr_pos] = 1
#     #explore up, down, left, right
#     extend_good_spots((curr_pos[0]-1, curr_pos[1]),good_spots, all_obs, visited, width, height)
#     extend_good_spots((curr_pos[0]+1, curr_pos[1]),good_spots, all_obs, visited, width, height)
#     extend_good_spots((curr_pos[0], curr_pos[1]-1),good_spots, all_obs, visited, width, height)
#     extend_good_spots((curr_pos[0], curr_pos[1]+1),good_spots, all_obs, visited, width, height)
#     return



def degrees_of_freedom(coeff, big_pos, big_hh, all_obs, goal_pos, width, height):
  huge_pen = 10**25
  #LETS look at degrees of freedom instead
  #currently justy deals with obstacles, but lets add BOARD EDGEs, can also be getting blocked by other balls
  freedom = 4
  #check vertical blocking & horizontal blocking, i.e a door or a tunnel, do not punish unless direction 90 degrees
  #relative to block is also blocked
  blocked_vert = False
  blocked_horz = False

  if (big_pos[0],big_pos[1]-1) == goal_pos or (big_pos[0],big_pos[1]+1) == goal_pos:
    freedom -= 0
  #check if blocked by other obstacles or walls
  elif (big_pos[0],big_pos[1]-1) in all_obs or (big_pos[1]-1) < 0:
    #do not punish for being blocked on both sides(sometimes it is necessary)
    # if (big_pos[0],big_pos[1]+1) in all_obs or (big_pos[1]+1) >= height:
    #   freedom -= 0
    #   blocked_vert = True
    # else:
      freedom -= 2
  #if you cant go down, you also cant go up
  #Inverse applies if you cant go up thus, if both are present, it makes no difference
  elif (big_pos[0],big_pos[1]+1) in all_obs or (big_pos[1]+1) >= height:
    #do not punish for being blocked on both sides(sometimes it is necessary)
    # if (big_pos[0],big_pos[1]-1) in all_obs or (big_pos[1]-1) < 0:
    #   freedom -= 0
    #   blocked_vert = True
    # else:
      freedom -= 2

  if (big_pos[0]-1,big_pos[1]) == goal_pos or (big_pos[0]+1,big_pos[1]) == goal_pos:
    freedom -= 0
  #blocked left thus cant go right, either
  elif (big_pos[0]-1,big_pos[1]) in all_obs or (big_pos[0]-1) < 0:
    
    # if (big_pos[0]+1,big_pos[1]) in all_obs or (big_pos[0]+1) >= width:
    #   freedom -= 0
    #   blocked_horz = True
    # else:
      freedom -= 2
  elif (big_pos[0]+1,big_pos[1]) in all_obs or (big_pos[0]+1) >= width:
    
    # if (big_pos[0]-1,big_pos[1]) in all_obs or (big_pos[0]-1) < 0:
    #   freedom -= 0
    #   blocked_horz = True
    # else:
      freedom -= 2

  #return penalties
  if freedom == 0:
    return huge_pen
  elif freedom == 2:
    if coeff == 1:
      return big_hh
    elif blocked_vert or blocked_horz:
      return huge_pen

    return coeff**big_hh
  else:
    return 0

def hh_helper(good_spots, medium_pos, goal_pos, width, height):
    blocks_to_goal = 0
    if medium_pos in good_spots:
      blocks_to_goal += man_distance(medium_pos, goal_pos)
    else:
      vert = abs(medium_pos[0] - goal_pos[0])
      horz = abs(medium_pos[1] - goal_pos[1])

      #NOTE: might change this to if both (horizontal & vertical lines to good positions) exist, then pick min of those

      #is it a straight line (horizontal) path from here to a good spot
      if (medium_pos[0], goal_pos[1]) in good_spots:
        blocks_to_goal += man_distance(goal_pos, (medium_pos[0], goal_pos[1]))
        blocks_to_goal += man_distance((medium_pos[0], goal_pos[1]), medium_pos)
        #great, good, but still penalized, but less

      #is it a straight line (vertical) path from here to a good spot
      elif (goal_pos[0], medium_pos[1]) in good_spots:
        blocks_to_goal += man_distance(goal_pos, (goal_pos[0], medium_pos[1]))
        blocks_to_goal += man_distance((goal_pos[0], medium_pos[1]), medium_pos)

      else:
        blocks_to_goal += width*height

    return blocks_to_goal

def check_for_dead_ends(snowball_pos, all_obs, width, height, goal):

    left_surr = False
    right_surr = False
    up_surr = False
    down_surr = False

    #flags to check where im surrounded
    if (snowball_pos[0]-1,snowball_pos[1]) in all_obs:
      left_surr = True
    if (snowball_pos[0]+1,snowball_pos[1]) in all_obs:
      right_surr = True
    if (snowball_pos[0], snowball_pos[1]-1) in all_obs:
      up_surr=True
    if (snowball_pos[0], snowball_pos[1]+1) in all_obs:
      down_surr = True   

    huge_pen = 10**25
    #4 corners on board
    if snowball_pos[0] == 0 and snowball_pos[1] == 0 and goal != snowball_pos:
      return huge_pen
    elif snowball_pos[0] == (width - 1) and snowball_pos[1] == 0 and goal != snowball_pos:
      return huge_pen
    elif snowball_pos[0] == 0 and snowball_pos[1] == (height - 1) and goal != snowball_pos:
      return huge_pen
    elif snowball_pos[0] == (width - 1) and snowball_pos[1] == (height - 1) and goal != snowball_pos:
      return huge_pen
    #check for walls, once you push onto a wall, you cant push off
    #same goes for artificial walls introdued by obstacles (how to deal with these)
    elif snowball_pos[0] == 0 and goal[0] != snowball_pos[0]:
      return huge_pen
    elif snowball_pos[0] == (width - 1) and goal[0] != snowball_pos[0]:
      return huge_pen
    elif snowball_pos[1] == 0 and goal[1] != snowball_pos[1]:
      return huge_pen
    elif snowball_pos[1] == (height - 1) and goal[1] != snowball_pos[1]:
      return huge_pen

    #goal check it avoid redundancy
    elif snowball_pos == goal:
      return 0

    #TODO: CHECK FOR DEADLOCKS MADE BY WALLS AND AN OBSTACLE
    #checks for corners made by walls and obstacles
    #beside a vertical wall and blocked
    elif snowball_pos[0] == 0  and (up_surr or down_surr):
      return huge_pen
    elif snowball_pos[0] == (width - 1) and (up_surr or down_surr):
      return huge_pen
    elif snowball_pos[1] == 0 and (left_surr or right_surr):
      return huge_pen
    elif snowball_pos[1] == (height - 1) and (left_surr or right_surr):
      return huge_pen 

#    ADD THIS IN------------------------------------------------------------------------------------------------
    #check for deadlocks made by obstacles
    #checking for artificial corners made by obstacles 
    #surrounded up and left
    elif left_surr and up_surr:
      return huge_pen
    #surrounded up and right
    elif right_surr and up_surr:
      return huge_pen
    #down and left
    elif left_surr and down_surr:
      return huge_pen
    #down and right
    elif right_surr and down_surr:
      return huge_pen
         

    # elif snowball_pos[0] == 0
    #check for corners cr
    else:

      # #case 1 stuck in top right: blocked in top right, on right, and above
      # if ((snowball_pos[0] + 1, snowball_pos[1]-1) in obstacles) and ((snowball_pos[0] + 1, snowball_pos[1]) in obstacles) and ((snowball_pos[0], snowball_pos[1]-1)):
      #   return huge_pen
      # #case 2 stuck in bottom right: blocked: bottom right, right and bottom
      # elif ((snowball_pos[0] + 1, snowball_pos[1]+1) in obstacles) and ((snowball_pos[0] + 1, snowball_pos[1]) in obstacles) and ((snowball_pos[0], snowball_pos[1]+1)):
      #   return huge_pen
      # #stuck in top left: blocked top left, top, left
      # if ((snowball_pos[0] - 1, snowball_pos[1]-1) in obstacles) and ((snowball_pos[0], snowball_pos[1]-1) in obstacles) and ((snowball_pos[0]-1, snowball_pos[1]) in obstacles):
        # return huge_pen
      # #stuck in bottom left due to objects in obstacles set: blocked: bottom left, bottom and left
      # elif ((snowball_pos[0] - 1, snowball_pos[1]+1) in obstacles) and ((snowball_pos[0], snowball_pos[1]+1) in obstacles) and ((snowball_pos[0]-1, snowball_pos[1])):
      #   return huge_pen
      # #checking 1 block blocking me due to board & 1 due to obstacle
      # #top right
      # else:
      return 0

def get_position(snowballs_on_board, get_pos, indices):
    
    #loop over all indices and see which exist on board
    for index in indices:
      if snowballs_on_board[index][1]:
        return get_pos[index]
    
    #will never get hit
    return None
      

def man_distance(where_from, where_to):
    return abs(where_from[0] - where_to[0]) + abs(where_from[1] - where_to[1])

def heur_zero(state):
    '''Zero Heuristic can be used to make A* search perform uniform cost search'''
    return 0

def fval_function(sN, weight):
#IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
    # print(dir(sN))

  
    #Many searches will explore nodes (or states) that are ordered by their f-value.
    #For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    #You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    #The function must return a numeric f-value.
    #The value will determine your state's position on the Frontier list during a 'custom' search.
    #You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    return (sN.gval + weight * sN.hval)

def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound = 5):
#IMPLEMENT
  '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
  '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  '''implementation of weighted astar algorithm'''
  print(initial_state)
  print(initial_state.print_state())
  print(initial_state.obstacles)
  max_size = 10**6
  # costing = 75
  costs = (max_size,max_size,max_size)
  #define starting and ending times
  init_time = os.times()[0]
  ending = init_time + timebound
  #best_first with full cycle_checking
  #best_first
  se = SearchEngine(strategy="custom", cc_level="full")
   #can we find something
  se.init_search(initial_state, snowman_goal_state, heur_fn, (lambda sN : fval_function(sN,30)))
  v = se.search(timebound=timebound)

  if not v:
    print(f"Not found returned")
    return False
  else:
    # print(dir(v))
    # print(v.gval)
    # print(heur_fn(v))
    #update pruning values
    costs = (v.gval, max_size, max_size)
  
  #update timebound
  time_to_solve = os.times()[0] - init_time
  # print(f"Time to solve First one: {time_to_solve}")
  timebound = (ending - os.times()[0])
  # print(f"First TimeBound: {timebound}")

  best_thus_far = v

  while timebound > time_to_solve:
    v = se.search(timebound=timebound, costbound=costs)
    #if no better solution is found, we return our best found solution to date
    if not v:
      print(f"Returned: {best_thus_far.gval}")
      return best_thus_far

    #prune based on g-value
    elif v.gval < costs[0]:
      costs = (v.gval, max_size, max_size)
      best_thus_far = v
    # print(f"Gval: {v.gval}")
    
    #update timebound
    timebound = (ending - os.times()[0])
    # print(f"TimeBound: {timebound}")


  
  print(f"Returned: {best_thus_far.gval}")
  return best_thus_far

  
def anytime_gbfs(initial_state, heur_fn, timebound = 5):
#IMPLEMENT
  '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
  '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  '''implementation of weighted astar algorithm'''
  print(initial_state)
  print(initial_state.print_state())
  print(initial_state.obstacles)
  costing = 30
  max_size = 10**6
  # costing = 75
  costs = (max_size,max_size,max_size)
  #define starting and ending times
  init_time = os.times()[0]
  ending = init_time + timebound
  #best_first with full cycle_checking
  #best_first
  se = SearchEngine(strategy="best_first", cc_level="full")
  #initialize the search & run it without a bound

  #can we find something
  se.init_search(initial_state, snowman_goal_state, heur_fn)
  v = se.search(timebound=timebound)
  

  if not v:
    print(f"Not found returned")
    return False
  else:
    costs = (v.gval, max_size, max_size)
  
  #update timebound
  time_to_solve = os.times()[0] - init_time
  # print(f"Time to solve First one: {time_to_solve}")
  timebound = (ending - os.times()[0])
  # print(f"First TimeBound: {timebound}")

  best_thus_far = v

  while timebound > time_to_solve:
    v = se.search(timebound=timebound, costbound=costs)
    #if no better solution is found, we return our best found solution to date
    if not v:
      print(f"Returned: {best_thus_far.gval}")
      return best_thus_far

    #prune based on g-value
    elif v.gval < costs[0]:
      costs = (v.gval, max_size, max_size)
      best_thus_far = v
    # print(f"Gval: {v.gval}")
    
    #update timebound
    timebound = (ending - os.times()[0])
    # print(f"TimeBound: {timebound}")


  
  print(f"Returned: {best_thus_far.gval}")
  return best_thus_far

  
    
