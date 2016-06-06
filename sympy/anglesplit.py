# show that solving a spread polynomial will produce interesting
# possibilities for the corresponding angles involved.
#
# For example Spread Polynomial S2 is 4s(1-s).
# Consider the spread 3/4 which corresponds to 60 degree angle and
# also to a 120 degree angle simultaneously.
# Solving S2=3/4 produces two results, s=1/4 and s=3/4.
# s=1/4 corresponds to a 30 degree angle, which is half of 60 degrees.
# s=3/4 corresponds to a 60 degree angle, which is half of 120 degrees.
# of course you could say 1/4 also corresponds to a 150 degree angle
# and 3/4 corresponds to a 120 degree angle. But leave that for another time.
# Also -60 and 60 are ... kind of the same thing, but also leave that for
# another time.
#
# The tricky bit is that solving a spread polynomial often produces multiple
# results. If the polynomial has an s^5 then it is of 'degree 5' in math
# language, which also means it can have 5 different solutions.
#
# What does that mean for this idea of corresponding angles?
# Basically it means you get 5 different versions of "1/5 of the angle".
# For example solving S5=3/4 produces 5 spreads
# [3/4,
#  -sqrt(5)/16 + sqrt(-3*sqrt(5)/128 + 15/128) + 7/16
#  -sqrt(5)/16 - sqrt(-3*sqrt(5)/128 + 15/128) + 7/16
#   sqrt(5)/16 + sqrt( 3*sqrt(5)/128 + 15/128) + 7/16
#   sqrt(5)/16 - sqrt( 3*sqrt(5)/128 + 15/128) + 7/16]
#
# These correspond to angles of 84,60,48,24, and 12 degrees (not in that order).
# Those are each 1/5 of 420,300,240,120,60
# But 420,300,240,120, and 60 can all be thought of as corresponding to the
# original spread of 3/4.

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
	return factor(spoly)

def anglefy(sympyspread):
	spreadvalue = complex(sympyspread.evalf()).real
	sinus = math.sqrt( spreadvalue )
	# ignore the negative root, it's ok
	angle1 = 180*(math.asin(sinus))/3.14159
	return angle1 #,angle2

n=5
spreadpoly=spread_poly(n)

spread=Rational(3,4)
print('Solving ',spreadpoly,'=',spread)
spreads=solve(spreadpoly-spread,s)
print(spreads)
print(anglefy(spread),end=' -> ')
newangles = []
for sp in spreads: newangles += [anglefy(sp)]
for m in newangles: print(m,end=' ')
print()
print('             ',end=' ')
for m in newangles: print(m*n,end=' ')
print()
