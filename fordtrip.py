from piliko import *

# ford circles, descartes circles, and the triple quad formula.


# Before reading this, please google Ford Circles, Descartes Kissing Circles,
# and Rational Trigonometry Triple Quad Formula


# What we are doing here, is basically running an experiment to see if the
# Fourth Kissing Circle of three Kissing Ford circles follows a certain pattern,
# namely,
# 
# Curvature( fourth circle ) = 2 * sum of curvatures of other three.
#
# Why? Because if its true, then you can associate 3 rhombuses with the 
# 3 Kissing Circles, set the Rhombus Quadrance = to Circle Curvature, 
# and a Fourth Rhombus that follows the pattern will have twice the 
# Quadrance (signed area) of the other three combined.



# In Descarte's letter to Princess of Bohemia:
#
# 4 mutually tangent circles have curvatures that meet this formula:
#
# 2*(k1^2+k2^2+k3^2+k4^2)=(k1+k2+k3+k4)^2
#
# Ford Circles are Descartes circles with one of the k's set to 0,
# resulting in a 'circle of infinite radius', aka, a straight line.
#
# In this case, the formula changes:
#
# 2*(k1^2+k2^2+k3^2)=(k1+k2+k3)^2
# 
#
# This is identical to the Triple Quad formula for Quadrances
# aka 'signed area of Rhombuses' in the plane.
#
# 2*(Q1^2+Q2^2+Q3^2)=(Q1+Q2+Q3)^2
#
# In Blue Geometry, the quadrance will be the area of a square and
# the side lengths of two of the squares will exactly add to the side length 
# of the third, making 3 collinear points.
# 
# But note, here, that Descarte's formula actually can take any three tangent
# circles and provide 'two options' for drawing a fourth circle.
#
# Given k1,k2,k3, we can solve for k4 using the old fashioned quadratic formula:
#
# k4 = k1 + k2 + k3 +/- 2 * sqrt( k1*k2 + k2*k3 + k3*k1 )
# 
# k4 can be 0... as in the Ford circles.. but what about the tiny little
# circle you could fit 'inbetween' the ford circles that is tangent to all three?
#
# k4 = k1 + k2 + k3 + 2*sqrt( k1*k2 + k2*k3 + k3*k1 )
# 
# Well, it turns out that for Ford circles, k4 is always 2 ( k1+k2+k3 )
#
# What if we translate that back into our Quadrances?
#
# Given three Rhombuses with Quadrances meeting the Triple Quad formula,
# there are two possible 'fourth' rhombuses to meet Descarte's formula.
# Quadrance = 0, or Quadrance = 2*(Q1+Q2+Q3)
# 
# In other words, the 'inner' Descarte's circle corresponds to a Rhombus
# with twice the area of the other three Rhombuses put together. 
#
# Let's test it.

from piliko import *
import math

sequence = farey_sequence(15)
for x in sequence: print x,
print

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
	Q4a = Q1+Q2+Q3 + 2 * babylonian_square_root( Q1*Q2+Q2*Q3+Q3*Q1 )
	Q4b = Q1+Q2+Q3 - 2 * babylonian_square_root( Q1*Q2+Q2*Q3+Q3*Q1 )
	print 'Ford circle x coords:', a,b,c
	print ' 3 Kissing circle curvatures:',Q1,Q2,Q3,'->Quadrances of 3 Rhombi'
	print ' Fourth Circle Curvatures a,b:',Q4a,Q4b,' Ratio Q4a to Q1+Q2+Q3:',Fraction(Q4a,Q1+Q2+Q3)
	# ratio should always be two
	# Q4b should always be 0 (the Ford Circles touch this line,
	#  the line being a circule of curvature 0, and thus infinite radius)
