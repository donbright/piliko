
from piliko import *


# Draw Descarte's theorem applied to Ford Circles... 
# But draw it with Green Circles (hyperbolas) not Blue Circles!
# If the Green Circle drawing algorithm is good, then they will 
# actually be ... tangent?? Maybe?
#
# Please see the file descartesford.py for more explanation
#


circs = ford_circles(1)
ncircs = []
for c in circs:
	ncircs += [ circle(c.center,-c.radial_quadrance) ]
circs += ncircs
x=Fraction(1,2)
y=Fraction(7,24)
curvature = k4 = 24
radius = Fraction( 1, curvature )
quadrance = sqr( radius )
center = point(x,y)
circs += [circle(center,quadrance)]
circs += [circle(center,-quadrance)]
plot_green_circles( circs )
plotshow()
