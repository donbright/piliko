from piliko import *
from random import randint

# this particular experiment draws a triangle and then the three
# chromogeometry circumcircles, red, blue and green

# each time you run it gives a different triangle. 

t1 = triangle(randint(0,10),randint(0,10),randint(0,10),randint(0,10),randint(0,10),randint(0,10))
t=triangle(t1)
print t
rcc = red_circumcenter( t )
bcc = blue_circumcenter( t )
gcc = green_circumcenter( t )
rcq1 = redq( rcc, t[0] )
rcq2 = redq( rcc, t[1] )
rcq3 = redq( rcc, t[2] )
bcq1 = blueq( bcc, t[0] )
gcq1 = greenq( gcc, t[0] )
gcq2 = greenq( gcc, t[1] )
gcq3 = greenq( gcc, t[2] )
print 'rcenter',rcc
print 'red cqs',rcq1,rcq2,rcq3
print 'gcenter',gcc
print 'g cqs',gcq1,gcq2,gcq3
plot_triangle(t)
plot_red_circle(circle(rcc,rcq1))
plot_blue_circle(circle(bcc,bcq1))
plot_green_circle(circle(gcc,gcq1))

plotshow()
