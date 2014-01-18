from piliko import *
from random import randint
depth=10

c=circle(0,0,1)
a,b=1,0
l1,l2=find_tangent_lines( c, a, b )
print c,l1,l2
plot_circle(c)
plot_lines(l1,l2)

c=circle(0,0,1)
a,b=0,1
l1,l2=find_tangent_lines( c, a, b )
print c,l1,l2
plot_circle(c)
plot_lines(l1,l2)

c=circle(randint(1,depth),randint(1,depth),sqr(randint(1,depth)))
m,n=randint(1,depth),randint(1,depth)
a,b=Fraction(redq(m,n),blueq(m,n)),Fraction(greenq(m,n),blueq(m,n))
l1,l2=find_tangent_lines( c, a, b )
print c,l1,l2
plot_circle(c)
plot_lines(l1,l2)

plotshow()

