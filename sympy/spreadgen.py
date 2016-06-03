# symbolically calculate the spread polynomial S_N given n

# using the Explicit Formula, p 106 of Divine Proportions, Norman J Wildberger

from sympy import *
s,r,C,D,n=symbols('s,r,C,D,n')

r=sqrt(4*s*(1-s))
C=1-2*s+I*r
D=1-2*s-I*r

def spread_poly(n):
	spoly = (2 - C**n - D**n)/4
	return spoly
for i in range(0,24):
	print i,factor(spread_poly(i))
	print i,simplify(spread_poly(i))
	print i,solve(spread_poly(i),s)
