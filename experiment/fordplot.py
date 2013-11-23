from piliko import *

def fordcircle( xcoord ):
	radius = Fraction(1,2*sqr(xcoord.denominator))
	xcenter,ycenter = xcoord,radius
	return circle(point(xcenter,ycenter),radius)

def nextcircle( circ1, circ2 ):
	a = circ1.center.x.numerator
	b = circ1.center.x.denominator
	c = circ2.center.x.numerator
	d = circ2.center.x.denominator
	new_x = Fraction( a+c, b+d )
	return fordcircle( new_x )

c1=fordcircle( Fraction(0,1) )
c2=fordcircle( Fraction(1,1) )
depth=5
circs=[c1,c2]
for i in range(0,depth):
	newcircs = []
	for i in range(len(circs)-1):
		c1,c2 = circs[i],circs[i+1]
		c3 = nextcircle( c1, c2 )
		newcircs += [c1,c3]
	newcircs += [circs[-1]]
	circs = newcircs
for c in circs:
	print c
plot_circles( circs )
