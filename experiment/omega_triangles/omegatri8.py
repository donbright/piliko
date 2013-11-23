from piliko import *

# small experiment with Wildberger's Omega Triangles

# this example takes a parallellogram and the four triangles that
# connstruct it. 

# it draws the omega triangles for each of the four triangles.

# there are some interesting patterns, artistically.... 

from random import randint
print
x1,y1=0,0
x2,y2=randint(0,10),randint(0,10)
x3,y3=randint(0,10),randint(0,10)
p1,p2,p3 = point(x1,y1),point(x2,y2),point(x3,y3)
p4 = p2+p3
mp = midpoint(p1,p4)
t = triangle(p1,p2,mp)
t2 = triangle(p1,p3,mp)
t3 = triangle(p3,p4,mp)
t4 = triangle(p2,p4,mp)
ot = omega_triangle( t )
ot2 = omega_triangle( t2 )
ot3 = omega_triangle( t3 )
ot4 = omega_triangle( t4 )
tris = [t,t2,t3,t4,ot,ot2,ot3,ot4]
print 'points:',p1,p2,p3,p4,mp
print 'triangles:',len(tris)
plot_triangles(tris)

