from piliko import *

# what are the circum centers and circum-radial quadrances of pythagorean
# triangles formed from rational points on the unit circle?

# answer: the circumradial quadrance is constant, and it's 1/4.
# circumradius = sqrt( circum radial quadrance )
# therefore the circumradius is also constant, and is 1/2

# interesting note.. 
# for this type of triangle, the red circum center is the same as the blue,
# but the red circumradial quadrance is not constant.. and can be negative!
# the green circumcenter is always the 'foot' of the triangle on the x axis
# and the circumradial quadrance there is always 0. in other words, the
# green circum-circle is always null for these types of triangles.

from random import randint
m=randint(0,10)
n=randint(0,10)
x = Fraction(redq(m,n),blueq(m,n))
y = Fraction(greenq(m,n),blueq(m,n))
p1,p2,p3=point(0,0),point(x,0),point(x,y)
t=triangle(p1,p2,p3)
print 'triangle ',p1,p2,p3,'->'
print 'blue cc,crq',blue_circumcenter(t),
print blue_circumradial_quadrance(t)
print 'red cc,crq',red_circumcenter(t),
print red_circumradial_quadrance(t)
print 'green cc,crq',green_circumcenter(t),
print green_circumradial_quadrance(t)
