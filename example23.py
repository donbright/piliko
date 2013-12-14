from piliko import *
from random import randint
depth=10

# green tangent lines. in other words, tangent lines to green circles... aka 
# the hyperbola formed by 2xy=Quadrance where Quadrance 
# can be >0 or <0
# 
# interesting... a line with slope<0 is only tangent to a green circle 
# with positive quadrance. in other words, for every green circle with
# positive quadrance, the slope of a tangent line will always be <0
# so if you try to find a tangent with a slope>0, you get no result.
#
# a line with slope>0 is only tangent to a green circle with negative 
# quadrance. in other word, for every green circle with negative quadrance,
# the slope of a tangent line will always be >0.
# so if you try to find a tangent with a slope<0, you get no result.
#
# note that when a*b >0, slope is negative. and a*b<0, slope is positive.
# in other words, a*b has to have the opposite sign from the circle's Quadrance 
#

c=circle(0,0,1)
a,b=1,2
l1,l2=find_green_tangent_lines( c, a, b )
print l1,l2
plot_green_circles(c)
plot_lines(l1,l2)

c=circle(0,0,-4)
a,b=-1,2
l1,l2=find_green_tangent_lines( c, a, b )
print l1,l2
plot_green_circles(c)
plot_lines(l1,l2)


sign=1
if randint(-1,1)<1: sign=-1
m,n=randint(1,depth),randint(1,depth)

# ensure that we are dealing with rational points by using a parameterization
a,b=sign*(blueq(m,n)-greenq(m,n)),blueq(m,n)-redq(m,n)

c=circle(randint(-depth,depth),randint(-depth,depth),sign*sqr(randint(0,depth)))
l1,l2=find_green_tangent_lines( c, a, b )
print a,b,':',
print c,l1,l2
plot_green_circle(c)
plot_lines(l1,l2)
plot_points(c.center)
plotshow()

