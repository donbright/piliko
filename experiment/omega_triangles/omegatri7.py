from piliko import *

# small experiment with Wildberger's Omega Triangles

# in this, we take two input triangles that form a paralellogram
# and then output the two omega triangles. (and circum triangles and ninepoint)

from random import randint
print
p1=point(randint(0,10),randint(0,10))
p2=point(randint(0,10),randint(0,10))
p3=point(randint(0,10),randint(0,10))
t = triangle(p1,p2,p3)
t2 = triangle(p1+(p3-p1)+(p2-p1),p2,p3)
ot = omega_triangle( t )
ot2 = omega_triangle( t2 )
ct = circum_triangle( t )
ct2 = circum_triangle( t2 )
nt = ninepoint_triangle( t )
nt2 = ninepoint_triangle( t2 )
tris = [t,t2,ot,ot2,ct,ct2,nt,nt2]
print 'points:',p1,p2,p3,p2+p3
print 'triangles:',len(tris)
plot_triangles(tris)

