#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.  

'''This file will contain different constraint propagators to be used within 
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method). 
      bt_search NEEDS to know this in order to correctly restore these 
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been 
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated 
        constraints) 
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope 
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
     
     
var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable 

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no 
    propagation at all. Just check fully instantiated constraints'''
    
    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

#TODO: WHAT TO DO ABOUT DOMAIN WIPE OUTS, DO WE JUST RETURN OR CONTINUE?
def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with 
       only one uninstantiated variable. Remember to keep 
       track of all pruned variable,value pairs and return '''
    #check constraints that have one unassigned variable, then prune based on that
    constraints_of_interest = None
    #if variable passed into newvar, only get 
    if newVar:
      constraints_of_interest = csp.get_cons_with_var(newVar)
    else:
      constraints_of_interest = csp.get_all_cons()

    #check which of these constraints only have one unassigned variable
    constraints_of_interest = constraints_with_one_unassigned(constraints_of_interest)

    # print(f"LEN: {len(constraints_of_interest)}")
    pruned = list()
    for con in constraints_of_interest:
      #there will only be one unassigned var as per requirements
      un_var = con.get_unasgn_vars()[0]
      values = un_var.cur_domain()
      #try each value
      for val in values:
        satis = con.has_support(un_var, val)
        #if no support (no satisfying assignments for un_var=var), prune it
        if not satis:
          un_var.prune_value(val)
          #add to pruned
          pruned.append((un_var, val))
          #check if domain wipe out, then return
          if un_var.cur_domain_size() == 0:
            return False, pruned


    return True, pruned



#loop over all constraints, return only those with one unassigned value
def constraints_with_one_unassigned(constraints):

  of_interest = list()
  for cons in constraints:
    if cons.get_n_unasgn() == 1:
      of_interest.append(cons)
  return of_interest


def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce 
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
    constraints_of_interest = None
    if newVar:
      constraints_of_interest = csp.get_cons_with_var(newVar)
    else:
      constraints_of_interest = csp.get_all_cons()
    # print(*constraints_of_interest)
    con = constraints_of_interest[0]
    # print(con)
    # print(con.sat_tuples)
    # for c in con.get_scope():
    #   print(c)
    #   print(c.get_assigned_value())
    #   print(c.cur_domain())

    # for var in con.get_scope():
    #     for val in var.cur_domain():
    #       assign_found = con.has_support(var, val)
    #       if not assign_found:
    #         print(f"not found: {var}, {val}")

    q = Queue(constraints_of_interest)
    pruned = list()
    i = 0
    while not q.is_empty():
      con = q.dequeue()
      # print(f"Here we are: {con}, i= {i}")
      # print(f"Scope: {con.scope}")
      i+=1
      # print(type(con))
      for var in con.get_scope():
        for val in var.cur_domain():
          assign_found = con.has_support(var, val)
          if not assign_found:
            var.prune_value(val)
            pruned.append((var, val))
            #eventually
            if var.cur_domain_size() == 0:
              # print(f"FUCK: {var}")
              # print(var)
              #if DOW return, as per slides
              return False, pruned
            else:
              #push all constraints if var V in their scope onto queue, if not already in queue
              the_ones = has_var_v(constraints_of_interest, var)
              q.enqueue_nonreplicating_to_list(the_ones)

    return True, pruned

def has_var_v(constraints, var):
  the_ones = list()
  for con in constraints:
    if var in con.get_scope():
      the_ones.append(con)
  return the_ones

class Queue:
  
  def __init__(self, elems=[]):
    self.queue = elems
  
  def dequeue(self):
    if self.size() == 0:
      return -1 
    val = self.queue[0]
    self.queue = self.queue[1:]
    return val
  
  def enqueue(self, val):
    self.queue.append(val)
    return 1
  
  def size(self):
    return len(self.queue)
  
  def is_empty(self):
    return (self.size() == 0)

  def enqueue_nonreplicating_to_list(self, elems):
    for elem in elems:
      if not (elem in self.queue):
        self.queue.append(elem)
    return 1 

  def __str__(self):
    return ""+str(self.queue)+""


def ord_mrv(csp):
    ''' return variable according to the Minimum Remaining Values heuristic '''
    all_vars = csp.get_all_unasgn_vars()
    least_count = float("inf")
    min_var = None
    for var in all_vars:
      pot_min = var.cur_domain_size()
      if pot_min < least_count:
        least_count = pot_min
        min_var = var
    return min_var