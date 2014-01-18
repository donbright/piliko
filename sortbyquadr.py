from piliko import *

# sort points by quadrance... blue, then red, then green

# then plot the points, and show which are the 'least' and 'most' from 
# the point 0,0 in the three different geometries, by drawing blue 
# circles, red circles and green circles (the latter two types of 
# circles look like hyperbolas) that contain the points
#
#
#
#
# result
# green is often similar to blue, but not always
# They are not guaranteed to have the same lowest point, nor highest.
#

from random import randint

def bqcmp( a, b ):
	#print 'bl',a,b,blueq(a.x,a.y), blueq( b.x, b.y )
	return cmp(blueq(a.x,a.y),blueq( b.x, b.y ))
def rqcmp( a, b ):
	#print 'rd',a,b,redq(a.x,a.y), redq( b.x, b.y )
	return cmp(redq(a.x,a.y),redq( b.x, b.y ))
def gqcmp( a, b ):
	#print 'gr',a,b,greenq(a.x,a.y), greenq( b.x, b.y )
 	return cmp(greenq(a.x,a.y),greenq( b.x, b.y ))

points=[]
#for i in range(0,80):
for i in range(0,5):
	points += [ point( randint(-100,100) , randint(-100,100) ) ]

points.sort( bqcmp )
bpoints = list(points)
points.sort( rqcmp )
rpoints = list(points)
points.sort( gqcmp )
gpoints = list(points)

bc_min=circle(0,0,blueq(bpoints[0 ]))
bc_max=circle(0,0,blueq(bpoints[-1]))
rc_min=circle(0,0,redq(rpoints[0 ]))
rc_max=circle(0,0,redq(rpoints[-1]))
gc_min=circle(0,0,greenq(gpoints[0 ]))
gc_max=circle(0,0,greenq(gpoints[-1]))
print bc_min,bc_max
print rpoints[0],rc_min,rc_max
print gc_min,gc_max
plot_blue_circles([bc_min,bc_max])
plot_red_circles([rc_min,rc_max])
plot_green_circles([gc_min,gc_max])
plot_points(points)
print points
plotshow()

