from piliko import *

# small experiment with Wildberger's Omega Triangles
# take the omega of the omega of the omega of the omega... weird stuff

# contiuning from omgeatri6.py, this shows that if you chain 
# omega_triangle() and circum_triangle(), you get these weird patterns where
# sometimes omega(circum(x)) is the same as circum(omega(x)), and sometimes
# its not. 

from random import randint

print
p1=point(randint(1,10),randint(1,10))
p2=point(randint(1,10),randint(1,10))
p3=point(randint(1,10),randint(1,10))
t = triangle(p1,p2,p3)
print t
ot=omega_triangle( t )
ct=circum_triangle( t )
cot=circum_triangle( ot )
oct=omega_triangle( ct )
ocot=omega_triangle( cot )
coct=circum_triangle( oct )
cocot=circum_triangle( ocot )
ococt=omega_triangle( coct )
tris = [t,ot,ct,cot,oct,ocot,coct,cocot,ococt]
for t in tris:
	print t.p0,t.p1,t.p2
print 'points:',p1,p2,p3
print 'triangles:',len(tris)
plot_triangles(tris)

