
def rec(t, vals, base):
	if t == 1:
		return base[0], base[1]

	b = rec(t-1, vals, base)
	sun = vals[0]*b[0] + vals[1]*b[1]
	rain = 1 - sun
	return sun,rain


print(rec(200, [0.8, 0.4], [0,1]))
