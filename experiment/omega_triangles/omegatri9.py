from piliko import *

# small experiment with Wildberger's Omega Triangles

# this example has three input triangles,
# the thing is that two of the input triangles are made by 'splitting'
# the third triangle... so they all share two points in common with each
# other... and the point is on the edge..

# the result is some interesting patterns of the orthotriangles...
# sometimes they look somewhat 'inset' from each other, other times they
# kind of 'fan' out, other times they are jumbled. 

from random import randint
print
x1,y1=0,0
x2,y2=randint(0,10),randint(0,10)
x3,y3=randint(0,10),randint(0,10)
p1,p2,p3 = point(x1,y1),point(x2,y2),point(x3,y3)
p4 = p2+p3
mp = midpoint(p1,p4)
t = triangle(p1,p2,p3)
t2 = triangle(p2,p3,p4)
t3 = triangle(p3,p4,p1)
t4 = triangle(p4,p1,p2)
tx = triangle(p1,p2,mp)
tx2 = triangle(p1,p3,mp)
tx3 = triangle(p2,p4,mp)
tx4 = triangle(p3,p4,mp)
ot = omega_triangle( t )
ot2 = omega_triangle( t2 )
ot3 = omega_triangle( t3 )
ot4 = omega_triangle( t4 )
otx = omega_triangle( tx )
otx2 = omega_triangle( tx2 )
otx3 = omega_triangle( tx3 )
otx4 = omega_triangle( tx4 )
#tris = [t,t2,t3,t4,ot,ot2,ot3,ot4]
#tris += [tx,tx2,tx3,tx4,otx,otx2,otx3,otx4]
tris = [t,ot]
tris += [tx,tx2,otx,otx2]
print 'points:',p1,p2,p3,p4,mp
print 'triangles:',len(tris)
plot_triangles(tris)

