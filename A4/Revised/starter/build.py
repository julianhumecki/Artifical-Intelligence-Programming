def builder(args):
	out = ""
	for i,arg in enumerate(args):
		if arg == "":
			out += ":"
		elif i != len(args)-1:
			out += arg + ":"
		else:
			out += arg + " "
	return out

print(builder(["fuck","","","dick","rider ", " cow\n"]))
original = "fuck*:* : NPO"
print(original == builder(original.split(":")))