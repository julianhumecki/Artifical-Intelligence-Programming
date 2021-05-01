#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.  

'''
Construct and return Tenner Grid CSP models.
'''

from cspbase import *
import itertools

#do we check against bs inputs?

def tenner_csp_model_1(initial_tenner_board):

  #extrac last row  
  last_row = initial_tenner_board[1]

  # print(initial_tenner_board)
  variable_array = list()
  #loop over board and assign values
  for i in range(0, len(initial_tenner_board[0])):
    sub_var_array = list()
    vals = [0,1,2,3,4,5,6,7,8,9]
    vals = prune_row(initial_tenner_board[0][i], vals)
    for j in range(0, len(initial_tenner_board[0][i])):
      if initial_tenner_board[0][i][j] == -1:
        sub_var_array.append(Variable(f"{i},{j}", vals))
      else:
        val = initial_tenner_board[0][i][j]
        var = Variable(f"{i},{j}", [val])
        sub_var_array.append(var)

    #append list to list
    variable_array.append(sub_var_array.copy())


  #specify constaints, each column must sum to value of column at n+1, each row must have unique 0-9
  #adjacent cells must have different values
  # print(variable_array)

  #row constraints, binary not equal to constraints for rows
  #0,0 != 0,1
  my_constraints = list() 
  #add binary not equal to constraints
  for i in range(len(variable_array)):
    my_constraints += add_row_b_constraints(variable_array[i], i)

  # print(f"Binary row len const: {len(my_constraints)}")
  temp = len(my_constraints)
  #add binary contiguous cell constraints
  contig = list()
  for i in range(len(variable_array)):
    for j in range(len(variable_array[i])):
      contig += add_contig_b_constraints(variable_array, i, j)

  my_constraints += contig

  # print(f"Adj cons len const: {len(my_constraints) - temp}")

  #add column constraints
  for j in range(0, 10):
    my_constraints += add_column_constraints(variable_array, j, last_row[j])
  
  # print(f"LEN CONST: {len(my_constraints)}")
  # print(*my_constraints)
  my_csp = CSP("tenner csp model 1")
  for entry in variable_array:
    for var in entry:
      #add variable
      my_csp.add_var(var)

  for cons in my_constraints:
    #add constraint
    my_csp.add_constraint(cons)


#TODO: FIGURE OUT WHY MODEL DOESN"T SOLVE CSP
  return my_csp, variable_array

def add_row_b_constraints(vars_in_row, row):
  size = 10
  #initialize constraint
  all_cons = list()
  #loop over all spots
  for i in range(0, size):
    for j in range(i+1, size):
      cons = Constraint(f"BNotEqualToRowConst row={row}, i={i}, j={j}", [vars_in_row[i],vars_in_row[j]])
      those_that_satisfy = list()
      for t in itertools.product(vars_in_row[i].cur_domain(), vars_in_row[j].cur_domain()):
        #use binary not equal to constraints
        if t[0] != t[1]:
          those_that_satisfy.append(t)

      #add tuples
      cons.add_satisfying_tuples(those_that_satisfy)
      all_cons.append(cons)
  #one constraint per row
  return all_cons


def add_contig_b_constraints(variable_array, row, col):
  valid_adj_pos = get_valid_adj_vars(variable_array, row, col)
  all_adj_const = list()
  my_var = variable_array[row][col]
  #loop over the variables of interest
  for i in range(len(valid_adj_pos)):      
        cons = Constraint(f"Adj Const row={row}, col={col};", [my_var, valid_adj_pos[i]])
        cons.add_satisfying_tuples(two_vars(my_var, valid_adj_pos[i]))
        all_adj_const.append(cons)

  return all_adj_const

def add_column_constraints(variable_array, col, total):
  all_vars = get_vars_in_col(variable_array, col)
  doms = list()
  #create constraint
  cons = Constraint(f"Col const {col}", all_vars)
  for var in all_vars:
    doms.append(var.cur_domain())
  #loop over all choices
  satisfy_tups = list()
  for t in itertools.product(*doms):
    if sum(t) == total:
      satisfy_tups.append(t)
  
  cons.add_satisfying_tuples(satisfy_tups)

  return [cons]


def two_vars(var_one, var_two):
  satisfiers = list()
  for t in itertools.product(var_one.cur_domain(), var_two.cur_domain()):
    #use binary not equal to constraints
    if t[0] != t[1]:
      # print("HI")
      satisfiers.append(t)
  
  return satisfiers

def get_valid_adj_vars(variable_array, i, j):
  valid = list()
  if i > 0:

    if j > 0:
      valid.append(variable_array[i-1][j-1])

    valid.append(variable_array[i-1][j])

    if j < len(variable_array[i])-1:
      valid.append(variable_array[i-1][j+1])
  
  #add variables underneath
  if i < len(variable_array) - 1:
    if j > 0:
      valid.append(variable_array[i+1][j-1])

    valid.append(variable_array[i+1][j])

    if j < len(variable_array[i])-1:
      valid.append(variable_array[i+1][j+1])

  return valid




def get_vars_in_col(variable_array, col):
  all_vars = list()
  #loop over column
  for i in range(len(variable_array)):
    all_vars.append(variable_array[i][col])
  return all_vars


def prune_row(arr, vals):
  rem = set(vals)
  for elems in arr:
    rem = rem - set([elems])
  return list(rem)


##############################
def is_unique(values):
  ss = set(values)
  return len(ss) == len(values)

def add_row_constraints(variable_array, row):
  cons = Constraint(f"Row const {row}", variable_array)
  doms = list()

  for var in variable_array:
    doms.append(var.cur_domain())
  #loop over all choices
  satisfy_tups = list()
  for t in itertools.product(*doms):
    if is_unique(t):
      satisfy_tups.append(t)
  
  cons.add_satisfying_tuples(satisfy_tups)
  return [cons]




def tenner_csp_model_2(initial_tenner_board):
    
  #extrac last row  
  last_row = initial_tenner_board[1]

  variable_array = list()
  #loop over board and assign values
  for i in range(0, len(initial_tenner_board[0])):
    sub_var_array = list()
    vals = [0,1,2,3,4,5,6,7,8,9]
    vals = prune_row(initial_tenner_board[0][i], vals)
    for j in range(0, len(initial_tenner_board[0][i])):
      if initial_tenner_board[0][i][j] == -1:
        sub_var_array.append(Variable(f"{i},{j}", vals))
      else:
        val = initial_tenner_board[0][i][j]
        var = Variable(f"{i},{j}", [val])
        sub_var_array.append(var)

    #append list to list
    variable_array.append(sub_var_array.copy())


  #specify constaints, each column must sum to value of column at n+1, each row must have unique 0-9
  #adjacent cells must have different values
  # print(variable_array)

  #row constraints, n-ary all not equal to
  my_constraints = list() 
  #add binary not equal to constraints
  for i in range(len(variable_array)):
    my_constraints += add_row_constraints(variable_array[i], i)

  # print(f"Binary row len const: {len(my_constraints)}")
  temp = len(my_constraints)
  #add binary contiguous cell constraints
  contig = list()
  for i in range(len(variable_array)):
    for j in range(len(variable_array[i])):
      contig += add_contig_b_constraints(variable_array, i, j)

  my_constraints += contig

  # print(f"Adj cons len const: {len(my_constraints) - temp}")

  #add column constraints
  for j in range(0, 10):
    my_constraints += add_column_constraints(variable_array, j, last_row[j])
  
  # print(f"LEN CONST: {len(my_constraints)}")
  # print(*my_constraints)
  my_csp = CSP("tenner csp model 2")
  for entry in variable_array:
    for var in entry:
      #add variable
      my_csp.add_var(var)

  for cons in my_constraints:
    #add constraint
    my_csp.add_constraint(cons)


#TODO: FIGURE OUT WHY MODEL DOESN"T SOLVE CSP
  return my_csp, variable_array

