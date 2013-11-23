from piliko import *

# small experiment with Wildberger's Omega Triangles
# take the omega of the omega of the omega of the omega... weird stuff

# this sequence shows a pattern that seems to recur with
# recursive omegas. you get two 'sets' of triangles that 'inscribe'
# each other. in other words, the points of one triangle seem to 
# lie on the edges of the other triangle. 

# the thing is, they dont 'exactly' lie... they just get close.
# annnnnnnnd... its every 'other' omega. . . for example
# omega(omega(omega(t))) seems to touch om(om(om(om(om(t)))))
# while om(om(om(om(t)))) seems to touch om(om(om(om(om(om(t))))))
# (thats, the third omega seems to touch the 5th, and
# the fourth touches the 6th.. etc etc)

print
p1,p2,p3=point(3,4),point(0,3),point(1,1)
t = triangle(p1,p2,p3)
print t
tris = [t]
for i in range(0,10):
        ot = omega_triangle( t )
        tris += [ot]
        t = ot
print 'points:',p1,p2,p3
print 'omega triangles:',len(tris)
plot_triangles(tris)

