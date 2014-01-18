from piliko import *

# this is the idea of 'ford spheres'.... mutually tangent spheres that
# also all touch a plane. we can also think of the plane as sphere of
# 'curvature 0'

# following the ideas of ford circles and descartes kissing circles in 2d,
# we can see that if we are given 3 kissing circles, we can find two 'fourth'.
# kissing circles. in the Ford Circles case, one of the 'fourths' is always
# a line. . . the other a tiny little circle in betwixt the other three.

# and in the world of kissing circles, we favor the idea of ''curvature''
# (1/r) instead of radius. 

# strangely enough the 'circle fourth circle in a Ford sequence is twice 
# the sum of the curvatures of the other 3 circles.

# the line, however, is a circle of curvature 0. in fact its a bit odd
# the effect the ford circles have on Descarte's equation

# Here is Descarte's formula. K = curvature = 1/radius.
#
# (k1+k2+k3+k4)^2=2*(k1^2+k2^2+k3^2+k4^2)
#
# If we have k1,k2, and k3, as we do for 3 kissing Ford circles,
# then K4 is this:
#
# k4 = k1+k2+k3+/- 2 * sqrt( k1k2 + k2k3 + k3k1 )
#
# but of course, if k4 is '0' descartes equation becoems this:
#
# (k1+k2+k3)^2=2*(k1^2+k2^2+k3^2)
#
# strangely enough, this is related to Heron's formula, or 
# Wildberger's Triple Quad Formula. Imagine three squares
# with areas 1, 1, 4. The sides are then 1,1,2. When lined up,
# the two 'span' the length of the third, exactly. . . indicating
# also that the corner-points of these squares are collinear. 
#
# Funnily enough the triple quad formula works for Any Rhombus, not
# just squares. But I digress.
#
#
# lets look at some patterns.
#
# Given one circle, you can create many, many circles
# that will touch it at exactly one point. ("Kiss" it) Not two points,
# not zero points, not three points. One point.
#
# Given two mutually tangent circles, you can create many, many circles
# that will kiss both of them. Not its "OK" if the circles are inside 
# each other.
#
# Given three mutually tangent circles, you can only create two circles
# that will touch all three!!
# 
# Given one sphere, you can find many to kiss it.
# Given two kissing spheres, you can find many to kiss them.
# Given three kissing spheres, you can find many to kiss them.
# Givven four kissing spheres, you can only find two to kiss them!!!!!
#
#
#
# Descartes Circles:
#
# (k1+k2+k3+k4)^2=2*(k1^2+k2^2+k3^2+k4^2)
#
# Descartes Ford Circles, k4=0 (3 kissing circles kissing a line )
#
# (k1+k2+k3)^2=2*(k1^2+k2^2+k3^2)
#
# Descartes Spheres:
#
# (k1+k2+k3+k4+k5)^2=3*(k1^2+k2^2+k3^2+k4^2+k5^2)
#
# Descartes Ford Spheres: k5=0 ( 4 kissing spheres kissing a plane)
#
# (k1+k2+k3+k4)^2=3*(k1^2+k2^2+k3^2+k4^2)

from piliko import *

def descartes_kissing_curvatures_3d(k1,k2,k3):
	term1 = 2*( k1*k2+k1*k3+k2*k3 ) - ( sqr(k1)+sqr(k2)+sqr(k3) )
	term2 = babylonian_square_root( term1 )
	root3 = babylonian_square_root( 3 )
	#print term1
	#print term2
	#print root3
	k4a = Fraction(1,2) * (  root3 * term2 + k1 + k2 + k3 )
	k4b = Fraction(1,2) * ( -root3 * term2 + k1 + k2 + k3 )
	return k4a,k4b

s1=sphere([0,0,1],Fraction(1,4))
s2=sphere([1,0,1],Fraction(1,4))
s3=sphere([Fraction(1,2),0,Fraction(1,8*8)],Fraction(1,8*8))
#k4a,k4b=descartes_kissing_curvatures_3d( 2, 2, 8 )
k4a,k4b=descartes_kissing_curvatures_3d( 2, 6, 8 )
print k4a,k4b
print float(k4a),float(k4b)
