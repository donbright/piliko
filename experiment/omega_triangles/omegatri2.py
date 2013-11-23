from piliko import *

# small experiment with Wildberger's Omega Triangles
# take the omega of the omega of the omega of the omega... weird stuff

print
p1,p2,p3=point(13,11),point(5,0),point(5,12)
t = triangle(p1,p2,p3)
tris = [t]
for i in range(0,8):
        ot = omega_triangle( t )
        tris += [ot]
        t = ot
print 'points:',p1,p2,p3
print 'triangles:',len(tris)
plot_triangles(tris)

