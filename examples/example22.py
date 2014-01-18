from piliko import *
from random import randint
depth=10

# red tangent lines. in other words, tangent lines to red circles... aka 
# the rectangular hyperbola formed by x^2-y^2=Quadrance where Quadrance 
# can be >0 or <0
# 
# interesting... a line with slope>1 is only tangent to a red circle 
# with positive quadrance. in other words, for every red circle with
# positive quadrance, the slope of a tangent line will always be >1
# so if you try to find a tangent with a slope<1, you get no result.
#
# a line with slope<1 is only tangent to a red circle with negative 
# quadrance. in other word, for every red circle with negative quadrance,
# the slope of a tangent line will always be <1.
# so if you try to find a tangent with a slope>1, you get no result.
#

c=circle(0,0,1)
a,b=3,5
l1,l2=find_red_tangent_lines( c, a, b )
print l1,l2 # should be null

c=circle(0,0,-1)
a,b=5,3
l1,l2=find_red_tangent_lines( c, a, b )
print l1,l2 # should be null

c=circle(0,0,1)
a,b=5,3
l1,l2=find_red_tangent_lines( c, a, b )
plot_red_circles(c)
plot_lines(l1,l2)
print c,l1,l2

c=circle(0,0,-1)
a,b=3,5
l1,l2=find_red_tangent_lines( c, a, b )
plot_red_circles(c)
plot_lines(l1,l2)
print c,l1,l2

sign=1
m,n=randint(1,depth),randint(1,depth)
if randint(-1,1)<0:
	sign=-1
	a,b=redq(m,n),blueq(m,n)
else:
	a,b=blueq(m,n),redq(m,n)
c=circle(randint(-depth,depth),randint(-depth,depth),sign*sqr(randint(0,depth)))
l1,l2=find_red_tangent_lines( c, a, b )
print c,l1,l2
plot_red_circle(c)
plot_lines(l1,l2)
plot_points(c.center)
plotshow()

