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
	return spoly

# give the first n angles associated with a given spread.
# for example 3/4 is associated with 60, 120, 180+60 (240), 180+120 (300), etc.
def associated_angles(spread,n):
	sinus = sqrt(spread).evalf()
	angle_in_radians = asin(sinus)
	angle_in_degrees = 180.0*angle_in_radians/math.pi
	supplement = 180.0 - angle_in_degrees
	tmp,tmp2 = angle_in_degrees,supplement
	angles = ()
	while len(angles)<n:
		angles += (tmp,)
		if len(angles)<n:
			angles += (tmp2,)
		tmp += 180.0
		tmp2 += 180.0
	return angles

n=3
spreadpoly = spread_poly(n)
startspread = Rational(3,4)
#startspread = Rational(1,1)
startspread = Rational(1,144)
#startspread = Rational(0,1)

print('Starting spread =',startspread)
print('Associated angles: ' + '%4.1f° '*n % associated_angles(startspread,n)+'...')
print('Spread polynomial (factored): S_ '+str(n)+' =',factor(spreadpoly))
print('Spread polynomial (plain   ): S_ '+str(n)+' =',expand(spreadpoly))
print('Solving equation',spreadpoly,'=',startspread)
spreads=[]
#spreads=solve(spreadpoly-spread,s)
#for i in range(len(spreads)): print(i,spreads[i])
roots=Poly(spreadpoly-startspread).all_roots(multiple=True)
for i in range(len(roots)):
	rootspread = roots[i]
	print( 'root',str(i+1)+': s  =',rootspread )
	print( 'root',str(i+1)+': s ~=',rootspread.evalf() )
	angles = associated_angles( rootspread,1 )
	print( 'associated angle: '+ '%4.1f° ' % angles,end=' ')
	print( 'x %i:' %n , '%4.1f°' % (angles[0]*n))
	#angle1 = 180*(math.asin(+sinus))/math.pi

