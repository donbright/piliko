from piliko import *

# small experiment with Wildberger's Omega Triangles
# take the omega of the omega of the omega of the omega... weird stuff

print
p1,p2,p3=point(0,0),point(4,1),point(3,4)
t = triangle(p1,p2,p3)
ot = omega_triangle( t )
oot = omega_triangle( ot )
t2 = triangle(p2,p3,point(5,3))
ot2 = omega_triangle( t2 )
oot2 = omega_triangle( ot2 )
ooot2 = omega_triangle( oot2 )
#tris= [t,ot,t2,ot2,oot,oot2]
tris= [t2,ot2,oot2,ooot2]
print 'points:',p1,p2,p3,p2+p3
print 'triangles:',len(tris)
plot_triangles(tris)

