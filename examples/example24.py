from piliko import *
from random import randint
depth=10

# example
# find a bunch of tangent lines given the slopes of the lines
# (in the form a,b where ax+by+c=0 is the eqn of a line). plot them.

c=circle(0,0,1)
c2=circle(0,0,-1)
m,n=randint(1,depth),randint(1,depth)
a1,b1=redq(m,n),greenq(m,n)
a2,b2=blueq(m,n),redq(m,n)
a3,b3=blueq(m,n)-redq(m,n),blueq(m,n)-greenq(m,n)
l1,l2=find_blue_tangent_lines( c, a1, b1 )
l3,l4=find_red_tangent_lines( c, a2, b2 )
l5,l6=find_green_tangent_lines( c, a3, b3 )
print l1,l2,l3,l4,l5,l6
plot_green_circles(c)
plot_blue_circles(c)
plot_red_circles(c)
plot_points(meet(l1,l5),meet(l1,l6))
plot_lines(l1,l2,l3,l4,l5,l6)
plotshow()

