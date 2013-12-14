from piliko import *

#
# This is to find the two 'fourth kisser circles' from Descares theorem, 
# given three Kissing Ford circles. The first fourth is obvious, the 
# 'flat line' or 'circle of zero curvature' that Ford circles all touch. 
# The second? Ahh, that's the one we are trying to find here.

# If you don't know what Ford Circles and Descartes Theorem are, you can
# check out Google, it won't take but a few minutes to grasp the basic
# concept. They are types of mutually tangent, 'kissing', circles.
#
#

# Per Descartes Theorem, 3 kissing circles have two possible fourth
# circles. One is 'curvature 0', of infinite radius, and that is 
# simply the flat line that Ford Circles all touch.
#
# The second. The second is interesting. Let's find it's curvature.
#
# Here is Descarte's formula. K = curvature = 1/radius.
#
# (k1+k2+k3+k4)^2=2*(kq^2+k2^2+k3^2+k4^2)
#
# If we have k1,k2, and k3, as we do for 3 kissing Ford circles,
# then K4 is this:
#
# k4 = k1+k2+k3+/- 2 * sqrt( k1k2 + k2k3 + k3k1 )
#
# Wait, you may ask, we know the Ford Circles curvature? Well, in case 
# you haven't the notes in front of you, lets review real quick. First, 
# we are talking about 3 Kissing Ford Circles. Now, lets review their 
# formula:
# 
# Radius = 1/(2*denominator^2)
# Ford Circle             Left   , Center      , Right
# Centers, X coordinates: a/b    , a+c/b+d     , c/d
# Radiuses:               1/2b^2 , 1/2(b+d)^2  , 1/2d^2
# Centers, Y coordinates: 1/2b^2 , 1/2(b+d)^2  , 1/2d^2
# Curvatures:             2b^2   , 2(b+d)^2    , 2d^2
#
# A nice easy example is to start with the basic Ford Circles,
# at 0/1 and 1/1. 
#
# Centers, X coordinates: 0/1       , 0+1/1+1     , 1/1
# Radiuses:               1/(2*1^2) , 1/2(1+1)^2  , 1/(2*1^2)
# Centers, Y coordinates: 1/(2*1^2) , 1/2(1+1)^2  , 1/(2*1^2)
# Curvatures:             2*1^2     , 2(1+1)^2    , 2*1^2
#
# Simplified:
#
# Centers, X coordinates:  0  , 1/2 ,  1
# Radiuses:               1/2 , 1/8 , 1/2
# Centers, Y coordinates: 1/2 , 1/8 , 1/2
# Curvatures:              2     8     2
#
#
# If you plug these into Descarte's formula, you get
#
# k4 = 2+8+2+/- 2*sqrt( 2*8 + 8*2 + 2*2 )
# k4 = 12 +/- 2*sqrt( 16 + 16 + 4 )
# k4 = 12 +/- 2*sqrt( 36 )
# k4 = 12 + 12 or 12 - 12 
# k4 = 0, 24
#
#
#
#

# So there we are. There are two possible 4th tangents, one a circle
# of 0 curvature, which is just the straigt line that all Ford circles
# are tangent to. 
#
# But wait, where are the x,y coordinates of this 'other' kisser circle?
# The one with curvature 24?
# It should be somewhere up there 'floating' in between the original 3.

#
#
# This is where the 'complex Descartes formula' comes in. 
#
# We treat the x,y coordinates of the circle centers in Descarte's formula
# as if they were 'complex numbers', in other words, 
#
#  x + y*sqrt(-1)
#
#  also written as 'i' for sqrt(-1):
#
#  x + y * i
#
# So for example, the complex number " 3 + 4 i " is actually geometrically
# expressing the x,y coordinate of 3,4. In this way, a single number, 
# the complex number, sort of represents a point on a 2-dimensional Cartesian
# grid system. 
#
# The Complex formula for kissing circles is like so:
#
# z = x + y*sqrt(-1)
#
# (k1z1+k2z2+k3z3+k4z4)^2=2*([k1z1]^2+[k2z2]^2+[k3z3]^2+[k4z3]^2)
#
# If we have k1,k2, and k3, as we do for 3 kissing Ford circles,
# then K4 is this:
#
# z4k4 = k1z1+k2z2+k3z3+/- 2 * sqrt( k1z1k2z2 + k2z2k3z3 + k3z3k1z1 )
#
#
# Wait, how do you even calculate that? 
# 
# It's not that bad actually. It's kind of like calculating an expression
# that contains a sqrt(2) or something, but you never actually have to
# 'get rid' of the sqrt because it's simply a y-coordinate.
#
# So, back to our example of Ford circles.
#
# Centers, X coordinates:  0  , 1/2 ,  1
# Radiuses:               1/2 , 1/8 , 1/2
# Centers, Y coordinates: 1/2 , 1/8 , 1/2
# Curvatures:              2     8     2
#
# In complex numbers, those x,y coordinates are like so:
#
# Ordinary center coordinates Rewritten as Complex numbers
#   x,y        -->    x +  y  * i
#   0,1/2      -->    0 + 1/2 * i
# 1/2,1/8      -->  1/2 + 1/8 * i
#   1,1/2      -->    1 + 1/2 * i
#
# So. In the Complex Descartes theorem we have this:
# 
# z4k4 = k1z1+k2z2+k3z3+/- 2 * sqrt( k1z1k2z2 + k2z2k3z3 + k3z3k1z1 )
#
# We actually know, believe it or not, z1, z2, and z3. We just wrote them.
#
#   x,y        -->    x +  y  * i 
#   0,1/2      -->    0 + 1/2 * i   == z1
# 1/2,1/8      -->  1/2 + 1/8 * i   == z2
#   1,1/2      -->    1 + 1/2 * i   == z3
#
# And we know k1, k2, and k3:  2, 8, and 2. Since we are dealing with 
# k1z1, k2z2, k3,z3, lets calculate them!
#
# 2 * ( 0 + 1/2 * i   )  == k1 * z1  = i
# 8 * ( 1/2 + 1/8 * i )  == k2 * z2  = 4 + i
# 2 * ( 1 + 1/2 * i   )  == k3 * z3  = 2 + i
#
# Therefore we can rewrite Descartes Complex theorem like so, since we know
# k1, k2, k3, z1, z2, and z3:
#
# k4z4 = i+ 4+i +2+i +/- 2*sqrt( i*(4+i) + (4+i)(2+i) + i(2+i) )
# 
# After more rewriting:
#
# k4z4 = 6+3i +/- 2*sqrt( 4i-1 + 8+6i-1 + 2i-1 )
# k4z4 = 6+3i +/- 2*sqrt( 4i+6i+2i + 8-1-1-1 )
# k4z4 = 6+3i +/- 2*sqrt( 5 + 12i )
#
# But can we simplify more? Sure! Sqrt( 5+12i ), using a bit of the quadratic
# formula, and some other tricks, is 3+2i. 
#
# k4 * z4 = 6+3i +/- 2* ( 3+2i )
#
# Rewrite some more:
# 
# k4 * z4 = 6+3i +/- (6+4i)
# k4 * z4 = 6+3i + 6+4i or 6+3i-6-4i
# k4 * z4 = 12+7i or 0-1i
#
# Now.. we can recall that we actually calculated k4 using the 
# 'ordinary' Descarte's formula, before, way above. k4 = 0 or 24
#
# (0 or 24) * z4 = 0-1i or 12+7i
#
# If we divide by what was k4, we get some interesting stuff. If k4 = 0,
#
# z4 = 0-1i / 0. 
# 
# Wait, what does 'divide by zero' mean? It can mean a lot of things, 
# but most folks just call it something like 'undefined'. Either way, 
# the geometrical interpretation here can be imagined like so: imagine 
# the 'center' of the circle is off at infinity somewhere, because this 
# circle has Zero Curvarture, and is in fact the flat line that the Ford 
# Circles all touch. At least that sounds kind of reasonable to me?
# 
# And what about the case where k4 was 24? Ahhh here is the clever bit!
#
# z4 = 12+7i  / 24
# z4 = 12/24+7/24 i
# z4 = 1/2 + 7/24 i
#
# So. Lets recall what we were doing in the first place here. We were looking
# for x,y coordinates for the Fourth Kissing circle, and we wanted to do that
# by looking at z4. 
#
# z4 = x + y*i
#
# In other words, if we calculate the complex number for z4, we can then
# find the x,y coordinates of the center of the 4th Kissing Circle. That's
# what we have done. 
#
# z4 = 1/2 + 7/24 * i
# z4 =   x +  y   * i 
#
#  x = 1/2    y = 7/24     
# 
# Awesome!!!
#
# So, given the first three Ford circles, we can now draw the tiny
# 'non-flat' circle that is inbetween them. It's at 1/2, 7/24 and
# it's curvature is 24! Way cool. 


circs = ford_circles(1)
x=Fraction(1,2)
y=Fraction(7,24)
center = point(x,y)
curvature = k4 = 24
radius = Fraction( 1, curvature )
quadrance = sqr( radius )
circs += [circle(center,quadrance)]
plot_circles( circs )
plotshow()
