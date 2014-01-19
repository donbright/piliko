# very, very 'rought draft' implementation of some Rational Geometry 
# codes. the type system has not been thought out carefully at all.
# See README.md

# Rational Geometry tries to stick to Rational numbers, here
# we use python's "Fraction" type to represent rationals.

# Rational Geometry was discovered and developed by Norman J Wildberger. 
# This code is not affiliated with him nor endorsed by him in any way. 
# See the README.md file for info.

# todo

# simplify code
# use actual test suite
# deal with /0 and other problems
# implement non-implemented stuff
# make function pointers shorter code, better code 
# put 'of' in func names

# what is omega inverse?


# code design philosophy
# work backwards from usage to code. what would i want to type?
# do i have to rememeber tech details or can i type whatever? 
# (example: triangle from lines, from points, from linesegs)
# (example: spread( x, y ) ---> allow x to be lines, vectors, etc.  
# the code can determine which is appropriate by itself. 

from fractions import Fraction

def rat( x, y ):
	return Fraction( x, y )

def abso( x ):
	if x<0: return -x
	else: return x

def sqr( x ):
	return x*x

def sum( *args ):
	tot = Fraction(0)
	for arg in args:
		tot += arg
	return tot

def avg( *args ):
	return Fraction(sum(*args),len(args))

def sign( x ):
	if x<0: return -1
	return 1

def checktype( typename, arg ):
	return isinstance( arg, typename )

def checktypes( typename, *args ): # are all args of a given type? 
	for i in range(len(args)):
		#if not checktype( typename, args[i] ): return False
		if not isinstance( args[i], typename ): return False		
	return True

# return true if all arguments are either int or Fraction
def checkrationals( *args ):
	for i in range(len(args)):
		if checktypes( Fraction, args[i]):
			pass
		elif checktypes( int, args[i] ):
			pass
		elif checktypes( long, args[i]):
			pass
		elif checktypes( tuple, args[i] ):
			for a in args[i]:
				if not checkrationals( a ): return False
		elif checktypes( str, args[i] ):
			for a in args[i]:
				if not checkrationals( Fraction(a) ): return False
		else:
			return False
	return True

def crash_if_nonrationals( *args ):
	if not checkrationals( *args ):
		raise Exception("Rationals only please")

def bitcount(*args):
	tot=0
	if checkrationals( *args ):
		for a in args:
			tot+=Fraction(a).numerator.bit_length()
			tot+=Fraction(a).denominator.bit_length()
		return tot
	else: raise Exception("Rationals only please")
bit_count=bitcount

class point:
	def __init__(self, *args):
		if checktypes(point,*args):
			self.x=args[0].x
			self.y=args[0].y
			if (hasattr(args[0],'z')): self.z=args[0].z
		elif checktypes(vector,*args):
			self.x=args[0][0]
			self.y=args[0][1]
			if (hasattr(args[0],'z')): self.z=args[0][2]
		elif checkrationals( *args ):
			self.x,self.y=args[0],args[1]
			if (len(args)==3): self.z=args[2]
		elif checktypes( list,*args ) and len(args[0])==2:
			self.x,self.y=args[0][0],args[0][1]
		elif checktypes( list,*args ) and len(args[0])==3:
			self.x,self.y,self.z=args[0][0],args[0][1],args[0][2]
		else: raise Exception( 'cant build point from'+str(args))
	def __str__( self ):
		return point_txt(self)
	def __repr__( self ):
		return point_txt(self)
	def __getitem__( self, i ):
		if i==0: return self.x
		if i==1: return self.y
		if i==2: return self.z
	def __add__( self, p):
		v=vector(self)+vector(p)
		return point(v)
	def __sub__( self, p):
		v=vector(self)-vector(p)
		return point(v)
	def __eq__(self, p):
		if p==None: return False
		if hasattr(p,'z') and hasattr(self,'z'):
			return self.x==p.x and self.y==p.y and self.z==p.z
		if hasattr(p,'z') and not hasattr(self,'z'): return False
		if hasattr(self,'z') and not hasattr(p,'z'): return False
		return self.x==p.x and self.y==p.y
class vector:
	def __init__( self, *args ):
		if checktypes( point,*args ) and len(args)==1:
			p = args[0]
		elif checktypes( complex,*args ) and len(args)==1:
			p = point(args[0].x,args[0].y)
		else:
			p = point( *args )
		self.x,self.y=p.x,p.y
		if hasattr(p,'z'): self.z=p.z
	def __str__( self ):
		return vector_txt(self)
	def __add__( self, v):
		newx = self.x + v.x
		newy = self.y + v.y
		if hasattr(v,'z'):
			newz = self.z + v.z
			return vector(newx, newy, newz)
		return vector(newx, newy)
	def __sub__( self, v ):
		negv = vector( -v.x, -v.y )
		if hasattr(v,'z'): negv.z = -v.z
		return self + negv
	def __mul__( self, *args ):
		if checkrationals(*args) and len(args)==1:
			scalar = args[0]
			newv = vector( self.x * scalar, self.y * scalar )
			if hasattr(self,'z'): newv.z = self.z * scalar
			return newv
		elif checktypes(point,*args) and len(args)==1:
			p = args[0]
			nx,ny = self.x * p.x, self.y * p.y
			if hasattr(self,'z'): nz = self.z * p.z
			return point( nx, ny, nz )
		else: raise Exception("unknown multiplication type for vector")
	def __div__( self, *args ):
		if checkrationals(*args) and len(args)==1:
			return self * Fraction(1,args[0])
	def __rmul__( self, scalar ):
		return self * scalar
	def __neg__( self ):
		return self * -1
	def dot( self, v ):
		x1,y1,x2,y2 = self.x,self.y,v.x,v.y
		p = x1*x2+y1*y2
		if hasattr(v,'z') and hasattr(self,'z'):
			z1,z2 = self.z,v.z
			p += z1*z2
		return p
	def cross( self, v ):
		ax,ay,az,bx,by,bz=self.x,self.y,self.z,v.x,v.y,v.z
		nx = wedge( ay, az, by, bz )
		ny = wedge( ax, az, bx, bz )
		nz = wedge( ax, ay, bx, by )
		return vector( nx, -ny, nz )
	def perpendicular( self, v ):
		return perpendicular( self, v )
	def parallel( self, v ):
		return parallel( self, v )
	def __getitem__( self, i ):
		if i==0: return self.x
		if i==1: return self.y
		if i==2: return self.z

# very simple complex numbers. the form is as follows:
#   x + y * i.
#   i is the square root of negative one
#   x and y are rationals. they also represent coordinates.
class complex:
	def __init__( self, *args ):
		if checkrationals(*args) and len(args)==2:
			self.x,self.y = args[0],args[1]
		elif checktypes(complex,*args) and len(args)==1:
			self.x,self.y=args[0].x,args[0].y
		else: raise Exception('complex needs x,y for x+yi')
	def __str__( self ): return complex_txt(self)
	def __repr__( self ): return complex_txt(self)
	def __add__( self, c ): return complex(self.x+c.x,self.y+c.y)
	def __neg__( self ): return complex(-self.x,-self.y)
	def __sub__( self, c ): return complex(self.x-c.x,self.y-c.y)
	def __div__( self, *args ):
		if checkrationals(*args) and len(args)==1:
			return complex( Fraction(self.x,args[0]), Fraction(self.y,args[0]) )
		else: raise Exception("unknown division for complex number")
	def __mul__( self, *args ):
		if checkrationals(*args) and len(args)==1:
			return complex( self.x*args[0], self.y*args[0] )
		elif checktypes(complex,*args) and len(args)==1:
			a,b,c,d = self.x,self.y,args[0].x,args[0].y 
			return complex(a*c-b*d, a*d+b*c) # (a+bi)(c+di)
		else: raise Exception("unknown multiplication for complex number")
	def __rmul__( self, scalar ): return self * scalar
	def sqrt( self ):
		x, y = self.x,self.y
		#  x + yi  => ( xoo + yoo i )( xoo + yoo i )
		# xoo*yoo*2 = y, xoo^2-yoo^2 = x
		# yoo = y / (2*xoo)
		# xoo^2 - ( y/(2*xoo) )^2 = x
		# xoo^4 - y^2/4 = x * xoo^2
		# xoo^2=q
		# q^2 - x * q - y^2/4 = 0
		# quadratic formula, solve q
		# q = [ -(-x) +/- sqrt( x*x - 4*1*-y^2/4 ) ] / 2*1
		# q = [ x +/- sqrt( x^2 + y^2 ) ]
		# xoo = +/- sqrt(q)
		# yoo = y / (2*xoo)
		qa = Fraction( x + babylonian_square_root( x*x + y*y ), 2 )
		qb = Fraction( x - babylonian_square_root( x*x + y*y ), 2 )
		#print 'qa,qb',qa,qb
		xooa = babylonian_square_root( abs(qa) )
		xoob = babylonian_square_root( abs(qb) )
		#print 'xoo',xooa,xoob
		yooa = Fraction( y, 2*xooa )
		yoob = Fraction( y, 2*xoob )
		return complex( xooa, yooa ), complex( xoob, yoob )
		
class bivector:
	def __init__( self, *args ):
		if checktypes( vector, *args ):
			self.v1,self.v2=args[0], args[1]
		else: raise Exception('not implemented')
	def __str__( self ):
		return bivector_txt(self)
	def __add__( self, bv ):
		return 
	def __sub__( self, bv ):
		raise Exception('not implemented')
	def __mul__( self, scalar ):
		return bivector( self.v1 * scalar , self.v2 )
		# could use self.v1, self.v2 * scalar
	def __rmul__( self, scalar ):
		return self.__mul__(scalar)
	def dot( self, v ):
		raise Exception('not implemented')
	def perpendicular( self, bv ):
		raise Exception('not implemented')
	def parallel( self, bv ):
		raise Exception('not implemented')
	def value( self ):
		# note, det v2, v2 = -1 * det v1, v2
		return determinant( self.v1, self.v2 )
	def __getitem__( self, i ):
		if i==0: return self.v1
		if i==1: return self.v2

# determinant, aka wedge, aka signed area of paralellogram formed by 2 vectors
def wedge( *args ):
	if checktypes(point,*args) and len(args)==2:
		x1,y1,x2,y2=args[0].x,args[0].y,args[1].x,args[1].y
	elif checkrationals(*args) and len(args)==4:
		x1,y1,x2,y2=args[0],args[1],args[2],args[3]
	elif checktypes(vector,*args) and len(args)==2:
		x1,y1,x2,y2=args[0].x,args[0].y,args[1].x,args[1].y
	else: raise Exception('dont understand input to wedge()'+str(args))
	return x1*y2-x2*y1

# line formula here is ax + by + c = 0
class line:
	def __init__( self, *args ):
		if checktypes(point,*args) and len(args)==2:
			self.init_from_points( args[0], args[1] )
		elif checktypes(list,*args) and len(args)==2:
			if len(args[0])==2 and len(args[1])==2:
				p1 = point(args[0][0],args[0][1])
				p2 = point(args[1][0],args[1][1])
				self.init_from_points( p1, p2 )
			else: raise Exception('line needs pts or rationals a,b,c')
		elif checktypes(tuple,*args) and len(args)==2:
			if len(args[0])==2 and len(args[1])==2:
				p1 = point(args[0][0],args[0][1])
				p2 = point(args[1][0],args[1][1])
				self.init_from_points( p1, p2 )
			else: raise Exception('line needs pts or rationals a,b,c')
		elif checkrationals(*args) and len(args)==3:
			self.a,self.b,self.c=args[0],args[1],args[2]
		elif checkrationals(*args) and len(args)==4:
			p1=point(args[0],args[1])
			p2=point(args[2],args[3])
			self.init_from_points( p1, p2 )
		else:
			raise Exception('line needs pts or rationals a,b,c')
	def init_from_points( self, p1, p2 ):
		# for any p collinear to p1,p2, area of 
		# paralello-gram formed by vector v1 (p2-p) and 
		# vector v2 (p1-p) = 0. thus v1 wedge v2 == 0. 
		# expand, and a,b,c become obvious.
		# (same theory as building plane from pts)
		pdiff = p2-p1
		self.a,self.b = pdiff.y,-pdiff.x
		self.c = -wedge( p1, p2 )
	def __str__( self ): return line_txt( self )
	def __repr__( self ): return line_txt( self )
	def __getitem__( self, i ):
		if i==0: return self.a
		if i==1: return self.b

		if i==2: return self.c


# plane formula here is ax + by + cz + d = 0
# Theory+Problems of Vector Analysis, Murray R Spiegel, 1959
# Schaum Publishing, New York. 
# For any p coplanar to p1,p2,p3, area of paralellapiped 
# formed by vector (p2-p), vector (p1-p), and 
# vector(p3-p) = 0. thus v1 dot v2 cross v3 = 0. expand 
# and a,b,c become obvious
#
#    | x-x1  y-y1  z-z1|
#det |x2-x1 y2-y1 z2-z1| = 0 --> x[(y2-y1)(z3-z1)-(y3-y1)(z2-z1)] + y[ ... = 0
#    |x3-x1 y3-y1 z3-z1|         a=(y2-y1)(z3-z1)-(y3-y1)(z2-z1) b=... c=...
#
#On Orientation:
#
#An interesting note. Given 3 points, M,N,P, if you feed them in the 
#reverse order, like P,N,M, then the resulting a,b,c,d will be 'flipped' 
#in sign. For example
#
#M,N,P = [0,0,1],[1,0,1],[0,1,1]
#plane(M,N,P) -> <0:0:1:-1>
#plane(P,N,M) -> <0:0:-1:1>
#
class plane:
	def __init__( self, *args ):
		if checktypes(point,*args) and len(args)==3:
			p1,p2,p3 = args[0],args[1],args[2]
			a,b,c,d=self.findequation(p1.x,p1.y,p1.z,p2.x,p2.y,p2.z,p3.x,p3.y,p3.z)
		elif checkrationals(*args) and len(args)==4:
			a,b,c,d=args[0],args[1],args[2],args[3]
		else:
			raise Exception('not implemented. plane needs pts or rationals a,b,c')
		self.a,self.b,self.c,self.d=a,b,c,d
	def findequation(self,x1,y1,z1,x2,y2,z2,x3,y3,z3 ):
		x21,x31 = x2-x1, x3-x1
		y21,y31 = y2-y1, y3-y1
		z21,z31 = z2-z1, z3-z1
		a = y21*z31-z21*y31
		b = z21*x31-x21*z31
		c = x21*y31-y21*x31
		dx = x1*( z21*y31 - y21*z31 )
		dy = y1*( x21*z31 - z21*x31 )
		dz = z1*( y21*x31 - x21*y31 )
		d = sum(dx,dy,dz)
		return a,b,c,d
	def __str__( self ):
		return plane_txt( self )
	def __getitem__( self, i ):
		if i==0: return self.a
		if i==1: return self.b
		if i==2: return self.c
		if i==3: return self.d

class lineseg:
	def __init__( self, *args ):
		if checktypes(point,*args) and len(args)==2:
			self.p0,self.p1=args[0],args[1]
		elif checkrationals(*args) and len(args)==4:
			self.p0 = point(args[0],args[1])
			self.p1 = point(args[2],args[3])
		else: raise Exception('lineseg needs 2 points')
	def __str__( self ):
		return lineseg_txt( self )
	def quadrance( self ):
		return quadrance( self.p0, self.p1 )
	def __getitem__( self, i ):
		if i==0: return self.p0
		if i==1: return self.p1
line_seg=lineseg

class triangle:
	l0,l1,l2=None,None,None
	p0,p1,p2=None,None,None
	ls0,ls1,ls2=None,None,None
	q0,q1,q2=None,None,None
	s0,s1,s2=[None]*3
	def __init__( self, *args ):
		if checktypes( line, *args ) and len(args)==3:
			self.init_from_lines( args[0],args[1],args[2] )
		elif checktypes( point, *args ) and len(args)==3:
			self.init_from_points( args[0],args[1],args[2] )
		elif checktypes( vector, *args ) and len(args)==3:
			self.init_from_points( point(args[0]),point(args[1]),point(args[2]) )
		elif checkrationals( *args ) and len(args)==6:
			p1=point(args[0],args[1])
			p2=point(args[2],args[3])
			p3=point(args[4],args[5])
			self.init_from_points( p1, p2, p3 )
		elif checkrationals( *args ) and len(args)==9:
			p1=point(args[0],args[1],args[2])
			p2=point(args[3],args[4],args[5])
			p3=point(args[6],args[7],args[8])
			self.init_from_points( p1, p2, p3 )
		elif checktypes( triangle, *args ):
			self.init_from_points( args[0][0],args[0][1],args[0][2] )
		elif checktypes( list, *args ):
			if len(args)==3 and len(args[0])==2 and len(args[1])==2 and len(args[2])==2:
				p1 = point(args[0][0],args[0][1])
				p2 = point(args[1][0],args[1][1])
				p3 = point(args[2][0],args[2][1])
				self.init_from_points( p1, p2, p3 )
			elif len(args)==1:
				t=triangle(*args[0])
				self.init_from_points( t[0],t[1],t[2])
		elif checktypes( tuple, *args ):
			if len(args)==3 and len(args[0])==2 and len(args[1])==2 and len(args[2])==2:
				p1 = point(args[0][0],args[0][1])
				p2 = point(args[1][0],args[1][1])
				p3 = point(args[2][0],args[2][1])
			self.init_from_points( p1, p2, p3 )
		else:
			raise Exception('dont know how to build triangle'+str(args))

	def init_from_lines( self, l0, l1, l2 ):
		p0,p1,p2 = meet(l1,l2),meet(l0,l2),meet(l0,l1)
		self.init_from_points( p0, p1, p2 )

	def init_from_points( self, p0, p1, p2 ):
		#l0,l1,l2 = line(p0,p1),line(p1,p2),line(p2,p0)
		#ls0,ls1,ls2 = lineseg(p1,p2),lineseg(p0,p2),lineseg(p0,p1)
		#q0,q1,q2=quadrance(ls0),quadrance(ls1),quadrance(ls2)
		#s0,s1,s2=spread(l1,l2),spread(l0,l2),spread(l0,l1)

		#self.l0,self.l1,self.l2=l0,l1,l2
		self.p0,self.p1,self.p2=p0,p1,p2
		#self.ls0,self.ls1,self.ls2=ls0,ls1,ls2
		#self.q0,self.q1,self.q2=q0,q1,q2
		#self.s0,self.s1,self.s2=s0,s1,s2
		
	def __str__( self ):
		return triangle_txt( self )
	def __getitem__( self, i ):
		if i==0: return self.p0
		if i==1: return self.p1
		if i==2: return self.p2
	def __setitem__( self, i, value ):
		if i==0: self.p0 = value
		if i==1: self.p1 = value
		if i==2: self.p2 = value

# Circles in Rational Geometry
#
# The first thing to think about is that we don't store the radius. 
# Radius is not always rational, even on a circle that has two rational 
# points. Instead store the squared radius, or 'radial quadrance', which 
# is always rational between two rational points. For example, consider a 
# circle centered at 0,0 with the rational point 1,1. It has an 
# irrational radius of sqrt(2).
#
# in general, the hope is to avoid functions that require the use of 
# radius. but in cases where we do need it, like plotting a graphical 
# representation of the circle, we Approximate.
#
# What does this mean for rational points on the circle? Ah. A circle 
# with irrational radius might not have infinitely many rational points 
# on it, like a circle with rational radius does. But of course, the 
# circle with rational radius has Radial Quadrance that is a perfect 
# square, like 9 or 81/25. And there are infinitely many perfect squares 
# So... our rational radius circles are rather plentiful in the plane 
# are they not? But still, unless we confine ourselves to some highly 
# restricted set of points in the plane, we will deal with irrational 
# radius Circles. And so there might not be a nice rational 
# paramterization of a circle with irrational radius? Or am I missing 
# something?
#
# As an aside, it's a fun fact that if you take a rational triangle you 
# get a rational circumcenter, but the circumradius might be irrational 
# --> but you still get three rational points on it! Another aside: Note 
# that for example, given two circles, radius e and pi, both with 
# rational centers, we as a species don't know if they can be tangent or 
# not. This is the state of affairs of modern mathematics. So many 
# questions still to ponder!
#
# OK. So. How do we draw a circle though? We approximate the radius 
# using a rational number and a square root algorithm, like that used in 
# ancient Mesopotamia / Iraq / Babylon. Ideally we could draw a 'fuzzy 
# line' for irrational radius circles but .. it's beyond my graphics 
# system at the moment. Anyways. We find the apporximate rational 
# radius, and then use a rational paramterization of the circle to build 
# a rational approximation of the irrational radius circle.
#
#
# The next thing to think about is that in Chromogeometry, the shape of 
# Red and Green circles is not a circle, it's a hyperbola. Red is 
# x^2-y^2=radius^2=radial_quadrance. 
#
# Note that the quadrance for a circle in this particular computer code 
# doesn't have a color tied to it, kind of like the quadrance of the 
# formulas like triple-quad dont have a color tied to them. Whether a 
# circle is blue, red, or green is a matter of interpretation when it 
# comes time to draw it or use it somewhere within this computer code 
# package. . . the circle itself only has a center point and a radial 
# quadrance, not a 'color'.
#
# So take these three circles. They have a center, 0,0 and a radial 
# quadrance, 1, but there are three chromogeometry interpretations:
#
#  x^2+y^2=1   x^2-y^2=1   2xy=1    blue,   red,   green
#
# They form one circle, one rectangluar hyperbola, and one 'sideways'
# hyperbola... But if you draw them, they appear to be tangent. Where?
# x=1,y=0 satisfies both blue and red formulas. So the blue circle touches
# the red circle (hyperbola) there. And green? x=1,y=1 satisfies both
# blue and green formulas, so the blue circle touches the green circle
# (hyperbola) there.
#
# How about green and red? y=1/2x, x^2-(1/2x)^2=1, x^4-. . uhm yeah. 
# Plug it into Wolfram Alpha (TM) and you will see if/where Red and 
# Green touch.
#
#
# Now... here is the clever bit. Note that Red Quadrance between points 
# can be negative! That means that our red circles can have negative 
# radial quadrance. But then what is the radius? Normally its 
# sqrt(Quadrance). How can you 'approximate' sqrt(-7) with the 
# Babylonian's algorithm? You can't. The root is what we moderns call an 
# Imaginary Number.
#
# But hold on... I can draw a rational point, like 3,4, that has a 
# negative Red Radial Quadrance between itself and 0,0. 3*3-4*4 = 9-16 = 
# -7. What's the big deal? I can just draw the point at 3,4, thats not 
# imaginary.
#
# Ah. But the 'shape' of the red circle then becomes 'flipped' over the 
# line x=y (the 'red null line' / red axis). And so, you can have two 
# red circles, one with radial quadrance 7 and another with -7, and they 
# will not intersect! Instead, one will be the 'flipped' hyperbola of 
# the other over the x=y line. One will have a irrational radius, 
# sqrt(7), the other will have an imaginary irrational radius, sqrt(-7).
# If you draw both, you get a sort of 'x' shape with four 'nubs' coming in
# towards the origin.
#
# Lastly note that in addition to radial quadrance, we store squared 
# curvature... curvature being the inverse of radius (1/radius). 
# 
# Note that this means we can have a circle with 'infinite radius'. We 
# dont actually store infinity, instead we store curvature as 0 and 
# radius as 'None'. And when radius is 0, we have 'infinite curvature' (None)
#
# So if Red and Green circles can have negative radial quadrance, and thus
# imaginary radius... what about blue circles?
# 
# Interesting you should ask. No, they can't, if you consider the form 
# of the blue quadrance equation. x^2+y^2=Q, then Q is never less than 
# 0, unless x and/or y -itself- is imaginary. However... note that the
# radius itself can be negative... and that x and y will still satisfy
# the equation. But what is 'negative radius'???? What is the point of that?
#
# Ok. Let's say you are a Princess of Bohemia and you write letters to 
# Renee Descartes. Lets say he tells you that with three 'kissing 
# circles', you can find there are two possible choices for a fourth 
# 'kisser'. In Algebra,
#
# 2*(k1^2+k2^2+k3^2+k4^2)=(k1+k2+k3+k4)^2 where k = curvature = 1/radius
#
# If you are given k1,k2,k3, then k4 is sqrt(some mess)... but recall that
# sqrt() can have two answers! Negative and Positive! If, by chance, the
# equation reduced to this:
#
# (k4-1)(k4+1/3)=0
#
# then k4 would have to be 1 or -1/3, meaning radius has to be 1 or -3, 
# giving us radial quadrance of 1 or 9. Note that our points, x and y,
# can satisfy the blue quadrance formula even with a negative radius.
#
# But if radius is distance, how could x and y give a 'negative' 
# distance? Maybe we can imagine that instead of distance, we have 
# 'displacement', or a sort of 'vector' x,y, to our rational points on 
# the circle, and it has a 'negative' magnitude? For example the vector 
# (3,4) could be multiplied by -1, to give (-3,-4). The circle formed by 
# these points is basically an 'inversion' of the ordinary circle, 
# inversion through the origin 0,0. It looks exactly the same, it has 
# all the same points eventually, but it is still there, a sort of twin 
# shadow of the ordinary circle, right on top of it.

#
# Lastly, what about 'infinite radius', where curvature is zero?
#
# Recall the actualy full equation for a conic section
#
# ax^2+by^2+cx+dy+exy+f=0
#
# In that case, the curvature is 0 so the circle is a line. 
# Therefore a=0,b=0,e=0, and then c,d,f become coefficients of a line equation:
#
# cx+dy+f = 0
#
#in that case, the circle will contain 'equation coefficients'.
# 
class circle:
	def __init__(self, *args):
		if (len(args)<2): raise Exception('need center x,y and radial quadrance')
		if checkrationals(*args) and len(args)>=3:
			p = point(args[0],args[1])
			self.init_from_point_and_radial_q( p, args[2] )
		elif checktypes(point,args[0]) and checktypes(int,args[1]):
			self.init_from_point_and_radial_q( args[0], args[1] )
		elif checktypes(int,args[0]) and checktypes(point,args[1]):
			self.init_from_point_and_radial_q( args[1], args[0] )
		elif checktypes(point,args[0]) and checktypes(Fraction,args[1]):
			self.init_from_point_and_radial_q( args[0], args[1] )
		elif checktypes(Fraction,args[0]) and checktypes(point,args[1]):
			self.init_from_point_and_radial_q( args[1], args[0] )
		elif checktypes(tuple,args[0]) and checkrationals(args[1]):
			p = point(args[0][0],args[0][1])
			self.init_from_point_and_radial_q( p, args[1] )
		elif checktypes(list,args[0]) and checkrationals(args[1]):
			p = point(args[0][0],args[0][1])
			self.init_from_point_and_radial_q( p, args[1] )
		else: raise Exception('need center x,y and radial quadrance')
	def init_from_point_and_radial_q( self, p, rq ):
		self.center = p
		self.radial_quadrance = rq
		if (rq!=0): self.curvature_quadrance = Fraction(1,rq)
		else: self.curvature_quadrance = None
#	def init_curvature_zero( self,

	def __str__( self ):
		return circle_txt(self)
	def __repr__( self ):
		return circle_txt(self)




class sphere:
	def __init__(self, *args):
		if (len(args)<2): raise Exception('need center x,y,z and radial quadrance')
		if checkrationals(*args) and len(args)>=4:
			p = point(args[0],args[1],args[2])
			self.init_from_point_and_radial_q( p, args[3] )
		elif checktypes(point,args[0]) and checktypes(int,args[1]):
			self.init_from_point_and_radial_q( args[0], args[1] )
		elif checktypes(int,args[0]) and checktypes(point,args[1]):
			self.init_from_point_and_radial_q( args[1], args[0] )
		elif checktypes(point,args[0]) and checktypes(Fraction,args[1]):
			self.init_from_point_and_radial_q( args[0], args[1] )
		elif checktypes(Fraction,args[0]) and checktypes(point,args[1]):
			self.init_from_point_and_radial_q( args[1], args[0] )
		elif checktypes(tuple,args[0]) and checkrationals(args[1]):
			p = point(args[0][0],args[0][1],args[0][2])
			self.init_from_point_and_radial_q( p, args[1] )
		elif checktypes(list,args[0]) and checkrationals(args[1]):
			p = point(args[0][0],args[0][1],args[0][2])
			self.init_from_point_and_radial_q( p, args[1] )
		else: raise Exception('need center x,y,z and radial quadrance')
	def init_from_point_and_radial_q( self, p, rq ):
		self.center = p
		self.radial_quadrance = rq
		if (rq!=0): self.curvature_quadrance = Fraction(1,rq)
		else: self.curvature_quadrance = None
#	def init_curvature_zero( self,

	def __str__( self ):
		return sphere_txt(self)
	def __repr__( self ):
		return sphere_txt(self)


class quaternion:
	def __init__(self,t,v):
		self.t,self.v=t,v




######## formulas, functions, theorems, operations

#### determinant of vectors
## assume rows of matrix = vectors
## note there is no matrix definition here

def determinant( *args ):
	if checktypes(vector,*args):
		pass
	elif checktypes(point,*args):
		v1,v2=vector(args[0]),vector(args[1])
	else:
		raise Exception('this determinant() needs vector input as rows')
	result = None

	if len(args)<=1: raise Exception('not implemented')

	if len(args)==2:
		v1,v2 = args[0],args[1]
		x1,y1,x2,y2 = v1.x,v1.y,v2.x,v2.y
		result = x1*y2 - x2*y1

	if len(args)==3:
		v1,v2,v3 = args[0],args[1],args[2]
		a,b,c = v1.x, v1.y, v1.z
		d,e,f = v2.x, v2.y, v2.z
		g,h,i = v3.x, v3.y, v3.z
		result = a*e*i - a*f*h + b*f*g - b*d*i + c*d*h - c*e*g

	if len(args)>3: raise Exception('not implemented')

	return result
	

################# nullity

def is_null_point( A ):
	v1 = vector(A.x,A.y)
	if v1.dot(v1)==0: return True
	return False

def is_null_vector( v ):
	if v1.dot(v1)==0: return True
	return False

def is_null_line_from_points( p1, p2 ):
	v1 = vector(p1)
	v2 = vector(p2)
	if is_null_vector( v2-v1 ): return True
	return False

def is_null_line( l ):
	a,b,c=l.a,l.b,l.c
	# ax+by+c = 0 ---> y = ( -c -ax ) / b
	# ax+by+c = 0 ---> x = ( -c -by ) / a
	if b!=0: 
		p1x = 0
		p1y = Fraction( -l.c -l.a * p1x , l.b )
		p2x = 1
		p2y = Fraction( -l.c -l.a * p2x , l.b )
	elif a!=0:
		p1y = 0
		p1x = Fraction( -l.c -l.b * p1y , l.a )
		p2y = 1
		p2x = Fraction( -l.c -l.b * p2y , l.a )
	else:
		raise Exception('dont know what to do with line, a&b = 0')
	A1=point(p1x,p1y)
	A2=point(p2x,p2y)
	v1=vector(A1)
	v2=vector(A2)
	if is_null_vector( v2-v1 ): return True
	return False

def is_null_triangle( t ):
	if is_null_line( t.l0 ): return True
	if is_null_line( t.l1 ): return True
	if is_null_line( t.l2 ): return True
	return False

def is_null( *args ):
	if checktype( line, args[0] ): return is_null_line( args[0] )
	if checktype( triangle, args[0] ): return is_null_triangle( args[0] )
	if checktype( point, args[0] ): return is_null_point( args[0] )
	if checktype( vector, args[0] ): return is_null_vector( args[0] )
	if len(args)>1:
		if checktype( point, args[0] ) and checktype(point,args[1]):
			return is_null_line_from_points( args[0], args[1] )

################# altitudes
# note, line is 3 Rationals: [a:b:c] where ax + by + c = 0

def blue_altitude_line_point( l, A ):
	a,b,c = l.a,l.b,l.c
	x0,y0 = A.x,A.y
	return line(b,-a,-b*x0+a*y0)
def red_altitude_line_point( l, A ):
	a,b,c = l.a,l.b,l.c
	x0,y0 = A.x,A.y
	return line(b,a,-b*x0-a*y0)
def green_altitude_line_point( l, A ):
	a,b,c = l.a,l.b,l.c
	x0,y0 = A.x,A.y
	return line(a,-b,-a*x0+b*y0)

def blue_altitude( *args ):
	if len(args<2): raise Exception('need line and point')
	if checktypes(line, args[0]) and checktypes(point, args[1]):
		l,A = args[0],args[1]
	elif checktypes(point, args[0]) and checktypes(line, args[1]):
		l,A = args[1],args[0]
	return blue_altitude( l, A )

def red_altitude( *args ):
	if len(args<2): raise Exception('need line and point')
	if checktypes(line, args[0]) and checktypes(point, args[1]):
		l,A = args[0],args[1]
	elif checktypes(point, args[0]) and checktypes(line, args[1]):
		l,A = args[1],args[0]
	else:
		raise Exception('need line and point')
	return red_altitude( l, A )

def green_altitude( *args ):
	if len(args<2): raise Exception('need line and point')
	if checktypes(line, args[0]) and checktypes(point, args[1]):
		l,A = args[0],args[1]
	elif checktypes(point, args[0]) and checktypes(line, args[1]):
		l,A = args[1],args[0]
	else:
		raise Exception('need line and point')
	return green_altitude( l, A )

def blue_foot( line0, point0 ):
	a,b,c=line0.a,line0.b,line0.c
	x0,y0=point0.x,point0.y
	fx=Fraction(sqr(b)*x0-a*b*y0-a*c,blueq(a,b))
	fy=Fraction(-a*b*x0+sqr(a)*y0-b*c,blueq(a,b))
	return point(fx,fy)

def red_foot( line0, point0 ):
	a,b,c=line0.a,line0.b,line0.c
	x0,y0=point0.x,point0.y
	fx=Fraction(-sqr(b)*x0-a*b*y0-a*c,redq(a,b))
	fy=Fraction(a*b*x0+sqr(a)*y0+b*c,redq(a,b))
	return point(fx,fy)

def green_foot( line0, point0 ):
	a,b,c=line0.a,line0.b,line0.c
	x0,y0=point0.x,point0.y
	fx=Fraction(a*x0-b*y0-c,2*a)
	fy=Fraction(-a*x0+b*y0-c,2*b)
	return point(fx,fy)

###### perpendicular

# Question - can there be multiple perpendiculars for one vector? 
# answer - yes... do we return both though?
def blue_find_perpendicular_vector( v1 ):
	return vector(-v1.y,v1.x)
def red_find_perpendicular_vector( v1 ):
	return vector(v1.y,v1.x)
def green_find_perpendicular_vector( v1 ):
	return vector(-v1.x,v1.y)
find_perpendicular_vector=blue_find_perpendicular_vector

def blue_find_perpendicular_line( l1 ):
	return line(-l1.b,l1.a,l1.c)
def red_find_perpendicular_line( l1 ):
	return line(l1.b,l1.a,l1.c)
def green_find_perpendicular_line( l1 ):
	return line(-l1.a,l1.b,l1.c)
find_perpendicular_line=blue_find_perpendicular_line

def blue_is_perpendicular_for_vectors( v1, v2 ):
	return v1.x*v2.x + v1.y*v2.y == 0
def red_is_perpendicular_for_vectors( v1, v2 ):
	return v1.x*v2.x - v1.y*v2.y == 0
def green_is_perpendicular_for_vectors( v1, v2 ):
	return v1.x*v2.y + v1.y*v2.x == 0

def blue_is_perpendicular_for_linesegs( ls1, ls2 ):
	v1,v2=vector(ls1[1]-ls1[0]),vector(ls2[1]-ls2[0])
	return blue_is_perpendicular_for_vectors(v1,v2)
def red_is_perpendicular_for_linesegs( ls1, ls2 ):
	v1,v2=vector(ls1[1]-ls1[0]),vector(ls2[1]-ls2[0])
	return red_is_perpendicular_for_vectors(v1,v2)
def green_is_perpendicular_for_linesegs( ls1, ls2 ):
	v1,v2=vector(ls1[1]-ls1[0]),vector(ls2[1]-ls2[0])
	return green_is_perpendicular_for_vectors(v1,v2)

def blue_is_perpendicular_for_lines( l1,l2 ):
	return l1.a*l2.a+l1.b*l2.b==0
def red_is_perpendicular_for_lines( l1,l2 ):
	return l1.a*l2.a-l1.b*l2.b==0
def green_is_perpendicular_for_lines( l1,l2 ):
	return l1.a*l2.b+l1.b*l2.a==0

def blue_is_perpendicular( *args ):
	if checktypes(line,*args) and len(args)==2:
		return blue_is_perpendicular_for_lines(args[0],args[1])
	elif checktypes(lineseg,*args) and len(args)==2:
		return blue_is_perpendicular_for_linesegs(args[0],args[1])
	elif checktypes(vector,*args) and len(args)==2:
		return blue_is_perpendicular_for_vectors(args[0],args[1])
	else: raise Exception('unknown args to blue_is_perpendicular',args)
def red_is_perpendicular( *args ):
	if checktypes(line,*args) and len(args)==2:
		return red_is_perpendicular_for_lines(args[0],args[1])
	elif checktypes(lineseg,*args) and len(args)==2:
		return red_is_perpendicular_for_linesegs(args[0],args[1])
	elif checktypes(vector,*args) and len(args)==2:
		return red_is_perpendicular_for_vectors(args[0],args[1])
	else: raise Exception('unknown args to red_is_perpendicular',args)
def green_is_perpendicular( *args ):
	if checktypes(line,*args) and len(args)==2:
		return green_is_perpendicular_for_lines(args[0],args[1])
	elif checktypes(lineseg,*args) and len(args)==2:
		return green_is_perpendicular_for_linesegs(args[0],args[1])
	elif checktypes(vector,*args) and len(args)==2:
		return green_is_perpendicular_for_vectors(args[0],args[1])
	else: raise Exception('unknown args to green_is_perpendicular',args)
def is_blue_perpendicular( *args ): return blue_is_perpendicular( *args )
def is_red_perpendicular( *args ): return red_is_perpendicular( *args )
def is_green_perpendicular( *args ): return green_is_perpendicular( *args )

########## parallel

def red_parallel_vectors( v1, v2 ):
	raise Exception("not implemented ")
def green_parallel_vectors( v1, v2 ):
	raise Exception("not implemented ")
def blue_parallel_vectors( v1, v2 ):
	return v1.x*v2.y - v2.x*v1.y == 0

def red_parallel_linesegs( v1, v2 ):
	raise Exception("not implemented ")
def green_parallel_linesegs( v1, v2 ):
	raise Exception("not implemented ")
def blue_parallel_linesegs( v1, v2 ):
	raise Exception("not implemented ")

def red_parallel_lines( v1, v2 ):
	raise Exception("not implemented ")
def green_parallel_lines( v1, v2 ):
	raise Exception("not implemented ")
def blue_parallel_lines( v1, v2 ):
	raise Exception("not implemented ")


def parallel( *args, **kwargs ):
	if 'color' in kwargs.keys(): color=kwargs['color']
 	else: color='blue'

	if color=='red':
		parallel_vectors = red_parallel_vectors
		parallel_lines = red_parallel_lines
		parallel_linesegs = red_parallel_linesegs
	elif color == 'green':
		parallel_vectors = green_parallel_vectors
		parallel_lines = green_parallel_lines
		parallel_linesegs = green_parallel_linesegs
	elif color == 'blue':
		parallel_vectors = blue_parallel_vectors
		parallel_lines = blue_parallel_lines
		parallel_linesegs = blue_parallel_linesegs

	if isinstance(args[0],point): # and isinstance(args[1],point):
		raise Exception( "not implemented")
	if isinstance(args[0],line) and isinstance(args[1],line):
		return parallel_lines( args[0], args[1] )
	if isinstance(args[0],lineseg) and isinstance(args[1],lineseg):
		return parallel_linesegs( args[0], args[1] )
	if isinstance(args[0],vector) and isinstance(args[1],vector):
		return parallel_vectors( args[0], args[1] )
	return None



############### quadrance

def red_quadrance_points( p1, p2 ):
	if hasattr(p2,'z') and hasattr(p1,'z'):
		raise Exception(" 3d red quadrance not implemented ")
	return sqr( p2.x-p1.x ) - sqr( p2.y-p1.y )

def green_quadrance_points( p1, p2 ):
	if hasattr(p2,'z') and hasattr(p1,'z'):
		raise Exception(" 3d green quadrance not implemented ")
	return 2*( p2.x-p1.x ) * ( p2.y-p1.y )

def blue_quadrance_points( p1, p2 ):
	q = sqr( p2.x-p1.x ) + sqr( p2.y-p1.y )
	if hasattr(p2,'z') and hasattr(p1,'z'): q += sqr( p2.z-p1.z )
	return q

def blue_quadrance_coords(x1,y1,x2,y2):
	return sqr(x1-x2)+sqr(y2-y1)
def red_quadrance_coords(x1,y1,x2,y2):
	return sqr(x1-x2)-sqr(y2-y1)
def green_quadrance_coords(x1,y1,x2,y2):
	return 2*sqr(x1-x2)*sqr(y2-y1)


def red_quadrance_lineseg( ls ):
	return red_quadrance_points( ls.p0, ls.p1 )
def green_quadrance_lineseg( ls ):
	return green_quadrance_points( ls.p0, ls.p1 )
def blue_quadrance_lineseg( ls ):
	return blue_quadrance_points( ls.p0, ls.p1 )

def quadrance_vector( v, color='blue' ):
	p0 = point( 0,0 )
	p1 = point( v.x, v.y )
	if hasattr(v,'z'):
		p0.z = 0
		p1.z = v.z
	if color=='red':
		return red_quadrance_points( p0, p1 )
	elif color=='green':
		return green_quadrance_points( p0, p1 )
	elif color=='blue':
		return blue_quadrance_points( p0, p1 )

def red_quadrance_vector( v ):
	return quadrance_vector( v, color='red' )
def green_quadrance_vector( v ):
	return quadrance_vector( v, color='green' )
def blue_quadrance_vector( v ):
	return quadrance_vector( v, color='blue' )

def red_quadrance( *args ):
	return quadrance( *args, color='red' )
def green_quadrance( *args ):
	return quadrance( *args, color='green' )
def blue_quadrance( *args ):
	return quadrance( *args, color='blue' )

def quadrance( *args, **kwargs ):
	if 'color' in kwargs.keys(): color=kwargs['color']
 	else: color='blue'

	if color=='blue':
		quadrance_points = blue_quadrance_points
		quadrance_lineseg = blue_quadrance_lineseg
		quadrance_vector = blue_quadrance_vector
	elif color == 'green':
		quadrance_points = green_quadrance_points
		quadrance_lineseg = green_quadrance_lineseg
		quadrance_vector = green_quadrance_vector
	elif color == 'red':
		quadrance_points = red_quadrance_points
		quadrance_lineseg = red_quadrance_lineseg
		quadrance_vector = red_quadrance_vector

	if isinstance(args[0],point) and len(args)>1 and isinstance(args[1],point):
		return quadrance_points( args[0],args[1] )
	elif isinstance(args[0],point) and len(args)==1:
		return quadrance_points( point(0,0),args[0] )
	elif isinstance(args[0],lineseg):
		return quadrance_lineseg( args[0] )
	elif isinstance(args[0],vector):
		return quadrance_vector( args[0] )
	return None



def blue_quadrance_quaternion( q ):
	# checktype( quaternion, q )
	t,x,y,z=q.t,q.x,q.y,q.z
	return t*t+x*x+y*y+z*z

def quadrance_quaternion( q ):
	return blue_quadrance_quaternion( q )

############### spreads



# fixme - if a1^2 - bq^2 = 0 then l1 = null line
# both must be non null?
def red_spread_lines( l1, l2 ):
	a1,b1,c1 = l1.a, l1.b, l1.c
	a2,b2,c2 = l2.a, l2.b, l2.c
	numerator = -1 * sqr(a1*b2-a2*b1)
	denominator = (a1*a1-b1*b1)*(a2*a2-b2*b2)
	if denominator==0: return None
	return Fraction( numerator, denominator )

def green_spread_lines( l1, l2 ):
	a1,b1,c1 = l1.a, l1.b, l1.c
	a2,b2,c2 = l2.a, l2.b, l2.c
	numerator = -1 * sqr(a1*b2-a2*b1)
	denominator = 4 * a1 * a2 * b1 * b2
	if denominator==0: return None
	return Fraction( numerator, denominator )
	
def blue_spread_lines( l1, l2 ):
	a1,b1,c1 = l1.a, l1.b, l1.c
	a2,b2,c2 = l2.a, l2.b, l2.c
	numerator = sqr(a1*b2-a2*b1)
	denominator = (a1*a1+b1*b1)*(a2*a2+b2*b2)
	if denominator==0: return None
	return Fraction( numerator, denominator )

def red_spread_vectors( v1, v2 ):
	raise Exception(" not implemented ")

def green_spread_vectors( v1, v2 ):
	raise Exception(" not implemented ")

def blue_spread_vectors( v1, v2 ):
	# assume 2d
	# fixme - if quadrance of either = 0 then its undefined
	numerator = sqr(v2.dot(v1)) 
	denominator = blue_quadrance_vector( v1 ) * blue_quadrance_vector( v2 )
	return 1 - Fraction( numerator, denominator )

def red_spread( *args ):
	return spread( *args, color='red' )

def green_spread( *args ):
	return spread( *args, color='green' )

def blue_spread( *args ):
	return spread( *args, color='blue' )

def spread( *args, **kwargs ):
	if 'color' in kwargs.keys(): color=kwargs['color']
 	else: color='blue'

	if color=='blue':
		spread_lines = blue_spread_lines
		spread_vectors = blue_spread_vectors
	elif color == 'green':
		spread_lines = green_spread_lines
		spread_vectors = green_spread_vectors
	elif color == 'red':
		spread_lines = red_spread_lines
		spread_vectors = red_spread_vectors

	if isinstance(args[0],line) and isinstance(args[1],line):
		return spread_lines( args[0], args[1] )
	if isinstance(args[0],vector) and isinstance(args[1],vector):
		return spread_vectors( args[0], args[1] )



def red_solid_spread( v1, v2, v3 ):
	raise Exception('not implemented')
def green_solid_spread( v1, v2, v3 ):
	raise Exception('not implemented')
def blue_solid_spread( v1, v2, v3 ):
	Q = quadrance
	numerator = sqr( determinant( v1, v2, v3 ) )
	denominator = Q( v1 ) * Q( v2 ) * Q( v3 ) 
	return Fraction( numerator, denominator )

def solid_spread( *args, **kwargs ):
	for i in range(len(args)):
		if not isinstance(args[i],vector):
			raise Exception('solid spread needs vector input')
	if len(args)!=3: raise Exception('solid spread needs 3d vectors')

	if 'color' in kwargs.keys(): color=kwargs['color']
 	else: color='blue'

	if color=='red':
		solid_spread = red_solid_spread
	elif color == 'green':
		solid_spread = green_solid_spread
	elif color == 'blue':
		solid_spread = blue_solid_spread

	return solid_spread( args[0], args[1], args[2] )


def spread_polynomial( n, s ):
	crash_if_nonrationals( n, s )
	if n==0: return 0
	if n==1: return s
	sn_minus_1 = spread_polynomial(n-1,s)
	sn_minus_2 = spread_polynomial(n-2,s)
	sn = 2*(1-2*s)*sn_minus_1 - sn_minus_2 + 2*s
	return sn

#################### meet

# fixme - what if dont meet? what if same line?
# what if a,b,c all 0?
def meet_lines( l1, l2 ):
	if spread( l1, l2 ) == 0: return None
	a1,b1,c1 = l1.a, l1.b, l1.c
	a2,b2,c2 = l2.a, l2.b, l2.c
	x = Fraction( b2*c1-b1*c2, a2*b1-a1*b2 )
	y = Fraction( a2*c1-a1*c2, b2*a1-b1*a2 )
	return point( x, y )

def meet_line_and_point( l, p ):
	if l.a*p.x + l.b*p.y + l.c == 0: return p
	else: return None

def meet_plane_and_point( pl, pt ):
	if pt.x*pl.a + pt.y*pl.b + pt.z*pl.c + pl.d == 0:
		return pt
	else:
		return None
	
def meet( *args ):
	if isinstance(args[0],line) and isinstance(args[1],line):
		return meet_lines( args[0], args[1] )
	elif isinstance(args[0],line) and isinstance(args[1],point):
		return meet_line_and_point( args[0], args[1] )
	elif isinstance(args[0],point) and isinstance(args[1],line):
		return meet_line_and_point( args[1], args[0] )
	elif isinstance(args[0],point) and isinstance(args[1],plane):
		return meet_plane_and_point( args[1], args[0] )
	elif isinstance(args[1],point) and isinstance(args[0],plane):
		return meet_plane_and_point( args[0], args[1] )

	raise Exception(' not implemented' + str(args) )



############################## 1-dimensional projective geometry

# see NJW's paper, arxiv.org/pdf/math/0701338v1.pdf

class projective_form1d:
	def __init__(self, *args):
		crash_if_nonrationals( args )
		self.d,self.e,self.f=args[0],args[1],args[2]
	def __str__( self ):
		return projective_form_txt(self)
	def discriminant( self ):
		return self.d*self.f-sqr(self.e)

blue_projective_form1d = projective_form1d(1,0,1)
red_projective_form1d = projective_form1d(1,0,-1)
green_projective_form = projective_form1d(0,1,0)

def ppoint_nullcheck1d( ppoint, pform ):
	x,y=ppoint.x,ppoint.y
	d,e,f=pform.d,pform.e,pform.f
	return d*sqr(x)+2*e*x*y+f*sqr(y)

def projective_point1d( *args ):
	if args[0]==0 and args[1]==0:
		raise Exception('projective point cannot have x & y as 0 ')
	return point(args[0],args[1])

def ppoint_perpendicular1d( *args, **kwargs ):
	if 'color' in kwargs.keys(): color=kwargs['color']
 	else: color='blue'
	if not checktype( point, args[0] ):
		raise Exception ('ppoint perp needs a projective point')
	x,y=args[0].x,args[0].y
	p = projective_point(x,y)
	if color=='blue': p=projective_point( -y, x )
	elif color == 'red': p=projective_point( y, x )
	elif color == 'green': p=projective_point( x, -y )
	return p

def projective_quadrance_blue1d( *args ):
	return projective_quadrance( *args, color='blue' )
def projective_quadrance_red1d( *args ):
	return projective_quadrance( *args, color='red' )
def projective_quadrance_green1d( *args ):
	return projective_quadrance( *args, color='green' )

def projective_quadrance1d( *args, **kwargs ):
	if 'color' in kwargs.keys(): color=kwargs['color']
 	else: color='blue'

	if color=='blue': form=blue_projective_form
	elif color == 'green': form=green_projective_form
	elif color == 'red': form=red_projective_form

	for arg in args:
		if isinstance( arg, projective_form ):
			form = arg

	return projective_quadrance_wform( args[0], args[1], form )

def projective_quadrance_wform1d( *args ):
	if not checktype(point, args[0]):
		raise Exception('arg 0-projective_quadrance() needs point,point,form')
	if not checktype(point, args[1]):
		raise Exception('arg 1-projective_quadrance() needs point,point,form')
	if not checktype(projective_form, args[2]):
		raise Exception('arg 2-projective_quadrance() needs point,point,form')
	p1=args[0]
	p2=args[1]
	form=args[2]
	v1,v2=vector(p1),vector(p2)
	if form.discriminant()==0:
		raise Exception('form ',str(form),' is degenerate')
	numerator = form.discriminant() * sqr(determinant(v1,v2))
	denominator = ppoint_nullcheck( p1, form ) * ppoint_nullcheck ( p2, form )
	return Fraction( numerator, denominator )

def projective_triple_spread1d( *args ):
	crash_if_nonrationals( *args )
	if not len(args)==3:
		raise Exception( 'proj trip spread requires 3 numbers')
	return sqr(a+b+c) - 2*(a*a+b*b+c*c) - 4*a*b*c


############ quadrea. "a measure of the non-collinearity of points"
### (if input is three points, the result is 16*(triangle area squared), signed
### note that red + green quadrea are equal, and negative of the blue quadrea
def univ_quadrea( q1, q2, q3 ):
	# see also archimedes function
	return sqr(q1+q2+q3)-2*(sqr(q1)+sqr(q2)+sqr(q3))

def blue_quadrea_points( p1, p2, p3 ):
	q1 = blue_quadrance(p3,p1)
	q2 = blue_quadrance(p1,p2)
	q3 = blue_quadrance(p2,p3)
	return univ_quadrea( q1, q2, q3 )
def red_quadrea_points( p1, p2, p3 ):
	q1 = red_quadrance(p3,p1)
	q2 = red_quadrance(p1,p2)
	q3 = red_quadrance(p2,p3)
	return univ_quadrea( q1, q2, q3 )
def green_quadrea_points( p1, p2, p3 ):
	q1 = green_quadrance(p3,p1)
	q2 = green_quadrance(p1,p2)
	q3 = green_quadrance(p2,p3)
	return univ_quadrea( q1, q2, q3 )

def blue_quadrea_tri( tri ):
	q1 = blue_quadrance(tri.p0,tri.p1)
	q2 = blue_quadrance(tri.p1,tri.p2)
	q3 = blue_quadrance(tri.p2,tri.p0)
	return univ_quadrea( q1, q2, q3 )
def red_quadrea_tri( tri ):
	q1 = red_quadrance(tri.p0,tri.p1)
	q2 = red_quadrance(tri.p1,tri.p2)
	q3 = red_quadrance(tri.p2,tri.p0)
	return univ_quadrea( q1, q2, q3 )
def green_quadrea_tri( tri ):
	q1 = green_quadrance(tri.p0,tri.p1)
	q2 = green_quadrance(tri.p1,tri.p2)
	q3 = green_quadrance(tri.p2,tri.p0)
	return univ_quadrea( q1, q2, q3 )


def blue_quadrea( *args ):
	if checktypes( point, *args ) and len(args)==3:
		return blue_quadrea_points( args[0],args[1],args[2] )
	if checktypes( triangle, *args ) and len(args)==1:
		return blue_quadrea_tri( args[0] )
	raise Exception('quadrea only knows 3 pts or one triangle')
def red_quadrea( *args ):
	if checktypes( point, *args ) and len(args)==3:
		return red_quadrea_points( args[0],args[1],args[2] )
	if checktypes( triangle, *args ) and len(args)==1:
		return red_quadrea_tri( args[0] )
	raise Exception('quadrea only knows 3 pts or one triangle')
def green_quadrea( *args ):
	if checktypes( point, *args ) and len(args)==3:
		return green_quadrea_points( args[0],args[1],args[2] )
	if checktypes( triangle, *args ) and len(args)==1:
		return green_quadrea_tri( args[0] )
	raise Exception('quadrea only knows 3 pts or one triangle')

quadrea = blue_quadrea



############################## misc stuff




# def find_tangent_lines( circle0, a, b):
# given a blue circle and the slope of a line, find the two lines that are 
# tangent to the circle that have the given slope. the slope is expressed as
# two rationals, a and b, which are the 'a','b' coefficients of a line with
# this form: ax+by+c=0. we dont know c. this function will find c for us.
# 
# for example. given a circle at 0,0 with radial quadrance 1, and a slope
# of a=1,b=0, find the tangent lines.
#
# slope of a=1,b=0 is basically a straight vertical line going up and down. 
# the result will be two lines touching the circle at 1,0 and -1,0. Their
# equations: 
#   1x+0y+1=0
#   1x+0y-1=0
#
# Note that in order to produce a rational result, input a and b must be 
# the two legs of a rational Pythagorean triple. Also the circle's 
# quadrance must be a perfect rational square. For example: 
# a=3,b=4,circ=(2,3,25) is OK but a=1,b=1,circle(0,0,1) is not OK 
# because the intersection point would be sqrt(2),sqrt(2) which is irrational.
# 
# If non-pythagorean inputs are givenm an Exception is raised.
#
# Approximations can be made in cases like a=1,b=1, as long as they are
# Rational approximations. I don't have an algorithm for finding such
# approximations but its possible to do it, as they are an infinite number
# of rational Pythagorean triples.
def find_blue_tangent_lines( circle0, a, b):
	# algorithm: translate the circle to 0,0. consider a line with 
	# perpendicular slope, -b a, thru 0,0 and find its 2 
	# intersection points with the circle centered at 0,0. translate those 
	# 2 points back to where the circles original center was. find 
	# the eqn of the lines with the original slope passing thru those 
	# new pts.

	# x^2+y^2=r^2=Quadrance << circle eqn
	# ax+by+c=0 << line eqn
	# bx-ay=0 << line eqn thru origin thats perpendicular to given slope
	# y=-bx/-a 
	# x^2+(-bx/-a)^2=Q 
	# x^2*a^2+b^2*x^2=a^2*Q
	# meetx= + or - a*sqrt(Q/(a^2+b^2))
	# by symmetry, x=ay/b, etc etc -> 
	# meety= + or - b*sqrt(Q/(a^2+b^2))
	if sqr(a)+sqr(b)==0: return line(0,0,0),line(0,0,0)
	tmp = Fraction(circle0.radial_quadrance,sqr(a)+sqr(b))
	root = perfect_square_root( tmp )
	meet1 = point(a*root,b*root)
	meet2 = point(-a*root,-b*root)
	meet3 = meet1+circle0.center
	meet4 = meet2+circle0.center
	c3 = -1*(a*meet3.x+b*meet3.y)
	c4 = -1*(a*meet4.x+b*meet4.y)
	l3,l4 = line(a,b,c3),line(a,b,c4)
	return l3,l4
find_tangent_lines=find_blue_tangent_lines


# def find_red_tangent_lines( circle0, a, b): given a red circle (hyperbola) 
# and the slope of a line, find the two lines that are tangent to the 
# circle that have the given slope. the slope is expressed as two 
# rationals, a and b, which are the 'a','b' coefficients of a line with 
# this form: ax+by+c=0. we dont know c. this function will find c for us.
#
# Note that in order to produce a rational result, input a and b must be 
# the hypoteneuse and one leg of a rational Pythagorean triple. Also the circle's 
# quadrance must be a perfect rational square (negative OK). For example: 
# a=5,b=4,circ=(2,3,25) is OK but a=2,b=1,circle(0,0,1) is not OK 
# because the intersection point would be irrational.
#
# you can generate such pythagorean pairs using a paramteriztaion, like
# m,n=random integers, then a=blueq(m,n) and b=redq(m,n) will be OK.
#
# for red circles, a line with slope>1 is only tangent to a red circle 
# with positive quadrance. in other words, for every red circle with
# positive quadrance, the slope of a tangent line will always be >1
# so if you try to find a tangent with a slope<1, you get no result.
#
# a line with slope<1 is only tangent to a red circle with negative 
# quadrance. in other word, for every red circle with negative quadrance,
# the slope of a tangent line will always be <1.
# so if you try to find a tangent with a slope>1, you get no result.
#
# algebraically, this is because you wind up with imaginary coordinates. 
# visually, its because the the hyperbola x^2-y^2=1 will never have a 
# tangent with slope of, say, for example, slope of 1/2, or 1/8, or etc 
# etc. and the hyperbola x^2-y^2=-1 wont have a tangent line with slope
# of, say, 2, or 4, or 5.
#
def find_red_tangent_lines( circle0, a, b):
	# algorithm: similar to blue circles, 
	# but using the red circle equation,
	# annnd the red idea of perpendicular.
	# annnnnnd we deal with negative Quadrance, which is OK for red circs.
	# ( for neg quadrance info, see description of 'circles' 
	#   elsewhere in this code )
	# 
	# x^2-y^2=r^2=Quadrance << red circle eqn
	# ax+by+c=0 << line eqn
	# bx+ay=0 << line eqn thru 0,0 thats red perpendicular to given slope
	# y=-bx/a 
	# x^2-(-bx/a)^2=Q 
	# x^2*a^2-b^2*x^2=a^2*Q
	# meetx= + or - a*sqrt(Q/(a^2-b^2))
	# by symmetry, x=-ay/b, etc etc -> 
	# meety= + or - b*sqrt(Q/(a^2-b^2))
	Q=circle0.radial_quadrance
	#x=y and x=-y lines are considered never tangent
	# (null lines of the red geometry)
	if sqr(a)-sqr(b)==0: return line(0,0,0),line(0,0,0)
	tmp = Fraction(circle0.radial_quadrance,sqr(a)-sqr(b))
	# this is where we detect lines with slope<1 and positive quadrance,
	# or lines with slope>1 and negative quadrance, both have null solutions
	if tmp<0: return line(0,0,0),line(0,0,0)
	root = perfect_square_root( tmp )
	meet1 = point(-a*root,b*root)
	meet2 = point(a*root,-b*root)
	meet3 = meet1+circle0.center
	meet4 = meet2+circle0.center
	c3 = -1*(a*meet3.x+b*meet3.y)
	c4 = -1*(a*meet4.x+b*meet4.y)
	l3,l4 = line(a,b,c3),line(a,b,c4)
	return l3,l4



# def find_green_tangent_lines( circle0, a, b): given a green circle (hyperbola) 
# and the slope of a line, find the two lines that are tangent to the 
# circle that have the given slope. the slope is expressed as two 
# rationals, a and b, which are the 'a','b' coefficients of a line with 
# this form: ax+by+c=0. we dont know c. this function will find c for us.
#
# Note that in order to produce a rational result, input a and b must be 
# of a form such that a/2*b is a perfect square. In other words, a and b
# must be the two 'differences' between a Pythagorean triple hypoteneuse and
# each of its legs. 
#
# Also the circle's quadrance must be a perfect rational square 
# (negative OK). For example: a=1,b=2,circ=(0,0,25) is OK but 
# a=4,b=3,circle(0,0,1) is not OK because the intersection point would 
# be irrational.
#
# You can generate such Pythagorean pairs using a paramteriztaion. For example
# given m,n=random integers, then 
#   a=blueq(m,n)-greenq(m,n)
#   b=blueq(m,n)-redq(m,n)
#
# for green circles, a line with positive slope (a*b<0) is only going to have
# a tangent to a green circle with negative quadrance. the same is true for
# negative slope-lines and positive quadrances. algebraically its because
# you wind up with imaginary intersection points. visually, it's because
# the hyperbola xy=1 will never have a tangent with slope of, say, for example,
# slope of 1. nor with 1/2, not with 1/8, etc.
#
def find_green_tangent_lines( circle0, a, b):
	# algorithm: similar to red circles, 
	#
	# 2xy=r^2=Quadrance << green circle eqn
	# ax+by+c=0 << line eqn
	# -ax+by=0 << line eqn thru 0,0 thats green perpendicular to given slope
	# y=ax/b 
	# 2*x*(ax/b)=Q 
	# 2*x*x*(a/b)=Q
	# x*x*(a/b)=Q/2
	# x*x=bQ/2a
	# meetx= + or - sqrt(bQ/2a)
	# by symmetry, x=-by/-a, etc etc -> 
	# meety= + or - sqrt(aQ/2b)
	Q=circle0.radial_quadrance
	#horiz and vert lines are considered never tangent
	# (null lines of the green geometry)
	if a*b==0: return line(0,0,0),line(0,0,0)
	tmp1 = Fraction(Q*b,2*a)
	tmp2 = Fraction(Q*a,2*b)
	# this is where we detect if the circle's quadrance and the 
	# line's slope both are both positive or both negative... either 
	# situation has a null result. note that a,b both >0 = negative slope
	if tmp1<0 or tmp2<0: return line(0,0,0),line(0,0,0)
	root1 = perfect_square_root( tmp1 )
	root2 = perfect_square_root( tmp2 )
	meet1 = point(root1,sign(a*b)*root2)
	meet2 = point(-root1,sign(a*b)*-root2)
	meet3 = meet1+circle0.center
	meet4 = meet2+circle0.center
	c3 = -1*(a*meet3.x+b*meet3.y)
	c4 = -1*(a*meet4.x+b*meet4.y)
	l3,l4 = line(a,b,c3),line(a,b,c4)
	return l3,l4


def archimedes_function_3numbers(a,b,c): 
	return sqr(a+b+c) - 2*(a*a+b*b+c*c)

def Archimedes_function( *args ):
	if checkrationals(*args) and len(args)==3:
		a,b,c=args[0],args[1],args[2]
		return archimedes_function_3numbers( a, b, c )
	else: raise Exception("Archimede's function requires 3 numbers")
archimedes_function=Archimedes_function

def Herons_function( tri ):
	q1=blueq(tri[0],tri[1])
	q2=blueq(tri[1],tri[2])
	q3=blueq(tri[2],tri[0])
	return Archimedes_function(q1,q2,q3)
herons_function=Herons_function

def quadruple_quad( *args ):
	print 'warning,,, i think this might be implenented wrong..'
	if checkrationals(*args):
		return quadruple_quad_rationals(args[0],args[1],args[2],args[3])
	elif checktypes(list,*args) and len(args)==1:
		l = args[0]
		if len(l)==4:
			return quadruple_quad_rationals(l[0],l[1],l[2],l[3])
		else:
			raise Exception('need 4 rationals or a list of 4 rationals')
	else: 
		raise Exception('need 4 rationals or a list of 4 rationals')

def quadruple_quad_rationals( a, b, c, d):
	term0 = sqr( a + b + c + d )
	term1 = -2 * ( a*a + b*b + c*c + d*d )
	term2 = sqr( term0 + term1 ) - 64*a*b*c*d
	return term2

def reverse_orientation_triangle( t ):
	return triangle( t[0], t[2], t[1] )

def reverse_orientation( *args ):
	if checktypes(triangle,*args) and len(args)==1:
		return reverse_orientation_triangle( args[0] )
	elif checktypes(list,*args):
		tris = []
		for arg in args[0]:
			if not checktypes(triangle,arg):
				raise Exception('rever. orient. unimplemented')
			tris += [reverse_orientation_triangle( arg )]
		return tris
	else:
		raise Exception('reverse orientation not implemented')
	
def mirrorx_triangle(t):
	p1 = t[0] * vector(-1,1,1)
	p2 = t[1] * vector(-1,1,1)
	p3 = t[2] * vector(-1,1,1)
	return triangle( p1, p2, p3 )

def mirrory_triangle(t):
	p1 = t[0] * vector(1,-1,1)
	p2 = t[1] * vector(1,-1,1)
	p3 = t[2] * vector(1,-1,1)
	return triangle( p1, p2, p3 )

def mirrorz_triangle(t):
	p1 = t[0] * vector(1,1,-1)
	p2 = t[1] * vector(1,1,-1)
	p3 = t[2] * vector(1,1,-1)
	return triangle( p1, p2, p3 )

def mirrorx_point(p):
	if hasattr(p,'z'): return point(-p.x,p.y,p.z) 
	else: return point(-p.x,p.y)
def mirrory_point(p):
	if hasattr(p,'z'): return point(p.x,-p.y,p.z) 
	else: return point(p.x,-p.y)
def mirrorz_point(p):
	if hasattr(p,'z'): return point(p.x,p.y,-p.z) 
	else: return point(p.x,p.y)

def mirrorx( *args ):
	if checktypes(triangle,*args) and len(args)==1:
		return mirrorx_triangle( args[0] )
	elif checktypes(point,*args) and len(args)==1:
		return mirrorx_point( args[0] )
	else: raise Exception('mirror not implemented')
def mirrory( *args ):
	if checktypes(triangle,*args) and len(args)==1:
		return mirrory_triangle( args[0] )
	elif checktypes(point,*args) and len(args)==1:
		return mirrory_point( args[0] )
	else: raise Exception('mirror not implemented')
def mirrorz( *args ):
	if checktypes(triangle,*args) and len(args)==1:
		return mirrorz_triangle( args[0] )
	elif checktypes(point,*args) and len(args)==1:
		return mirrorz_point( args[0] )
	else: raise Exception('mirror not implemented')

# translate a triangle by a vector. example, triangle 0,0 1,0 0,1 by vector 2,0
# result is 2,0 3,0 2,1
def translate_triangle_by_vector( t, v ):
	return triangle( t.p0+v, t.p1+v, t.p2+v )
def translate_lineseg_by_vector( ls, v ):
	p1,p2 = ls[0]+v,ls[1]+v
	return lineseg(p1,p2)
def translate( *args ):
	if len(args)<2: raise Exception( 'need 2 objects for translation' )
	if checktypes( vector, args[0] ) and checktypes( triangle, args[1] ):
		return translate_triangle_by_vector( args[1], args[0] )
	elif checktypes( vector, args[0] ) and checktypes( triangle, args[1] ):
		return translate_triangle_by_vector( args[1], args[0] )
	elif checktypes( lineseg, args[0] ) and checktypes( vector, args[1] ):
		return translate_lineseg_by_vector( args[0], args[1] )
	else: raise Exception('unknown type to translate'+str(args))

# midpoint, its the half-way point between two points.
def midpoint_from_points( p1, p2 ):
	newx = Fraction(p2.x+p1.x,2)
	newy = Fraction(p2.y+p1.y,2)
	return point(newx,newy)
def midpoint_segment( lseg ):
	return midpoint_from_points(lseg[0],lseg[1])
def midpoint(*args):
	if checktypes(point,*args): return midpoint_from_points(args[0],args[1])
	if checktypes(lineseg,*args): return midpoint_segment(args[0])
	raise Exception('dont know how to do midpoint of given object')
# bisect a line segment and return the two resulting smaller segments
def even_split(lseg):
	mp=midpoint(lseg)
	newl1 = lineseg(lseg[0],mp)
	newl2 = lineseg(mp,lseg[1])
	return newl1,newl2

# do three lines meet at a single point?
def concurrent( line1, line2, line3 ):
	monomial = 'a1*b2*c3'
	asymp = gen_antisymmetric_polynomial_string( monomial )
	a1,b1,c1 = line1.a,line1.b,line1.c
	a2,b2,c2 = line2.a,line2.b,line2.c
	a3,b3,c3 = line3.a,line3.b,line3.c
	result = eval(asymp)
	if result==0: return True
	return False

# are points collinear?
def collinear( *args ):
	if checktypes(line,*args):
		for i in range(0,len(args)):
			l1 = args[i]
			l2 = args[(i+1)%len(args)]
			test += spread(l1,l2)
			if test != 0: return False
		return True
	if checktypes(point,*args):
		test = 0
		for i in range(0,len(args),2):
			p1 = args[i]
			p2 = args[(i+1)%len(args)]
			p3 = args[(i+2)%len(args)]
			test += eval_asympoly( 'x1*y2', p1, p2, p3 )
			if test != 0: return False
		return True

def cross( l0, l1 ):
	if not checktypes( line, [l0,l1] ): raise Exception('cross() needs lines')
	return 1 - spread( l0, l1 )

def is_harmonic_pencil_lines( l0, l1, l2, l3 ):
	# see WildTrig39
	raise Exception('not implemented')

def is_harmonic_range_points( p0, p1, p2, p3 ):
	# per WildTrig39, Cross-Ratio can never be 1, therefore
	# squared-cross-ratio can only be one when cross-ratio = -1,
	# therefore you can determine whether points are a 'harmonic range'
	# using the squared cross ratio. 
	if p0 == None or p1 == None or p2 == None or p3 == None: return False
	if squared_cross_ratio_points( p0, p1, p2, p3 ) == 1: return True
	return False

def is_harmonic_range( *args ):
	if not checktypes( point, *args ):
		raise Exception ('harmonic range expects 4 points')
	if not len(args)==4:
		raise Exception ('harmonic range expects 4 points')
	return is_harmonic_range_points( args[0],args[1],args[2],args[3] )

def squared_cross_ratio_lines( l0, l1, l2, l3 ):
	# lines must meet at a single point. see WildTrig39
	raise Exception('not implemented')

def squared_cross_ratio_vectors( v0,v1,v2,v3 ):
	# see WildTrig39
	raise Exception('not implemented')
	
def squared_cross_ratio_points( p0,p1,p2,p3 ):
	# fixme - points must be distinct....
	# fixme - if b is midpoint of c,d, a might be 'at infinity', see
	# wildtrig39 5:05
	a,b,c,d=p0,p1,p2,p3
	if not collinear(a,b,c,d): raise Exception("input pts must be collinear")
	numerator = Fraction ( quadrance(a,c), quadrance(a,d) )
	denominator = Fraction ( quadrance(b,c), quadrance(b,d) )
	return Fraction( numerator, denominator )

	# fun fact - you can calculate squared-cross-ratio using only 
	#     one of the coordinates, except for horiz/vertical lines.

def squared_cross_ratio( *args ):
	if checktypes( point, *args ):
		if len(args)==4:
			a,b,c,d=args[0],args[1],args[2],args[3]
			return squared_cross_ratio_points(a,b,c,d)


def is_pythagorean_triple( a, b, c ):
	return a*a+b*b==c*c

def is_pythagorean_triple_permutation( a, b, c ):
	if a*a+c*c == b*b: return True
	if c*c+b*b == a*a: return True
	if a*a+b*b == c*c: return True
	return False

# circumradial quadrance -> basiclly the square of circumradius.
# whats circumradius? the radius of a circle that has all 3 points of the
# triangle lying exactly on the circle
def blue_circumradial_quadrance( tri ):
	p1 = blue_circumcenter( tri )
	p2 = tri.p0
	return blue_quadrance_points( p1, p2 )
def red_circumradial_quadrance( tri ):
	p1 = red_circumcenter( tri )
	p2 = tri.p0
	return red_quadrance_points( p1, p2 )
def green_circumradial_quadrance( tri ):
	p1 = green_circumcenter( tri )
	p2 = tri.p0
	return green_quadrance_points( p1, p2 )

def blue_circumcircle( tri ):
	return circle(blue_circumcenter(tri),blue_circumradial_quadrance(tri))
def red_circumcircle( tri ):
	return circle(red_circumcenter(tri),red_circumradial_quadrance(tri))
def green_circumcircle( tri ):
	return circle(green_circumcenter(tri),green_circumradial_quadrance(tri))
circumcircle=blue_circumcircle

def blue_ninepointcircle( tri ):
	bnc = blue_ninepointcenter(tri)
	return circle( bnc , blue_quadrance( bnc, midpoint(tri[0],tri[1]) ) )
blue_ninepoint_circle=blue_ninepointcircle
def red_ninepointcircle( tri ):
	rnc = red_ninepointcenter(tri)
	return circle( rnc , red_quadrance( rnc, midpoint(tri[0],tri[1]) ) )
red_ninepoint_circle=red_ninepointcircle
def green_ninepointcircle( tri ):
	gnc = green_ninepointcenter(tri)
	return circle( gnc , green_quadrance( gnc, midpoint(tri[0],tri[1]) ) )
green_ninepoint_circle=green_ninepointcircle

circumradial_quadrance=blue_circumradial_quadrance

##################### triangle measurements

def blue_smallest_quadrance( tri ):
	q1=blue_quadrance_points( tri.p0, tri.p1 )
	q2=blue_quadrance_points( tri.p1, tri.p2 )
	q3=blue_quadrance_points( tri.p2, tri.p0 )
	return min(q1,q2,q3)
def red_smallest_quadrance( tri ):
	q1=red_quadrance_points( tri.p0, tri.p1 )
	q2=red_quadrance_points( tri.p1, tri.p2 )
	q3=red_quadrance_points( tri.p2, tri.p0 )
	return min(q1,q2,q3)
def green_smallest_quadrance( tri ):
	q1=green_quadrance_points( tri.p0, tri.p1 )
	q2=green_quadrance_points( tri.p1, tri.p2 )
	q3=green_quadrance_points( tri.p2, tri.p0 )
	return min(q1,q2,q3)

smallest_quadrance=blue_smallest_quadrance

def blue_smallest_spread( tri ):
	s1=blue_spread_lines( tri.l0, tri.l1 )
	s2=blue_spread_lines( tri.l1, tri.l2 )
	s3=blue_spread_lines( tri.l2, tri.l0 )
	return min(s1,s2,s3)
def red_smallest_spread( tri ):
	s1=red_spread_lines( tri.l0, tri.l1 )
	s2=red_spread_lines( tri.l1, tri.l2 )
	s3=red_spread_lines( tri.l2, tri.l0 )
	return min(s1,s2,s3)
def green_smallest_spread( tri ):
	s1=green_spread_lines( tri.l0, tri.l1 )
	s2=green_spread_lines( tri.l1, tri.l2 )
	s3=green_spread_lines( tri.l2, tri.l0 )
	return min(s1,s2,s3)

smallest_spread=blue_smallest_spread

################## omega triangle and friends

def omega_triangle( tri ):
	o0 = red_orthocenter( tri )
	o1 = green_orthocenter( tri )
	o2 = blue_orthocenter( tri )
	return triangle( o0, o1, o2 )


def circum_triangle( tri ):
	c0 = red_circumcenter( tri )
	c1 = green_circumcenter( tri )
	c2 = blue_circumcenter( tri )
	return triangle( c0, c1, c2 )

def ninepoint_triangle( tri ):
	c0 = red_ninepointcenter( tri )
	c1 = green_ninepointcenter( tri )
	c2 = blue_ninepointcenter( tri )
	return triangle( c0, c1, c2 )


# return the nth layer of the Farey sequence
farey_layers=[]
def farey_sequence(n):
	global farey_layers
	farey_layers=[[Fraction(0,1),Fraction(1,1)]]
	depth = n
	for i in range(0,depth):
		layer = farey_layers[i]
		farey_layers+=[[]]
		for j in range(len(layer)-1):
			numer = layer[j].numerator+layer[j+1].numerator
			denom = layer[j].denominator+layer[j+1].denominator
			farey_layers[i+1] += [layer[j],Fraction(numer,denom)]
		farey_layers[i+1]+=[Fraction(1,1)]
	return farey_layers[n]

# return Ford circle for x coordinate 'x'
def ford_circle(x):
	x=Fraction(x)
	radius = Fraction(1,2*sqr(x.denominator))
	return circle( point(x,radius), sqr(radius) )
	
# return the nth layer of ford circles
def ford_circles(n):
	circles = []
	for number in farey_sequence(n):
		circles += [ford_circle( number )]
	return circles









# must come last?
from piliko_sqrt import *
from piliko_bbox import *
from piliko_plot import *
from piliko_thms import *
from piliko_asymp import *
from piliko_tcents import *
from piliko_rand import *

from piliko_scuts import *

