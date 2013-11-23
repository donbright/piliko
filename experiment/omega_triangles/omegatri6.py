from piliko import *

# small experiment with Wildberger's Omega Triangles
# take the omega of the omega of the omega of the omega... weird stuff

# ok so this particular example shows, in some cases, that
# the circumtriangle of the omegatriangle is the same thing as the
# omegatriangle of the circumtriangle

from random import randint

print
p1=point(randint(1,10),randint(1,10))
p2=point(randint(1,10),randint(1,10))
p3=point(randint(1,10),randint(1,10))
t = triangle(p1,p2,p3)
print t
ot=omega_triangle( t )
ct=circum_triangle( t )
oct=omega_triangle( ct )
cot=circum_triangle( ot )
tris = [t,ot,ct,oct,cot]
for t in tris:
	print t.p0,t.p1,t.p2
print 'points:',p1,p2,p3
print 'triangles:',len(tris)
plot_triangles(tris)

