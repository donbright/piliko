from piliko import *

# small experiment with Wildberger's Omega Triangles
# take the omega of the omega of the omega of the omega... weird stuff

print
p1,p2,p3=point(0,0),point(12,2),point(4,6)
t = triangle(p1,p2,p3)
tris = [t]
for i in range(0,8):
        ot = omega_triangle( t )
        tris += [ot]
        t = ot
print 'points:',p1,p2,p3
print 'triangles:',len(tris)
plot_triangles(tris)


print
p1,p2,p3=point(0,0),point(4,1),point(4,3)
t = triangle(p1,p2,p3)
tris = [t]
for i in range(0,8):
        ot = omega_triangle( t )
        tris += [ot]
        t = ot
print 'points:',p1,p2,p3
print 'triangles:',len(tris)
plot_triangles(tris)

