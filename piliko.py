# very, very basic implementation of some Rational Geometry formulas
# in two dimensions.

# Rational Geometry tries to stick to Rational numbers, here
# we use python's "Fraction" type to represent rationals.

# Rational Geometry is from Norman J Wildberger. This code is not affiliated
# with him in any way, but you can learn more at these websites:
#
# https://www.youtube.com/user/njwildberger
# http://web.maths.unsw.edu.au/~norman/
# http://www.wildegg.com
# http://www.cut-the-knot.org/pythagoras/RationalTrig/CutTheKnot.shtml
# http://farside.ph.utexas.edu/euclid.html

from fractions import Fraction

class line:
	# line formula here is ax + by + c = 0
	a,b,c=0,0,0
	def __init__( self, a, b, c ): 
		if (type(a) is float): raise Exception("Rationals only please")
		if (type(b) is float): raise Exception("Rationals only please")
		if (type(c) is float): raise Exception("Rationals only please")
		self.a,self.b,self.c=a,b,c
	def __str__( self ):
		return '<'+str(self.a)+":"+str(self.b)+":"+str(self.c)+'>'
		
class triangle:
	l0,l1,l2=line(0,0,0),line(0,0,0),line(0,0,0)
	def __init__( self, l0, l1, l2 ):
		self.l0,self.l1,self.l2 = l0, l1, l2
	def dump_lineqs( self ):
		return 'line eqs:'+str(self.l0)+','+str(self.l1)+','+str(self.l2)
	def __str__( self ):
		return self.dump_lineqs()

class point:
	x,y=0,0
	def __init__(self, x, y):
		if (type(x) is float): raise Exception("Rationals only please")
		if (type(y) is float): raise Exception("Rationals only please")
		self.x,self.y=x,y
	def dump_coords( self ):
		return '('+str(self.x)+','+str(self.y)+')'
	def __str__( self ):
		return self.dump_coords()

class lineseg:
	p0,p1=point(0,0),point(0,0)
	def __init__(self,p0,p1):
		self.p0,self.p1=p0,p1
	def dump_pts( self ):
		return str(self.p0) +'-'+str(self.p1)
	def dump_eqn( self ):
		return 'not implemented'
	def __str__( self ):
		return self.dump_pts()

def rat( x, y ):
	return Fraction( x, y )

def sqr( x ):
	return x*x

def red_quadrance( p1, p2 ):
	raise Exception(" not implemented ")

def green_quadrance( p1, p2 ):
	raise Exception(" not implemented ")

def blue_quadrance( p1, p2 ):
	return sqr(p2.x - p1.x)+sqr(p2.y-p1.y)

def quadrance( p1, p2 ):
	return blue_quadrance( p1, p2 )

def lsquadrance( lineseg ):
	return quadrance( lineseg.p1, lineseg.p0 )

def red_spread( l1, l2 ):
	raise Exception(" not implemented ")

def green_spread( l1, l2 ):
	raise Exception(" not implemented ")
	
def blue_spread( l1, l2 ):
	a1,b1,c1 = l1.a, l1.b, l1.c
	a2,b2,c2 = l2.a, l2.b, l2.c
	numerator = sqr(a1*b2-a2*b1)
	denominator = (a1*a1+b1*b1)*(a2*a2+b2*b2)
	return Fraction( numerator, denominator )

def spread( l1, l2 ):
	return blue_spread( l1, l2 )

def meet( l1, l2 ):
	a1,b1,c1 = l1.a, l1.b, l1.c
	a2,b2,c2 = l2.a, l2.b, l2.c
	x = Fraction()
	y = Fraction()
	return x,y

def intersection( l1, l2 ):
	return meet( l1, l2 )

def is_green_perpendicular( l1, l2 ):
	raise Exception(" not implemented ")
	
def is_red_perpendicular( l1, l2 ):
	raise Exception(" not implemented ")
	
def is_blue_perpendicular( l1, l2 ):
	return spread( l1, l2 ) == 0

def is_perpendicular( l1, l2):
	return is_blue_perpendicular( l1, l2 )

def is_paralell( l1, l2):
	return spread( l1, l2 ) == 1

def is_parallel( l1, l2):
	return paralell( l1, l2 )



# calculate left hand side and right hand side of various formulas

def triple_quad_lhs( q0, q1, q2 ):
	return sqr(q0+q1+q2)

def triple_quad_rhs( q0, q1, q2 ):
	return 2*( q0*q0 + q1*q1 + q2*q2 )

def quadruple_quad_lhs( q0, q1, q2, q3 ):
	term0 = sqr( q0 + q1 + q2 + q3 )
	term1 = q0*q0 + q1*q1 + q2*q2 + q3*q3
	return sqr( term0 - 2*term1 )

def quadruple_quad_rhs( q0, q1, q2, q3 ):
	return 64 * q0 * q1 * q2 * q3

