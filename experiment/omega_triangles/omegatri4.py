from piliko import *

# small experiment with Wildberger's Omega Triangles
# take the omega of the omega of the omega of the omega... weird stuff

# this sequence of omega's generates a.. well.. a circular shape.

print
p1,p2,p3=point(5,3),point(4,1),point(3,4)
t = triangle(p1,p2,p3)
print t
tris = [t]
for i in range(0,11):
        ot = omega_triangle( t )
        tris += [ot]
        t = ot
print 'points:',p1,p2,p3
print 'omega triangles:',len(tris)
plot_triangles(tris)

