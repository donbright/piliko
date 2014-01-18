from piliko import *

p0,p1,p2=point(0,0),point(4,0),point(4,3)
print 'p0,p1,p2',p0,p1,p2

Ab = blue_quadrea( p0, p1, p2 )
Ag = green_quadrea( p0, p1, p2 )
Ar = red_quadrea( p0, p1, p2 )

print 'blue quadrea of p0, p1, p2: ', Ab
print 'red quadrea of p0, p1, p2: ', Ag
print 'green quadrea of p0, p1, p2: ', Ar

p0,p1,p2=point(0,0),point(5,0),point(5,12)
print 'p0,p1,p2',p0,p1,p2
t = triangle( p0, p1, p2 )
print 'triangle t:',t
Ab = blue_quadrea( t )
Ag = green_quadrea( t )
Ar = red_quadrea( t )
print 'blue quadrea of t: ', Ab
print 'red quadrea of t: ', Ag
print 'green quadrea of t: ', Ar

