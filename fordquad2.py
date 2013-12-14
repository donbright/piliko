from piliko import *

# ford circles, descartes circles, and the triple quad formula.

# this is a similar experiment to fordtrip.py
# but with major tweaks.

# From Descartes, given 3 kissing circles w curvatures k1,k2,k3:
# you can find a fourth circle w curvature k4:
#
# k4 = k1 + k2 + k3 +/- sqrt( k1*k2 + k2*k3 + k3*k1 )

# written another way:
#
# k4a = k1 + k2 + k3 + sqrt( k1*k2 + k2*k3 + k3*k1 )
# k4b = k1 + k2 + k3 - sqrt( k1*k2 + k2*k3 + k3*k1 )
#

# note that when you add k4a and k4b, sqrt is cancelled and you get 
#
# k4a+k4b = 2 * (k1+k2+k3)
#
# Thus, even if the sqrt() is irrational, the sum of the new k4s is rational.
#
#

# That's fine for curvatures, but what about an alternative geometric
# interpretation, taken from Wildberger's Triple Quad formula?

# 2*(Q1^2+Q2^2+Q3^2) = (Q1+Q2+Q3)^2
#
#
# Given three Rhobuses with quadrances Q1, Q2, Q3, what is Q4, if we
# set the curvatures of the kissing circles = to the Quadrances?
# 

# Q4a and Q4b then are quadrances, and q4a is often negative. But Quadrances
# are 'signed area', not just area. So it's OK to be negative. 
#

# If you add the two areas together, it is like taking a 'negative rhombus'
# and adding it to a 'positive rhombus'. The negative rhombus eats a chunk
# out of the positive Rhombus. The area of the final, chunk-eaten-out
# Rhombus, is equal to Twice the Area of the other three Rhombuses added.
#
# Tada.

from piliko import *
import math

sequence = farey_sequence(4)
for x in sequence: print x,
print

def fakesqrt(x): return 1

for i in range(0,len(sequence)-2):
	a,b,c = sequence[i],sequence[i+1],sequence[i+2]

	# make sure we get only Kissing circles:
	if not b.numerator==a.numerator+c.numerator: continue
	if not b.denominator==a.denominator+c.denominator: continue

	# radius of a Ford circle = 1/(2*square of denominator of x coordinate) 
	# curvature of any circle = 1/radius
	curvature1 = 2*sqr(a.denominator)
	curvature2 = 2*sqr(b.denominator)
	curvature3 = 2*sqr(c.denominator)
	Q1,Q2,Q3 = curvature1,curvature2,curvature3
	#Q4a = Q1+Q2+Q3 + 2 * babylonian_square_root( Q1*Q2+Q2*Q3+Q3*Q1 )
	#Q4b = Q1+Q2+Q3 - 2 * babylonian_square_root( Q1*Q2+Q2*Q3+Q3*Q1 )
	print 'Ford circle x coords:', a,b,c
	print ' Original curvatures:',Q1,Q2,Q3
	Q2 = Q2 - 2
	print ' Modified curvatures:',Q1,Q2,Q3
	print ' 3 Kissing circle curvatures:',Q1,Q2,Q3,'->Quadrances of 3 Rhombi'
	# since we are going to add Q4a to Q4b, we dont need to actually
	# calculate the square root. since these roots tend to be Irrational
	# Numbers, and we dont have a symbolic system here, we just 'fake'
	# the square root to be the number 1. The result of the Addition
	# is the same because the terms cancel each other when Q4a, Q4b are added
	Q4a = Q1+Q2+Q3 + 2 * fakesqrt( Q1*Q2+Q2*Q3+Q3*Q1 )
	Q4b = Q1+Q2+Q3 - 2 * fakesqrt( Q1*Q2+Q2*Q3+Q3*Q1 )
	#print ' Fourth Circle Curvatures a,b:',Q4a,Q4b,' Ratio Q4a to Q1+Q2+Q3:',Fraction(Q4a,Q1+Q2+Q3)
	print ' Q4a+Q4b :', Q4a+Q4b
	print ' Q1+Q2+Q3 :', Q1+Q2+Q3
	print ' Ratio Q4a+Q4b to Q1+Q2+Q3: ',Fraction(Q4a+Q4b,Q1+Q2+Q3)
	# ratio should always be two
	# Q4b should always be 0 (the Ford Circles touch this line,
	#  the line being a circule of curvature 0, and thus infinite radius)

	# ??????????
	print ' Quadrea: ',Quadrea(Q1,Q2,Q3)
