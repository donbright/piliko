# print out factors of the coefficients of spread polynomials.

from sympy import *
import math

s=symbols('s')

# create the nth spread polynomial, in Sympy style,
# using the Explicit Formula, p 106 of Divine Proportions, Norman J Wildberger
def spread_poly(n):
	s,r,C,D=symbols('s,r,C,D')
	r=sqrt(4*s*(1-s))
	C=1-2*s+I*r
	D=1-2*s-I*r
	spoly = Rational(1,4)*(2 - C**n - D**n)
	return spoly

n=38
spreadpoly = spread_poly(n)
startspread = Rational(0,1)

print('Spread polynomial (factored): S_ '+str(n)+' =',factor(spreadpoly))
print('Spread polynomial (plain   ): S_ '+str(n)+' =',expand(spreadpoly))
coefficients = Poly(spreadpoly).coeffs()
for c in coefficients:
	factors = factorint(c)
	print(c,end=' ')
	for k in sorted(factors.keys()):
		print(str(k),end='')
		if (factors[k]!=1): print('**'+str(factors[k]),end=' ')
		else: print(end=' ')
	print()
