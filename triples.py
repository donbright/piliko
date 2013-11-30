
from piliko import *

# there is a correspondence between a triplet of Ford circles and
# a triplet of squares.
#
# How? Well, look at the triple quad formula, then look at Descartes
# kissing circles formula for Ford Circles
#
# Triple quad formula for three 'kissing' squares:
#
#  2* ( q1^2 + q2^2 + q3^2 ) = ( q1 + q2 + q3 ) ^ 2
#
# Descarte's Kissing Cirlces, for Ford Circles (fourth circle has curvature 0)
#
#  2* ( k1^2 + k2^2 + k3^2 ) = ( k1 + k2 + k3 ) ^ 2
#
# k = curvature of circle = 1/radius
#

# In other words, the correspondence is between the Curvature of the circles
# and the Quadrance of the squares

# Can we get any more detailed? Sure. Lets get down to some nitty gritty
# of what Ford circles are made of exactly.

#
# Note that ford circles come in this form:
#
# x coordinate: a/b
# y coordinate: radius
# radius: 1 / ( 2*b^2 )
#
# therefore the curvature of a ford circle is 2*b^2
#
#
# Now, consider three ford circles.
#
# circle 1:
# x coordinate: a/b
# y coordinate: radius
# radius: 1 / ( 2*b^2 )
# curvature: ( 2*b^2 )
#
# circle 2:
# x coordinate: c/d
# y coordinate: radius
# radius: 1 / ( 2*d^2 )
# curvature: ( 2*d^2 )
# 
# circle 3: by definition of Ford circles,
# x coordinate: a+c / b+d
# y coordinate: radius
# radius: 1 / ( 2*(b+d)^2 )
# curvature: ( 2*(b+d)^2 )

#
# There will be three corresponding Squares. 
# 
# Square 1:
# Quadrance: curvature of circle 1
# Square 2:
# Quadrance: curvature of circle 2
# Square 3:
# Quadrance: curvature of circle 3

# or more specifically
# Square 1:
# Quadrance: 2*b^2
# Square 2:
# Quadrance: 2*d^2
# Square 3:
# Quadrance: 2*(b+d)^2

#
#
# Note that the sides of these squares will have interesting relationships
# Square 1:
# Quadrance: 2*b^2
# Side length: sqrt(2) * b
# Square 2:
# Quadrance: 2*d^2
# Side length: sqrt(2) * d
# Square 3:
# Quadrance: 2*(b+d)^2
# Side length: sqrt(2) * (b+d)
#
#
# In other words, side 1 + side 2 = side 3. This is exactly what we might
# expect from the Triple Quad Formula - we might even call
# it Wildeberger's Kissing Squares. Although he calls it Archimedes
# Formula if I remember correctly.
#

#
# But can we go farther? Sure! Recall that Wildberger's Quadrance concept
# is not just of one kind. There is also 'red' quadrance and 'green' 
# quadrance.... they can both be interpreted as the signed area of 
# paralellograms. Therefore, the correspondence between the Ford-circle
# triples and three squares, also is a correspondence between the Ford-circle
# triple and three paralellograms.
# 
#

# OK! Can we go farther? Sure. Actually if you play around long enough 
# You will find that if you follow the "Fibonacci Path" down the ford 
# circles , in other words, the ford circles with x coordinate of 1/1, 
# 1/2, 2/3, 3/5, 5/8, etc etc etc.... you will find that the corresponding
# Kissing Quadrances will form a square-tiling of a rectangle.... specifially
# the famous Fibonacci sequence of squares that make a rectangle. 
#
#
# But can we go farther? Sure!
# If you follow a different path of Ford circles, you will find 'fibonacci-like'
# sequences.... and you will get alternative square tilings of the circle!
# The quickest easiest one is the ... 1 -> 4 -> 7 -> 11 branch. Unfortunately
# the gentleman's name escapes me at the moment. The trick is that you have
# to add extra '1' squares.... how many? As many as you 'skipped' when 
# starting down the Ford Circle path in the first place. 

#
# But can we go farther?
#
# 
#


class tquad:
	def __init__(self,q1,q2,q3):
		self.q1,self.q2,self.q3 = q1,q2,q3
	def __str__(self):
		return '['+str(self.q1)+','+str(self.q2)+','+str(self.q3)+']'

class tcirc:
	def __init__(self,c1,c2,c3):
		self.c1,self.c2,self.c3 = c1, c2, c3
	def __str__(self):
		return '['+str(self.c1)+','+str(self.c2)+','+str(self.c3)+']'

def corresponding( *args ):
	if checktypes(tquad,*args):
		tq = args[0]
		curvature1 = tq.q1
		curvature2 = tq.q2
		curvature3 = tq.q3
		radius1 = Fraction(1, curvature1)
		radius2 = Fraction(1, curvature2)
		radius3 = Fraction(1, curvature3)
		circle1 = circle(0,0,sqr(radius1))
		circle2 = circle(0,0,sqr(radius2))
		circle3 = circle(0,0,sqr(radius3))
		return tcirc(circle1,circle2,circle3)
	elif checktypes(tcirc,*args):
		tc = args[0]
		q1 = tc.c1.curvature
		q2 = tc.c2.curvature
		q3 = tc.c3.curvature
		return tquad(q1,q2,q3)


tq = tquad(1,2,3)
tc = corresponding(tq)
print tq
print tc
