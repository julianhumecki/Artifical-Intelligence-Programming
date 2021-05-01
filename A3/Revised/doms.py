
from cspbase import *
from propagators import prop_FC,  prop_GAC, ord_mrv
import itertools


def construct_q2():
	vals = [1,2,3,4,5]
	a = Variable("A",vals)
	b = Variable("B", vals)
	c = Variable("C",vals)
	d = Variable("D",vals)
	e = Variable("E",vals)

	c1 = Constraint("C1",[a,b])
	c2 = Constraint("C2",[d,a])
	c3 = Constraint("C3",[e,a,b])
	c4 = Constraint("C4",[e,c,d])
	c5 = Constraint("C5",[e,d])
	#c1
	satisfiers = list()
	for t in itertools.product(a.cur_domain(), b.cur_domain()):
		#use binary not equal to constraints
		if t[0] > t[1]:
		  # print("HI")
		  satisfiers.append(t)

	c1.add_satisfying_tuples(satisfiers)
	#c2
	satisfiers = list()
	for t in itertools.product(d.cur_domain(), a.cur_domain()):
		#use binary not equal to constraints
		if t[0] > t[1]:
		  # print("HI")
		  satisfiers.append(t)

	c2.add_satisfying_tuples(satisfiers)

	#c3
	satisfiers = list()
	for t in itertools.product(e.cur_domain(), a.cur_domain(),b.cur_domain()):
		#use binary not equal to constraints
		if t[0] == t[1] + t[2]:
		  # print("HI")
		  satisfiers.append(t)

	c3.add_satisfying_tuples(satisfiers)

	#c4
	satisfiers = list()
	for t in itertools.product(e.cur_domain(), c.cur_domain(),d.cur_domain()):
		#use binary not equal to constraints
		if t[0] < t[1] + t[2]:
		  # print("HI")
		  satisfiers.append(t)

	c4.add_satisfying_tuples(satisfiers)

	#c5
	satisfiers = list()
	for t in itertools.product(e.cur_domain(), d.cur_domain()):
		#use binary not equal to constraints
		if t[0] != t[1]:
		  # print("HI")
		  satisfiers.append(t)

	c5.add_satisfying_tuples(satisfiers)


	my_csp = CSP("model_q2")
	my_csp.add_var(a)
	my_csp.add_var(b)
	my_csp.add_var(c)
	my_csp.add_var(d)
	my_csp.add_var(e)

	my_csp.add_constraint(c1)
	my_csp.add_constraint(c2)
	my_csp.add_constraint(c3)
	my_csp.add_constraint(c4)
	my_csp.add_constraint(c5)

	return my_csp

my_problem = construct_q2()
# prop_GAC(my_problem)

all_vars = my_problem.get_all_vars()
# print("After GAC enforce")
# for var in all_vars:
	# print(var.cur_domain())

solver = BT(my_problem)
print("=======================================================")
print("GAC")
solver.bt_search(prop_GAC, var_ord=ord_mrv)
print("Solution")
for var in all_vars:
	print(var.cur_domain())