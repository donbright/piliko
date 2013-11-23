from piliko import *

# Rational exploration of De Launay triangulation.

# Source A: Norman Wildberger's "Chromogeometry", Jun 2008 (& his videos)
# Source B: Jonathan Shewchuk's "Delaunay Refinement Algorithms
#           for Triangular Mesh Generation" May 2001


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
# Wildbergerish, how about CircumQuadrance? The square of the 
# Circumradius? I forget NJW's terminology for circles but this will do 
# for now.
#
# An interesting question: Is the Circumradius guaranteed to be rational,
# if the three points of the triangle are rational? 
#
# It seems obvious that the Circum Quadrance will be rational in any case,
# even if the circum-radius is a square root. 
#
#
#
#
# Great. Now what about 'shortest edge'? We want to use 'smallest quadrance'.
# That is easy enough. Just find the 3 quadrances betwee the triangle's 3 points
# and you can find the smallest one easily. That is guaranteed to be Rational.
#
# 
# Cool, so now we have our equivalent:
# The Circumradius-to-shortest-edge ratio becomes
# CircumQuadrance-to-Smallest-Quadrance ratio.
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
# So.. the big question. Does Circumquadrance-to-smallest-quadrance have
# a relationship to 'smallest spread'?
#
# actually it does!
#
# If you play with enough examples you will notice something. 

# CircumQuadrance-to-SmallestQuadrance : 1/Smallest_Spread = 1 : 4
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
# so. put a 'bound', B, on the CQ-to-SQ ratio, the biggest CQ-to-SQ = B
# Then the smallest spread will be 1/4B? OK. Seems OK.
#
#

# Then, in Shewchuk's language, the 'Key Insight' of Delaunay Refinement
# is that you can chop out triangles by looking how they compare to B.
# 
# Now, you can define 'Skinny' triangles as those with a CQ-to_SQ bigger than B.
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
