from piliko import *

# Rational exploration of De Launay triangulation annnnd refinement.

# Source A: Norman Wildberger's "Chromogeometry", Jun 2008 (& his videos)
# Source B: Jonathan Shewchuk's "Delaunay Refinement Algorithms
#           for Triangular Mesh Generation" May 2001
# Source C: The Internet. Cut-The-Knot.org, Math StackOverflow

# Part 0. The Circumcenter
#
# De Launay's original paper was about "The Empty Sphere", La Sphere Vide.
# He was discussing arrangements of empty spheres in space. So what we are
# dealing with here, are circles. Namely, circles that have points in common
# with triangle vertexes. De Launay also noted Voroni in his paper, and 
# Voroni dealt with a diagram, aka, a Dirichlet tessellation, regarding
# the points 'closest to' main points, forming regions. The Voroni and 
# De Launay are 'duals' of each other, if you transpose points from one
# with the other, you get each other!
#
# And so we are not just dealing with triangles. We are dealing with some
# kind of concepts of distances and space and circles and their patterns. 
#
# For De Launay perspective, though, lets talk about Triangles. Every 
# triangle has a circle that touches it's three points. That is the 
# circum circle. The center is at the circum center. Interestingly, the 
# circum center is at the intersection of lines that bisect the sides of 
# the triangle.
#
# For rational Trig, what does this mean?
#
# First, we are dealing with Rational Points in a Cartesian plane... so 
# we are dealing with x,y coordinates and every x and y is a Rational 
# number. The tringles have 3 rational points as vertexes.#
#
# First off, does that mean the 'lengths' of the triangle are rational?
# No, of course not. But the 'quadrances' of the triangle are.
#
# Second, what about the circumcenter? Well, since it is the intersection
# of bisectors of the triangle, we are dealing with lines with rational
# slopes, and thus rational points of intersection. You can see this
# if you work out the math of intersections and rational points and midpoints
# and bisectors.
#
# Ok, so our circle has a rational center. Does it have a rational radius??
# No. Just as the sides of the triangle don't have to be rational, the
# radius doesn't have to be rational. A simple example is the triangle 
# with points at 0,0  1,0  and  0,1.  The circumcenter is at 1/2, 1/2
# but the radius is sqrt(2)/2. 
#
# The circum'quadrance', though, is rational. But it's a bit different
# than when we dealt with sides of the triangle. The sides of the triangle
# all have infinitely many rational points. Even if the length of the side
# is irrational, there are tons of rational points on it that we can play
# with. 
#
# For the circumcircle, the question is different.
# The radius can be irrational. 
# The standard rational paramterization of the circle, redq/blueq, greenq/blueq
# where q = quadrance b/t 0,0, and m,n, is based on the concept of a rational
# radius. namely, 1. So the point 1,0 is on it. 
#
# If a circle at 0,0 has irrational radius, the point 'radius,0' is 
# irrational. This breaks our paramterization. If you translate the center
# to a rational point, the situation is the same.
#
# However, every circum circle of a rational triangle has at least three 
# rational points... namely the vertexes of the triangle!! So there must
# be some number of rational points on these circles. 
#
#
# 
# 
#
#
#

# Part 1. The "Key Idea" of Delaunay Refinement
# 
# Miller,Talmor,Teng,Walkington's "Circumradius-to-shortest-edge-ratio"
# quoted by Shwechuk.
#
# Basically, take a triangle
# Now draw a circle that has it's three poitns exactly on the circle edge
# Now draw the center of the circle. 
# Now measure the distance from the center to the triangle's 3 points. 
# The distance will be the same for all three triangle points.
# That distance is the 'Circum Radius'
#
# Then find the side of the triangle that is shorter than the other two.
# 
# Now divide the length of the Circum Radius by the length of the 
# Smallest Side. That is your 'circumradius to shortest edge ratio'. 
#
# Shewchuk notes that this ratio = 1/(2*sin(smallest_angle)), if you
# can imagine that the triangle has a 'smallest angle' of the three
# angles that form it.
#
#
#
#
#
# Needle scratch. What can we do with Rational Trigonometry here?
# 
# First part, find the Circumcenter! No problem. Wildberger provides
# some formulas for that in his paper. It is rational, that is, given 
# rational coordinates for input, it produces rational coordinates for
# the Circumcenter. The details have been stuck into the 'piliko.py' 
# python code. 
#
# Second, lets replace 'Circum Radius' with something more 
# Wildbergerish, how about circumradial quadrance? The square of the 
# Circumradius? I forget NJW's terminology for circles but this will do 
# for now.
#
# An interesting question: Is the Circumradius guaranteed to be rational,
# if the three points of the triangle are rational? 
#
# It seems obvious that the Circum Quadrance will be rational in any case,
# even if the circum-radius is a square root. Or... for red 
# or green circles..Negative!
#
# Great. Now what about 'shortest edge'? We want to use 'smallest quadrance'.
# That is easy enough. Just find the 3 quadrances betwee the triangle's 3 points
# and you can find the smallest one easily. That is guaranteed to be Rational.
# 
# Cool, so now we have our equivalent:
# The Circumradius-to-shortest-edge ratio becomes
# circumradial quadrance-to-Smallest-Quadrance ratio.
#
#
#
#
# But we are not there yet. Shwechuk noted that this was related to the
# smallest angle by a simple formula. What do we do in Rational Trig?
#
# We dont use angles, we use 'spreads' between lines. A triangle has
# three spreads. Seems logical that it can have a 'smallest spread'. 
# 
# Now, Spread can be calculated directly from the points of the triangle,
# or from the lines of the triangle, or what have you. No problem. 
# It also produces a rational result when you do it. Although spread
# itself is not necessarily rational, if you give it rational inputs,
# you get rational output. ( I think? Please correct if Im wrong )
#
# So to find the smallest spread, calculate the 3 spreads of the triangle
# and find the minimum.
#
#
#
# Great. 
# So.. the big question. Does circumradial quadrance-to-smallest-quadrance have
# a relationship to 'smallest spread'?
#
# actually it does!
#
# If you play with enough examples you will notice something. 

# circumradial quadrance-to-SmallestQuadrance : 1/Smallest_Spread = 1 : 4
#
# CQ / SQ = 1 / 4*SS
#
# Should we have expected this? Sure, why not. Spread, of course,
# is 'sin squared', so through some trig substitutions you can 
# probably mess around and find that 2*sin(theta) is probably some kind of
# sin squared thing, but im too lazy.

#
# Shewchuk notes that if you then put a Bound, B, on the CR-to-SE ratio,
# you also 'bound' the smallest angle to arcsin(1/2B). 
#
# Do we have this for Rational Trig?
#
# so. put a 'bound', B^2, on the CQ-to-SQ ratio, the biggest CQ-to-SQ = B^2
# Then the smallest spread will be 1/4B^2? OK. Seems OK.
#
#

# Then, in Shewchuk's language, the 'Key Insight' of Delaunay Refinement
# is that you can chop out triangles by looking how they compare to B.
# 
# Now, you can define 'Skinny' triangles as those with a CQ-to_SQ Bigger 
# than B^2.
#

from random import randint
coords=[]
for i in range(0,6):
	coords+=[randint(0,10)]
t = triangle(coords[0],coords[1],coords[2],coords[3],coords[4],coords[5])
print t
cq= circum_quadrance(t)
sq= smallest_quadrance(t)
ss= smallest_spread(t)
cqtosq=Fraction(cq,sq)
print 'circumquad:',cq,'smallest quad:',sq
print 'circumquad to smallest quad:',cqtosq
print 'smallest spread:',ss
print ' 1 / 4 * smallest spread:',Fraction(1,4*ss)
