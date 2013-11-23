from fractions import Fraction as F

# exploring the sides of the triangles formed by the centers of 
# ford circles

def sqr(x): return x*x

def f2s(x):
	return str(x.numerator) + '/' + str(x.denominator)

class fordcirc:
	def __init__(self,numerator,denominator):
		self.xcoord = F(numerator,denominator)
		self.radius = F(1,2*sqr(denominator))
	def __str__(self):
		return '['+f2s(self.xcoord)+':'+f2s(self.radius)+']'

def findpythq( circ1, circ2 ):
	a = circ1.radius - circ2.radius 
	b = circ2.xcoord - circ1.xcoord
	c = circ1.radius + circ2.radius
	qa = sqr(a)
	qb = sqr(b)
	qc = sqr(c)
	return [f2s(qa),f2s(qb),f2s(qc)]

def nextcirc( circ1, circ2 ):
	a = circ1.xcoord.numerator
	b = circ1.xcoord.denominator
	c = circ2.xcoord.numerator
	d = circ2.xcoord.denominator
	return fordcirc( a+c, b+d )

c1=fordcirc(0,1)
c2=fordcirc(1,1)
psides = findpythq( c1, c2 )
print c1, c2, ':-:', psides[0:2],  ':', psides[2]
for i in range(0,5):
	c2 = nextcirc( c1, c2 )
	psides = findpythq( c1, c2 )
	print c1, c2, ':-:', psides[0:2],  ':', psides[2]


