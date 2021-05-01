
class Node:
	def __init__(self, name, h_val, nodes):
		self.name = name
		self.h_val = h_val
		self.nodes = nodes



def build_run():

	G1 = Node("G1",h_val=7,nodes=[])
	G2 = Node("G2",h_val=7,nodes=[])
	A = Node("A",h_val=7,nodes=[E, G1])
	A = Node("A",h_val=7,nodes=[E, G1])


	C = Node("A",h_val=7,nodes=[G3])
	B = Node("A",h_val=7,nodes=[C, F])
	D = Node("A",h_val=7,nodes=[B, G2])
	A = Node("A",h_val=7,nodes=[E, G1])

	S = Node("S",h_val=7,nodes=[A, B, C, D])
