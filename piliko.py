# very, very 'rought draft' implementation of some Rational Geometry 
# formulas. the type system has not been thought out carefully at all.

# most of this is for 2-dimensional space, some of it is for 1-dimensional space

# Rational Geometry tries to stick to Rational numbers, here
# we use python's "Fraction" type to represent rationals.

# Rational Geometry is from Norman J Wildberger. This code is not affiliated
# with him nor endorsed by him in any way. See the README for info.

#
# todo

# simplify code
# use actual test suite
# deal with /0 and other problems
# implement non-implemented stuff
# get the subscripts to match NJW's books/lectures (not 0 indexed, 1 indexed)
# split out print functions from basic code? sep presentation w data...
# make function pointers shorter code, better code 
# add args* based triangle constructor (points or lines)
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

def sqr( x ):
	return x*x

def avg( *args ):
	tot = Fraction(0)
	for arg in args:
		tot += arg
	return Fraction(tot,len(args))

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
		if checktypes( Fraction, args[i]) or checktypes( int, args[i] ):
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

class point:
	def __init__(self, *args):
		if checktypes(vector,*args):
			self.x=args[0][0]
			self.y=args[0][1]
			if (len(args)==3): self.z=args[0][2]
		elif checkrationals( *args ):
			self.x,self.y=args[0],args[1]
			if (len(args)==3): self.z=args[2]
		else: raise Exception( 'cant build point')
	def __str__( self ):
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
		if hasattr(p,'z') and hasattr(self,'z'):
			return self.x==p.x and self.y==p.y and self.z==p.z
		if hasattr(p,'z') and not hasattr(self,'z'): return False
		if hasattr(self,'z') and not hasattr(p,'z'): return False
		return self.x==p.x and self.y==p.y
class vector:
	def __init__( self, *args ):
		if checktype( point,args[0] ):
			p=args[0]
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

	def __rmul__( self, scalar ):
		return self * scalar
	def __neg__( self ):
		return self * -1
	def dot( self, v ):
		x1,y1,x2,y2 = self.x,self.y,v.x,v.y
		p = x1*x2+y1*y2
		if hasattr(v,'z'): raise Exception( 'not implemented' )
		if hasattr(self,'z'): raise Exception( 'not implemented' )
		return p
	def perpendicular( self, v ):
		return perpendicular( self, v )
	def parallel( self, v ):
		return parallel( self, v )
	def __getitem__( self, i ):
		if i==0: return self.x
		if i==1: return self.y
		if i==2: return self.z

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

class line:
	# line formula here is ax + by + c = 0
	def __init__( self, *args ):
		if len(args)==2 and isinstance(args[0],point) and isinstance(args[1],point):
			x1,y1,x2,y2=args[0].x,args[0].y,args[1].x,args[1].y
			a,b,c=y1-y2,x2-x1,x1*y2-x2*y1
		elif len(args)==3 and type(args[0])==int and type(args[1])==int and type(args[2])==int:
			a,b,c=args[0],args[1],args[2]
		elif len(args)==3 and instanceof(args[0],Fraction) and instanceof(args[1],Fraction) and instanceof(args[2],Fraction):
			a,b,c=args[0],args[1],args[2]
		else:
			raise Exception('not implemented. line needs pts or rationals a,b,c')
		self.a,self.b,self.c=a,b,c
	def __str__( self ):
		return line_txt( self )
	def __getitem__( self, i ):
		if i==0: return self.a
		if i==1: return self.b
		if i==2: return self.c

class lineseg:
	def __init__( self, *args ):
		if checktypes(point,*args):
			self.p0,self.p1=args[0],args[1]
		if checktypes(Fraction,*args):
			self.p0 = point(args[0],args[1])
			self.p1 = point(args[2],args[3])
		if checktypes(int,*args):
			self.p0 = point(args[0],args[1])
			self.p1 = point(args[2],args[3])
	def __str__( self ):
		return lineseg_txt( self )
	def quadrance( self ):
		return quadrance( self.p0, self.p1 )
	def __getitem__( self, i ):
		if i==0: return self.p0
		if i==1: return self.p1

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
		elif checktypes( tuple, *args ):
			if len(args)==3 and len(args[0])==2 and len(args[1])==2 and len(args[2])==2:
				p1 = point(args[0][0],args[0][1])
				p2 = point(args[1][0],args[1][1])
				p3 = point(args[2][0],args[2][1])
			self.init_from_points( p1, p2, p3 )
		else: raise Exception('dont know how to build triangle')

	def init_from_lines( self, l0, l1, l2 ):
		p0,p1,p2 = meet(l1,l2),meet(l0,l2),meet(l0,l1)
		self.init_from_points( p0, p1, p2 )

	def init_from_points( self, p0, p1, p2 ):
		l0,l1,l2 = line(p0,p1),line(p1,p2),line(p2,p0)
		ls0,ls1,ls2 = lineseg(p1,p2),lineseg(p0,p2),lineseg(p0,p1)
		q0,q1,q2=quadrance(ls0),quadrance(ls1),quadrance(ls2)
		s0,s1,s2=spread(l1,l2),spread(l0,l2),spread(l0,l1)

		self.l0,self.l1,self.l2=l0,l1,l2
		self.p0,self.p1,self.p2=p0,p1,p2
		self.ls0,self.ls1,self.ls2=ls0,ls1,ls2
		self.q0,self.q1,self.q2=q0,q1,q2
		self.s0,self.s1,self.s2=s0,s1,s2
		
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
		else: raise Exception('need center x,y and radial quadrance')
	def init_from_point_and_radial_q( self, p, rq ):
		self.center = p
		self.radial_quadrance = rq
		if (rq!=0): self.curvature_quadrance = Fraction(1,rq)
		else: self.curvature_quadrance = None
	def __str__( self ):
		return circle_txt(self)

class quaternion:
	def __init__(self,t,v):
		self.t,self.v=t,v

######## formulas, functions, theorems, operations

#### determinant of vectors
## assume rows of matrix = vectors
## note there is no matrix definition here

def determinant( *args ):
	for i in range(len(args)):
		if not isinstance(args[i],vector):
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

###### perpendicular

def red_perpendicular_vectors( v1, v2 ):
	raise Exception("not implemented ")
def green_perpendicular_vectors( v1, v2 ):
	raise Exception("not implemented ")
def blue_perpendicular_vectors( v1, v2 ):
	return v1.x*v2.x + v1.y*v2.y == 0

def red_perpendicular_linesegs( v1, v2 ):
	raise Exception("not implemented ")
def green_perpendicular_linesegs( v1, v2 ):
	raise Exception("not implemented ")
def blue_perpendicular_linesegs( v1, v2 ):
	raise Exception("not implemented ")

def red_perpendicular_lines( v1, v2 ):
	raise Exception("not implemented ")
def green_perpendicular_lines( v1, v2 ):
	raise Exception("not implemented ")
def blue_perpendicular_lines( v1, v2 ):
	raise Exception("not implemented ")


def perpendicular( *args, **kwargs ):
	if 'color' in kwargs.keys(): color=kwargs['color']
 	else: color='blue'

	if color=='red':
		perpendicular_vectors = red_perpendicular_vectors
		perpendicular_lines = red_perpendicular_lines
		perpendicular_linesegs = red_perpendicular_linesegs
	elif color == 'green':
		perpendicular_vectors = green_perpendicular_vectors
		perpendicular_lines = green_perpendicular_lines
		perpendicular_linesegs = green_perpendicular_linesegs
	elif color == 'blue':
		perpendicular_vectors = blue_perpendicular_vectors
		perpendicular_lines = blue_perpendicular_lines
		perpendicular_linesegs = blue_perpendicular_linesegs

	if isinstance(args[0],point): # and isinstance(args[1],point):
		raise Exception( "not implemented")
	if isinstance(args[0],line) and isinstance(args[1],line):
		return perpendicular_lines( args[0], args[1] )
	if isinstance(args[0],lineseg) and isinstance(args[1],lineseg):
		return perpendicular_linesegs( args[0], args[1] )
	if isinstance(args[0],vector) and isinstance(args[1],vector):
		return perpendicular_vectors( args[0], args[1] )
	return None




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

def meet( *args ):
	if isinstance(args[0],line) and isinstance(args[1],line):
		return meet_lines( args[0], args[1] )
	if isinstance(args[0],line) and isinstance(args[1],point):
		return meet_line_and_point( args[0], args[1] )
	if isinstance(args[0],point) and isinstance(args[1],line):
		return meet_line_and_point( args[1], args[0] )
	raise Exception(' not implemented' + str(args) )

############################## 1-dimensional projective geometry

# see NJW's paper, arxiv.org/pdf/math/0701338v1.pdf

class projective_form:
	def __init__(self, *args):
		crash_if_nonrationals( args )
		self.d,self.e,self.f=args[0],args[1],args[2]
	def __str__( self ):
		return projective_form_txt(self)
	def discriminant( self ):
		return self.d*self.f-sqr(self.e)

blue_projective_form = projective_form(1,0,1)
red_projective_form = projective_form(1,0,-1)
green_projective_form = projective_form(0,1,0)

def ppoint_nullcheck( ppoint, pform ):
	x,y=ppoint.x,ppoint.y
	d,e,f=pform.d,pform.e,pform.f
	return d*sqr(x)+2*e*x*y+f*sqr(y)

def projective_point( *args ):
	if args[0]==0 and args[1]==0:
		raise Exception('projective point cannot have x & y as 0 ')
	return point(args[0],args[1])

def ppoint_perpendicular( *args, **kwargs ):
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

def projective_quadrance_blue( *args ):
	return projective_quadrance( *args, color='blue' )
def projective_quadrance_red( *args ):
	return projective_quadrance( *args, color='red' )
def projective_quadrance_green( *args ):
	return projective_quadrance( *args, color='green' )

def projective_quadrance( *args, **kwargs ):
	if 'color' in kwargs.keys(): color=kwargs['color']
 	else: color='blue'

	if color=='blue': form=blue_projective_form
	elif color == 'green': form=green_projective_form
	elif color == 'red': form=red_projective_form

	for arg in args:
		if isinstance( arg, projective_form ):
			form = arg

	return projective_quadrance_wform( args[0], args[1], form )

def projective_quadrance_wform( *args ):
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

def projective_triple_spread( *args ):
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

def mirrorx( *args ):
	if checktypes(triangle,*args) and len(args)==1:
		return mirrorx_triangle( args[0] )
	else: raise Exception('mirror not implemented')
def mirrory( *args ):
	if checktypes(triangle,*args) and len(args)==1:
		return mirrory_triangle( args[0] )
	else: raise Exception('mirror not implemented')
def mirrorz( *args ):
	if checktypes(triangle,*args) and len(args)==1:
		return mirrorz_triangle( args[0] )
	else: raise Exception('mirror not implemented')

# translate a triangle by a vector. example, triangle 0,0 1,0 0,1 by vector 2,0
# result is 2,0 3,0 2,1
def translate_triangle_by_vector( t, v ):
	return triangle( t.p0+v, t.p1+v, t.p2+v )
def translate( *args ):
	if len(args)<2: raise Exception( 'need 2 objects for translation' )
	if checktypes( vector, args[0] ) and checktypes( triangle, args[1] ):
		return translate_triangle_by_vector( args[1], args[0] )
	if checktypes( triangle, args[0] ) and checktypes( vector, args[1] ):
		return translate_triangle_by_vector( args[0], args[1] )

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

####### calculate left hand side and right hand side of various formulas


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

def cross_law_lhs( tri ):
	return sqr(tri.q0+tri.q1-tri.q2)
	
def cross_law_rhs( tri ):
	cross = 1-tri.s2
	return 4*tri.q0*tri.q1*(cross)

def spread_law( tri ):
	a,b,c = tri.s0/tri.q0 , tri.s1/tri.q1 , tri.s2/tri.q2
	return str(a)+', '+str(b)+', '+str(c)

def triple_spread_lhs( tri ):
	return sqr( tri.s0 + tri.s1 + tri.s2 )

def triple_spread_rhs( tri ):
	s0,s1,s2 = tri.s0, tri.s1, tri.s2
	return 2 * ( s0*s0 + s1*s1 + s2*s2 ) + 4*s0*s1*s2

def pythagoras_lhs( tri ):
	return tri.q0 + tri.q1

def pythagoras_rhs( tri ):
	return tri.q2



###### formulas, functions, theorems - chromogeometry

def colored_quadrance_lhs( p0, p1 ):
	return sqr(blue_quadrance( p0, p1 ))

def colored_quadrance_rhs( p0, p1 ):
	return sqr(red_quadrance(p0, p1)) + sqr(green_quadrance(p0, p1))

def colored_spread_lhs( l0, l1 ):
	bs = blue_spread_lines( l0, l1 )
	rs = red_spread_lines( l0, l1 )
	gs = green_spread_lines( l0, l1 )
	return 1/bs + 1/rs + 1/gs

def colored_spread_rhs( l0, l1 ):
	return 2


###### anti-symmetric polynomials

# special polynomials used in many areas of geometry, especially 
# chromogeometry.
# 
# an anti-symmetrical polynomial is generated from an 'input monomial' 
# by transposing subscripts/indexes of variables
#
# example:
# input 'x1y2' returns six terms, by transposing '1' and '2' in a pattern:
# +x1y2 -x1y3 +x2y3 -x3y2 +x3y1 -x2y1
# 
# this particular sum is twice the signed area of the triangle of the 3 points
# x1,y1 x2,y2 x3,y3 
#
# It can be a bit confusing b/c the 'input' doesnt list x3,y3. But if 
# you get the hang of the transpositions it can help to understand. 
# Another way to think about it is to consider input monomial as 
# sort of like a 'seed' and the six-term polynomial 'grows' out of it.
# 
# The easiest function to use in this code is eval_asympoly(): You give 
# it a monomial and some values for x1,y1 x2,y2 x3,y3. It generates the 
# complete antisymmetric polynomial and plugs in the values for you into 
# the six generated terms, then sums them together and gives the 
# resulting sum.
#
# eval_asympoly( 'x1*y2', 3,4, 3,0, 1,-2 ) -> returns 20
#
# The other functions are 'helpers'


# More examples of antisymmetric polynomials:
#
# given: a monomial
#
# follow these 6 steps to generate the six terms of the antisymmetric 
# polynomial:
#
# start with the subscripts as given. 
# replace '2' with '3', and vice versa
# replace '1' with '2', and vice versa
# replace '2' with '3', and vice versa
# replace '1' with '2', and vice versa
# replace '2' with '3', and vice versa
# now assign positive and negative: like so: + - + - + -

# examples:
#
# input x1y2 returns six terms:
# +x1y2 -x1y3 +x2y3 -x3y2 +x3y1 -x2y1
#
# input x1*x1*x2*y2 returns six terms:
# +x1*x1*x2*y2 -x1*x1*x3*y3 +x2*x2*x3*y3 -x3*x3*x2*y2 +x3*x3*x1*y1 -x2*x2*x1*y1
#
# input x1*x1*x1*y1 returns six terms:
# +x1*x1*x1*y1 -x1*x1*x1*y1 +x2*x2*x2*y2 -x3*x3*x3*y3 +x3*x3*x3*y3 -x2*x2*x2*y2



# replace s1 for s2, and vice versa, in the input string s.
# example: given 'xabx','a','b' return 'xbax'
def transpose( s, s1, s2 ):
	s = s.replace(s1,'______term1______').replace(s2,'_____term2_____')
	s = s.replace('______term1______',s2).replace('_____term2_____',s1)
	return s

# given string representation of input monomial, generate a string
# with the six terms of the antisymmetric polynomial
def gen_antisymmetric_polynomial_string( s ):
	term1 = s
	term2 = transpose( term1, '2', '3' )
	term3 = transpose( term2, '1', '2' )
	term4 = transpose( term3, '2', '3' )
	term5 = transpose( term4, '1', '2' )
	term6 = transpose( term5, '2', '3' )
	#term1 = '+'+term1
	term2 = '-'+term2
	term3 = '+'+term3
	term4 = '-'+term4
	term5 = '+'+term5
	term6 = '-'+term6
	return term1+term2+term3+term4+term5+term6

# generate and calc the value of an antisymmetric polyonmial, given an 
# input monomial and some values for the input variables.
#
# first input must be a string representing a monomial python expression
# second input must be a python dictionary mapping strings to Rationals.
# example:
# dic = { 'x1': 4, 'y1': 5, 'x2': 3, 'y2': 0, 'x3': 1, 'y3': -2 }
# calc_antisymmetric_polynomial( 'x1*y2', dic )
# result: 20
def calc_antisymmetric_polynomial( monomial, vardict ):
	asp_str = gen_antisymmetric_polynomial_string( monomial )
	return eval(asp_str,{},vardict)

#### antisymmetric polynomial convenience functions

def gen_asymp_dict_from_points( p1, p2, p3 ):
	dic = {}
	dic['x1'],dic['y1']=p1.x,p1.y
	dic['x2'],dic['y2']=p2.x,p2.y
	dic['x3'],dic['y3']=p3.x,p3.y
	return dic

def gen_asymp_dict_from_triangle( t ):
	return gen_asymp_dict_from_points( t.p0, t.p1, t.p2 )

def gen_asymp_dict_from_rationals( x1,y1,x2,y2,x3,y3 ):
	p1 = point(x1,y1)
	p2 = point(x2,y2)
	p3 = point(x3,y3)
	return gen_asymp_dict_from_points( p1, p2, p3 )

def eval_asympoly_from_triangle( monomial, tri ):
	vardict = gen_asymp_dict_from_triangle( tri )
	return calc_antisymmetric_polynomial( monomial, vardict )

def eval_asympoly_from_points( monomial, p1, p2, p3 ):
	vardict = gen_asymp_dict_from_points( p1, p2, p3 )
	return calc_antisymmetric_polynomial( monomial, vardict )

def eval_asympoly_from_rationals( monomial, x1,y1,x2,y2,x3,y3 ):
	vardict = gen_asymp_dict_from_rationals( x1,y1,x2,y2,x3,y3 )
	return calc_antisymmetric_polynomial( monomial, vardict )

# easiest version to use. Examples:
# eval_asympoly('x1*y2',3,4,3,0,1,-2) -> returns 20
# p1,p2,p3 = point(3,4),point(3,0),point(1,-2) 
# eval_asympoly('x1*y2',p1,p2,p3) -> returns 20
# t = triangle(p1,p2,p3)
# eval_asympoly('x1*y2',t) -> returns 20
def eval_asympoly( *args ):
	if len(args)<2: raise Exception('need monomial, pointdata')
	if not isinstance(args[0],str):
		raise Exception('arg[0] s/b string')
	monomial = args[0]
	if checktype(triangle, args[1]):
		return eval_asympoly_from_triangle( monomial, args[1] )
	if checktype(point, args[1]) and checktype(point, args[2]):
		if checktype(point, args[3]):
			p1,p2,p3=args[1],args[2],args[3]
			return eval_asympoly_from_points( monomial, p1, p2, p3 )
	if checktype(Fraction, args[1]):
		x1,y1,x2,y2,x3,y3 = args[1],args[2],args[3],args[4],args[5],args[6]
		return eval_asympoly_from_rationals( monomial, x1,y1,x2,y2,x3,y3 )
	if checktype(int, args[1]):
		x1,y1,x2,y2,x3,y3 = args[1],args[2],args[3],args[4],args[5],args[6]
		return eval_asympoly_from_rationals( monomial, x1,y1,x2,y2,x3,y3 )
	
############################### triangle centers


############## orthocenters

def blue_orthocenter_from_triangle( t ):
	if not checktype(triangle,t): raise Exception('need triangle')
	terma = eval_asympoly( 'x1*x2*y2', t )
	termb = eval_asympoly( 'y1*y2*y2', t )
	termc = eval_asympoly( 'x1*y2', t )
	termd = eval_asympoly( 'x1*y1*y2', t )
	terme = eval_asympoly( 'x1*x1*x2', t )
	termf = eval_asympoly( 'x1*y2', t )
	x = Fraction( terma + termb, termc )
	y = Fraction( termd + terme, termf )
	return point(x,y)

def red_orthocenter_from_triangle( t ):
	if not checktype(triangle,t): raise Exception('need triangle')
	terma = eval_asympoly( 'x1*x2*y2', t )
	termb = eval_asympoly( 'y1*y2*y2', t )
	termc = eval_asympoly( 'x1*y2', t )
	termd = eval_asympoly( 'x1*y1*y2', t )
	terme = eval_asympoly( 'x1*x1*x2', t )
	termf = eval_asympoly( 'x1*y2', t )
	x = Fraction( terma - termb, termc )
	y = Fraction( termd - terme, termf )
	return point(x,y)

def green_orthocenter_from_triangle( t ):
	if not checktype(triangle,t): raise Exception('need triangle')
	terma = eval_asympoly( 'x1*x1*y2', t )
	termb = eval_asympoly( 'x1*x2*y1', t )
	termc = eval_asympoly( 'x1*y2', t )
	termd = eval_asympoly( 'x1*y2*y2', t )
	terme = eval_asympoly( 'x1*y1*y2', t )
	termf = eval_asympoly( 'x1*y2', t )
	x = Fraction( terma + termb, termc )
	y = Fraction( termd - terme, termf )
	return point(x,y)

def blue_orthocenter_from_points( p1, p2, p3 ):
	t = triangle( p1, p2, p3 )
	blue_orthocenter_from_triangle( t )
def red_orthocenter_from_points( p1, p2, p3 ):
	t = triangle( p1, p2, p3 )
	red_orthocenter_from_triangle( t )
def green_orthocenter_from_points( p1, p2, p3 ):
	t = triangle( p1, p2, p3 )
	green_orthocenter_from_triangle( t )


def blue_orthocenter( *args ):
	if checktype(triangle, args[0]):
		return blue_orthocenter_from_triangle( args[0] )
	if checktype(point, args[0]) and checktype(point, args[1]):
		if checktype(point, args[2]):
			p1,p2,p3=args[0],args[1],args[2]
			return blue_orthocenter_from_points( p1, p2, p3 )
def red_orthocenter( *args ):
	if checktype(triangle, args[0]):
		return red_orthocenter_from_triangle( args[0] )
	if checktype(point, args[0]) and checktype(point, args[1]):
		if checktype(point, args[2]):
			p1,p2,p3=args[0],args[1],args[2]
			return red_orthocenter_from_points( p1, p2, p3 )
def green_orthocenter( *args ):
	if checktype(triangle, args[0]):
		return green_orthocenter_from_triangle( args[0] )
	if checktype(point, args[0]) and checktype(point, args[1]):
		if checktype(point, args[2]):
			p1,p2,p3=args[0],args[1],args[2]
			return green_orthocenter_from_points( p1, p2, p3 )

orthocenter=blue_orthocenter


def blue_centroid( t ):
	x = avg(t.p0.x,t.p1.x,t.p2.x)	
	y = avg(t.p0.y,t.p1.y,t.p2.y)	
	return point(x,y)
def red_centroid( t ):
	return blue_centroid(t)
def green_centroid( t ):
	return blue_centroid(t)
centroid=blue_centroid

############## bounding box

def bounding_box_circle( c ):
	xmin = c.center.x-babylonian_square_root(abs(c.radial_quadrance))
	xmax = c.center.x+babylonian_square_root(abs(c.radial_quadrance))
	ymin = c.center.y-babylonian_square_root(abs(c.radial_quadrance))
	ymax = c.center.y+babylonian_square_root(abs(c.radial_quadrance))
	return point(xmin,ymin),point(xmax,ymax)

def bounding_box_triangle( t ):
	xmin = min(t.p0.x,t.p1.x,t.p2.x)
	ymin = min(t.p0.y,t.p1.y,t.p2.y)
	xmax = max(t.p0.x,t.p1.x,t.p2.x)
	ymax = max(t.p0.y,t.p1.y,t.p2.y)
	return point(xmin,ymin),point(xmax,ymax)
def bounding_box_triangles( ts ):
	minp,maxp = bounding_box_triangle(ts[0])
	tmpbox = bounding_box(minp,maxp)
	for t in ts: tmpbox.extend(bounding_box_triangle(t))
	return tmpbox.min,tmpbox.max
def bounding_box_circles( cs ):
	minp,maxp = bounding_box_circle(cs[0])
	tmpbox = bounding_box(minp,maxp)
	for c in cs: tmpbox.extend(bounding_box_circle(c))
	return tmpbox.min,tmpbox.max
def bounding_box_points( pts ):
	xmin,ymin,xmax,ymax=pts[0].x,pts[0].y,pts[0].x,pts[0].y
	for p in pts:
		xmin = min(xmin,p.x)
		ymin = min(ymin,p.y)
		xmax = max(xmax,p.x)
		ymax = max(ymax,p.y)
	return point(xmin,ymin),point(xmax,ymax)
def bounding_box_bboxes( boxes ):
	tmpbox = bounding_box(boxes[0].min,boxes[0].max);
	for b in boxes:
		tmpbox.extend( b.min, b.max )
	return tmpbox.min,tmpbox.max
def bounding_width( *args ):
	if checktypes(triangle,args) and len(args==1):
		minp,maxp = bbox_triangle( args[0] )
		return Fraction(minp.x+maxp.x,2)
def bounding_height( *args ):
	if checktypes(triangle,args) and len(args==1):
		minp,maxp = bbox_triangle( args[0] )
		return Fraction(minp.y+maxp.y,2)

class bounding_box:
	def __init__(self,*args):
		testmin,testmax = None,None
		if checktypes(triangle,*args):
			testmin,testmax = bounding_box_triangles( args )
		elif checktypes(point,*args):
			testmin,testmax = bounding_box_points( args )
		elif checktypes(bounding_box,*args):
			testmin,testmax = bounding_box_bboxes( args )
		elif checktypes(circle,*args):
			testmin,testmax = bounding_box_circles( args )
		elif checktypes(list,*args):
			if len(args)==2 and checkrationals(args[0][0]):
				xs,ys=args[0],args[1]
				testmin=point(min(xs),min(ys))
				testmax=point(max(xs),max(ys))
			else:
				for l in args:
					for item in l:
						self.extend(item)
					
		else:
			raise Exception('unknown types:'+str(args))
		self.min,self.max = testmin,testmax
	def extend(self,*args):
		testmin,testmax=self.min,self.max
		if checktypes(triangle,*args):
			testmin,testmax = bounding_box_triangles( args )
		elif checktypes(point,*args):
			testmin,testmax = bounding_box_points( args )
		elif checktypes(bounding_box,*args):
			testmin,testmax = bounding_box_bboxes( args )
		elif checktypes(circle,*args):
			testmin,testmax = bounding_box_circles( args )
		elif checktypes(list,*args):
			if len(args)==2 and checkrationals(args[0][0]):
				xs,ys=args[0],args[1]
				testmin=point(min(xs),min(ys))
				testmax=point(max(xs),max(ys))
			else:
				for l in args:
					for item in l:
						self.extend(item)
		elif checktypes(tuple,*args):
			for l in args:
				for item in l:
					self.extend(item)
		else: raise Exception('cannot extend,unknown type',args)
		self.min.x = min(testmin.x,self.min.x)
		self.min.y = min(testmin.y,self.min.y)
		self.max.x = max(testmax.x,self.max.x)
		self.max.y = max(testmax.y,self.max.y)
		return self
	def __add__( self, p): return self.extend( p )
	def add( self, p): return self.extend( p )
	def addto( self, p): return self.extend( p )
	def __str__(self): return bounding_box_txt(self)
	def width(self): return self.max.x-self.min.x
	def height(self): return self.max.y-self.min.y
	def frame(self): # slightly larger box
		newminx = self.min.x - self.width() * Fraction(5,100)
		newmaxx = self.max.x + self.width() * Fraction(5,100)
		newminy = self.min.y - self.height() * Fraction(5,100)
		newmaxy = self.max.y + self.height() * Fraction(5,100)
		return point(newminx,newminy),point(newmaxx,newmaxy)

############ circumcenters

def blue_circumcenter_from_triangle( t ):
	if not checktype(triangle,t): raise Exception('need triangle')
	terma = eval_asympoly( 'x1*x1*y2', t )
	termb = eval_asympoly( 'y1*y1*y2', t )
	termc = eval_asympoly( 'x1*y2', t )
	termd = eval_asympoly( 'x1*y2*y2', t )
	terme = eval_asympoly( 'x1*x2*x2', t )
	termf = eval_asympoly( 'x1*y2', t )
	x = Fraction( terma + termb, 2 * termc )
	y = Fraction( termd + terme, 2 * termf )
	return point(x,y)

def red_circumcenter_from_triangle( t ):
	if not checktype(triangle,t): raise Exception('need triangle')
	terma = eval_asympoly( 'x1*x1*y2', t )
	termb = eval_asympoly( 'y1*y1*y2', t )
	termc = eval_asympoly( 'x1*y2', t )
	termd = eval_asympoly( 'x1*y2*y2', t )
	terme = eval_asympoly( 'x1*x2*x2', t )
	termf = eval_asympoly( 'x1*y2', t )
	x = Fraction( terma - termb, 2 * termc )
	y = Fraction( termd - terme, 2 * termf )
	return point(x,y)

def green_circumcenter_from_triangle( t ):
	if not checktype(triangle,t): raise Exception('need triangle')
	terma = eval_asympoly( 'x1*x2*y2', t )
	termb = 0
	termc = eval_asympoly( 'x1*y2', t )
	termd = eval_asympoly( 'x1*y1*y2', t )
	terme = 0
	termf = eval_asympoly( 'x1*y2', t )
	x = Fraction( terma + termb, termc )
	y = Fraction( termd - terme, termf )
	return point(x,y)

def blue_circumcenter_from_points( p1, p2, p3 ):
	t = triangle( p1, p2, p3 )
	blue_circumcenter_from_triangle( t )
def red_circumcenter_from_points( p1, p2, p3 ):
	t = triangle( p1, p2, p3 )
	red_circumcenter_from_triangle( t )
def green_circumcenter_from_points( p1, p2, p3 ):
	t = triangle( p1, p2, p3 )
	green_circumcenter_from_triangle( t )


def blue_circumcenter( *args ):
	if checktype(triangle, args[0]):
		return blue_circumcenter_from_triangle( args[0] )
	if checktype(point, args[0]) and checktype(point, args[1]):
		if checktype(point, args[2]):
			p1,p2,p3=args[0],args[1],args[2]
			return blue_circumcenter_from_points( p1, p2, p3 )
def red_circumcenter( *args ):
	if checktype(triangle, args[0]):
		return red_circumcenter_from_triangle( args[0] )
	if checktype(point, args[0]) and checktype(point, args[1]):
		if checktype(point, args[2]):
			p1,p2,p3=args[0],args[1],args[2]
			return red_circumcenter_from_points( p1, p2, p3 )
def green_circumcenter( *args ):
	if checktype(triangle, args[0]):
		return green_circumcenter_from_triangle( args[0] )
	if checktype(point, args[0]) and checktype(point, args[1]):
		if checktype(point, args[2]):
			p1,p2,p3=args[0],args[1],args[2]
			return green_circumcenter_from_points( p1, p2, p3 )

circumcenter=blue_circumcenter



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

def blue_ninepointcircle( tri ):
	bnc = blue_ninepointcenter(tri)
	return circle( bnc , blue_quadrance( bnc, midpoint(tri[0],tri[1]) ) )
def red_ninepointcircle( tri ):
	rnc = red_ninepointcenter(tri)
	return circle( rnc , red_quadrance( rnc, midpoint(tri[0],tri[1]) ) )
def green_ninepointcircle( tri ):
	gnc = green_ninepointcenter(tri)
	return circle( gnc , green_quadrance( gnc, midpoint(tri[0],tri[1]) ) )

circumradial_quadrance=blue_circumradial_quadrance



######################## nine point centers

def blue_ninepointcenter_from_triangle( t ):
	if not checktype(triangle,t): raise Exception('need triangle')
	p1 = red_circumcenter_from_triangle( t )
	p2 = green_circumcenter_from_triangle( t )
	return midpoint_from_points( p1, p2 )

def red_ninepointcenter_from_triangle( t ):
	if not checktype(triangle,t): raise Exception('need triangle')
	p1 = blue_circumcenter_from_triangle( t )
	p2 = green_circumcenter_from_triangle( t )
	return midpoint_from_points( p1, p2 )

def green_ninepointcenter_from_triangle( t ):
	if not checktype(triangle,t): raise Exception('need triangle')
	p1 = blue_circumcenter_from_triangle( t )
	p2 = red_circumcenter_from_triangle( t )
	return midpoint_from_points( p1, p2 )

def blue_ninepointcenter_from_points( p1, p2, p3 ):
	t = triangle( p1, p2, p3 )
	return blue_ninepointcenter_from_triangle( t )
def red_ninepointcenter_from_points( p1, p2, p3 ):
	t = triangle( p1, p2, p3 )
	return red_ninepointcenter_from_triangle( t )
def green_ninepointcenter_from_points( p1, p2, p3 ):
	t = triangle( p1, p2, p3 )
	return green_ninepointcenter_from_triangle( t )

def blue_ninepointcenter( *args ):
	if checktype(triangle, args[0]):
		return blue_ninepointcenter_from_triangle( args[0] )
	elif checktype(point, args[0]) and checktype(point, args[1]):
		if checktype(point, args[2]):
			p1,p2,p3=args[0],args[1],args[2]
			return blue_ninepointcenter_from_points( p1, p2, p3 )
	else: raise Exception('unknown input type')
def red_ninepointcenter( *args ):
	if checktype(triangle, args[0]):
		return red_ninepointcenter_from_triangle( args[0] )
	elif checktype(point, args[0]) and checktype(point, args[1]):
		if checktype(point, args[2]):
			p1,p2,p3=args[0],args[1],args[2]
			return red_ninepointcenter_from_points( p1, p2, p3 )
	else: raise Exception('unknown input type')
def green_ninepointcenter( *args ):
	if checktype(triangle, args[0]):
		return green_ninepointcenter_from_triangle( args[0] )
	elif checktype(point, args[0]) and checktype(point, args[1]):
		if checktype(point, args[2]):
			p1,p2,p3=args[0],args[1],args[2]
			return green_ninepointcenter_from_points( p1, p2, p3 )
	else: raise Exception('unknown input type')
ninepointcenter=blue_ninepointcenter




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




############## square root bounds
### the square root of a rational number is often irrational. 
### we can find a rational approximation, thanks to the ancient Iraqis / 
### Babylonians.
### 
### there is also a 'is perfect square?' test function
###
### we ignore negative roots here. and imaginary roots.

# return [r1, r2] such that the sqrt(s) is guaranteed to be between them
def square_root_rough_bounds_int( s ):
	bitlength = int(Fraction(s.bit_length()-1,2))
	guess = 1
	for i in range(0,bitlength): guess *= 2
	return guess,guess*2

# return rational approximation of square root using Babylonian's method
# iterate for maxdepth iterations or until answer>maxbits. 
def babylonian_square_root_int( s, maxdepth=10, maxbits=256, firstguess=1 ):
	guesses=[firstguess]
	for i in range(1,maxdepth):
		lastguess = guesses[i-1]
		newguess = avg(lastguess,Fraction(s,lastguess))
		if lastguess==newguess: break
		if sqr(int(newguess))==s: # perfect square
			guesses += [ int(newguess) ]
			break
		# prevent digit ballooning causing Big Int freezing
		if (newguess.numerator.bit_length()+newguess.denominator.bit_length())>maxbits:
			break
		guesses += [newguess]
	#print 'guesses for root of ',s,float(s)
	#for g in guesses: print ' ',g,float(g),float(g*g)
	return guesses[-1]

def babylonian_square_root_for_fraction( s, maxdepth=10,maxbits=256 ):
	lo_n,hi_n = square_root_rough_bounds_int( s.numerator )
	lo_d,hi_d = square_root_rough_bounds_int( s.denominator )
	numer=babylonian_square_root_int( s.numerator, maxdepth, maxbits, lo_n )
	denom=babylonian_square_root_int( s.denominator, maxdepth, maxbits, lo_d )
	return Fraction(numer,denom)

def is_perfect_square(s):
	x = babylonian_square_root(s)
	if x*x==s: return True
	return False

# return rational approximation of square root of s
def babylonian_square_root( s, maxdepth=10, maxbits=256 ):
	if s<0: raise Exception('sqrt -1 aint rational')
	return babylonian_square_root_for_fraction( Fraction(s),maxdepth,maxbits )

##################### render objects into text

def bounding_box_txt( b ):
	s = '[ ' + str(b.min) + ' , ' + str(b.max) + ' ]'
	return s

def point_txt( p ):
	s = '['+str(p.x)+','+str(p.y)
	if hasattr(p,'z'): s += ',' + str(p.z)
	s += ']'
	return s

def bivector_txt( bv ):
	return vector_txt( bv.v1 ) + 'V' + vector_txt( bv.v2 ) + ' value: ' + str(bv.value())

def vector_txt( v ):
	s = '('+str(v.x)+','+str(v.y)
	if hasattr(v,'z'): s += ',' + str(v.z)
	s += ')'
	return s

def line_txt( l ):
	s = '<'+str(l.a)+":"+str(l.b)+":"+str(l.c)
	s += '>'
	return s

def lineseg_txt( l ):
	s = str(l.p0) +'-'+str(l.p1)
	return s

def projective_form_txt( pf ):
	s = str('['+ str(pf.d)+':'+str(pf.e)+':'+str(pf.f)+']')
	if pf.d==1 and pf.e==0 and pf.f == 1: s += ' (blue)'
	elif pf.d==1 and pf.e==0 and pf.f == -1: s += ' (red)'
	elif pf.d==0 and pf.e==1 and pf.f == 0: s += ' (green)'
	else: s += ' (unknown)'
	return s

def circle_txt( c ):
	s = str('['+str(c.center)+','+str(c.radial_quadrance)+'<->'+str(c.curvature_quadrance)+']')
	return s

def triangle_txt( tri ):
	spreads = str(tri.s0)+','+str(tri.s1)+','+str(tri.s2)
	line_eqns = str(tri.l0)+','+str(tri.l1)+','+str(tri.l2)
	linesegs = str(tri.ls0)+' '+str(tri.ls1)+' '+str(tri.ls2)
	points = str(tri.p0)+','+str(tri.p1)+','+str(tri.p2)
	quadrances = str(tri.q0)+','+str(tri.q1)+','+str(tri.q2)
	s ='\ntriangle: '
	s+='\n line eqns: ' + line_eqns
	s+='\n line segs: ' + linesegs
	s+='\n points: ' + points
	s+='\n blue quadrances: ' + quadrances
	s+='\n blue spreads: ' + spreads
	return s


############################## draw in graphics
# everything is done with rationals, except for a few
# calls to matplotlib's "ax" functions that require floats.

plotstarted=False
fig,ax,plt=None,None,None
plotbbox=None

# call matplotlib's "ax" plot function 'func', but convert from 
# rationals to floats first.
#
# example: 
#   ax_floatplot( [1,5],[2,12],ax.scatter) # < scatter plot points at 1,2 5,12
#   ax_floatplot( [0,4,5],[2,3,5],ax.plot ) #< plot line from 0,2 to 4,3 to 5,5
def ax_floatplot( xs, ys, func ):
	plotbbox.extend( xs,ys )
	fxs,fys=[],[]
	for x in xs: fxs += [float(x)]
	for y in ys: fys += [float(y)]
	func( xs, ys )

def plotinit( startitem ):
	global plotstarted,fig,ax,plt,plotbbox
	if plotstarted: return
	import numpy as np
	import matplotlib.pylab as plt
	fig,ax = plt.subplots(figsize=(8,8))
	plotstarted = True
	plotbbox = bounding_box( startitem )

def plotshow():
	ax.set_aspect(1)
	fmin,fmax = plotbbox.frame()
	ax.set_xlim(float(fmin.x),float(fmax.x))
	ax.set_ylim(float(fmin.y),float(fmax.y))
	plt.show()
	
def plot_triangles( *args ):
	if checktypes(list,*args):
		plot_triangles(*args[0])
		return
	triangles = args
	plotinit( triangles[0] )
	print len(triangles), 'triangles'
	xs,ys=[],[]
	for t in triangles:
		xs,ys=[],[]
		for i in 0,1,2:
			xs+=[t[i].x]
			ys+=[t[i].y]
		xs += [xs[0]]
		ys += [ys[0]]
		ax_floatplot(xs,ys,ax.plot)

def plot_points( *args ):
	if checktypes(point,*args):
		plotinit( args[0] )
		print len( args ), 'points'
		xs,ys=[],[]
		for p in args:
			xs += [p.x]
			ys += [p.y]
		ax_floatplot(xs,ys,ax.scatter) # scatter plot
	elif checktypes(list,*args):
		print len(args)
		if checktypes(point,args[0]):
			plot_points(*args[0])
		elif checktypes(list,args[0]) and len(args)==2:
			plotinit( point(args[0][0],args[1][0]) )
			ax_floatplot(args[0],args[1],ax.scatter) # scatter plot
	else: raise Exception('unknown type fed to plot_points')
		

def plot_blue_circle_w_radius( cx, cy, cr, depth ):
	pdic={}
	xs,ys=[],[]
	for m in range(0,depth):
		for n in range(0,depth):
			if (blueq(m,n)==0): continue
			x = cr*Fraction(redq(m,n),blueq(m,n))
			y = cr*Fraction(greenq(m,n),blueq(m,n))
			#print 'x,y,x^2+y^2',x,y,x*x+y*y
			pdic[x]=y
	sortedkeys = pdic.keys()
	sortedkeys.sort()
	# top half
	for key in sortedkeys:
		x,y=key,pdic[key]
		xs += [cx+x]
		ys += [cy+y]
	sortedkeys.reverse()
	# bottom half
	for key in sortedkeys:
		x,y=key,pdic[key]
		xs += [cx+x]
		ys += [cy-y]
	ax_floatplot(xs,ys,ax.plot)

# rational paramterization. 
def plot_blue_circles( *args ):
	if checktypes(list,*args):
		plot_blue_circles(*args[0])
		return
	circles = list(args)
	print len(circles), 'blue circles'
	plotinit( circles[0] )
	xs,ys=[],[]
	depth=10
	for c in circles:
		depth=8
		cx,cy=c.center.x,c.center.y
		cr = babylonian_square_root(c.radial_quadrance)
		plot_blue_circle_w_radius( cx, cy, cr, depth )

# (red circle = hyperbola)
# rational parameterization.
def plot_red_circle_w_radius( cx, cy, cr, depth ):
	pdic={}
	xs,ys=[],[]
	for m in range(0,int(Fraction(depth,2))):
		for n in range(-m,m):
			if (redq(m,n)==0): continue
			x = cr*Fraction(blueq(m,n),redq(m,n))
			y = cr*Fraction(greenq(m,n),redq(m,n))
			#print 'x,y,x^2-y^2',x,y,x*x-y*y
			pdic[y]=x
	sortedkeys = pdic.keys()
	sortedkeys.sort()
	# right half
	for key in sortedkeys:
		y,x=key,pdic[key]
		xs += [cx+x]
		ys += [cy+y]
	ax_floatplot(xs,ys,ax.plot)
	# left half
	xs,ys=[],[]
	for key in sortedkeys:
		y,x=key,pdic[key]
		xs += [cx-x]
		ys += [cy+y]
	ax_floatplot(xs,ys,ax.plot)

# (red circle = hyperbola)
# rational paramterization.
# imaginary radius.... represents red circles with negative radial quadrance.
# the hyperbola in this case is 'flipped' over the line x=y from the ordinary
# red circle
def plot_red_circle_w_imaginary_radius( cx, cy, cr, depth ):
	pdic={}
	for m in range(0,int(Fraction(depth,2))):
		for n in range(-m,m):
			if (redq(m,n)==0): continue
			y = cr*Fraction(blueq(m,n),redq(m,n))
			x = cr*Fraction(greenq(m,n),redq(m,n))
			#print 'x,y,x^2+y^2',x,y,x*x+y*y
			pdic[x]=y
	sortedkeys = pdic.keys()
	sortedkeys.sort()
	# top half
	xs,ys=[],[]
	for key in sortedkeys:
		x,y=key,pdic[key]
		xs += [cx+x]
		ys += [cy+y]
	ax_floatplot(xs,ys,ax.plot)
	# top half
	xs,ys=[],[]
	for key in sortedkeys:
		x,y=key,pdic[key]
		xs += [cx+x]
		ys += [cy-y]
	ax_floatplot(xs,ys,ax.plot)

# (red circle = hyperbola)
def plot_red_circles( *args ):
	if checktypes(list,*args):
		plot_red_circles(*args[0])
		return
	circles = list(args)
	print len(circles), 'red circles'
	plotinit( circles[0] )
	for c in circles:
		depth=10
		cx,cy=c.center.x,c.center.y
		if c.radial_quadrance>0:
			crlo = babylonian_square_root(c.radial_quadrance)
			plot_red_circle_w_radius( cx, cy, crlo, depth )
		else:
			crlo = babylonian_square_root(-c.radial_quadrance)
			plot_red_circle_w_imaginary_radius( cx, cy, crlo, depth )

def plot_green_circle_w_imaginary_radius( cx, cy, cr ):
	depth=5
	pdic={}
	for m in range(0,depth):
		for n in range(0,2*depth):
			if (greenq(m,n)==0): continue
			x = Fraction(m,n)
			y = Fraction(n,2*m)
			#print '2xy',x,y,2*x*y
			x = cr*x
			y = cr*y
			pdic[x]=y
	sortedkeys = pdic.keys()
	sortedkeys.sort()
	# right half
	xs,ys=[],[]
	for key in sortedkeys:
		x,y=key,pdic[key]
		xs += [cx-x]
		ys += [cy+y]
	ax_floatplot(xs,ys,ax.plot)
	# right half
	xs,ys=[],[]
	for key in sortedkeys:
		x,y=key,pdic[key]
		xs += [cx+x]
		ys += [cy-y]
	ax_floatplot(xs,ys,ax.plot)

def plot_green_circle_w_radius( cx, cy, cr ):
	depth=5
	pdic={}
	for m in range(0,depth):
		for n in range(0,2*depth):
			if (greenq(m,n)==0): continue
			x = Fraction(m,n)
			y = Fraction(n,2*m)
			#print '2xy',x,y,2*x*y
			x = cr*x
			y = cr*y
			pdic[x]=y
	sortedkeys = pdic.keys()
	sortedkeys.sort()
	# right half
	xs,ys=[],[]
	for key in sortedkeys:
		x,y=key,pdic[key]
		xs += [cx+x]
		ys += [cy+y]
	ax_floatplot(xs,ys,ax.plot)
	# right half
	xs,ys=[],[]
	for key in sortedkeys:
		x,y=key,pdic[key]
		xs += [cx-x]
		ys += [cy-y]
	ax_floatplot(xs,ys,ax.plot)

# (green circle = hyperbola)
# rational paramterization.
#
# bug - slow on small circles.
#
def plot_green_circles( *args ):
	if checktypes(list,*args):
		plot_green_circles(*args[0])
		return
	circles = list(args)
	print len(circles), 'green circles'
	plotinit( circles[0] )
	for c in circles:
		depth=5
		cx,cy=c.center.x,c.center.y
		if c.radial_quadrance>0:
			cr = babylonian_square_root(c.radial_quadrance)
			plot_green_circle_w_radius( cx, cy, cr )
		else:
			cr = babylonian_square_root(-c.radial_quadrance)
			plot_green_circle_w_imaginary_radius( cx, cy, cr )

plot_circles = plot_blue_circles



####################################3 shortcuts and conveniene functions
############ for the spelling challenged, frogetful, and inebriated

def is_paralell( l1, l2):
	return is_parallel( l1, l2 )

def is_green_perpendicular( l1, l2 ):
	raise Exception(" not implemented ")
	
def is_red_perpendicular( l1, l2 ):
	raise Exception(" not implemented ")
	
def is_blue_perpendicular( l1, l2 ):
	return spread( l1, l2 ) == 1

def is_perpendicular( l1, l2):
	return is_blue_perpendicular( l1, l2 )

def is_parallel( l1, l2):
	return spread( l1, l2 ) == 0

def intersection( l1, l2 ):
	return meet( l1, l2 )

# nice for doing paramterizations
def blueq( *args ):
	if checktypes(point,*args):
		if len(args)==1:
			return blue_quadrance(point(0,0),args[0])
		elif len(args)==2:
			return blue_quadrance(args[0],args[1])
		else: raise Exception('need 1 or 2 pts')
	elif checkrationals(*args):
		return blue_quadrance(point(0,0),point(args[0],args[1]))
	else: raise Exception('need point or x,y coords')
def redq( *args ):
	if checktypes(point,*args):
		if len(args)==1:
			return red_quadrance(point(0,0),args[0])
		elif len(args)==2:
			return red_quadrance(args[0],args[1])
		else: raise Exception('need 1 or 2 pts')
	elif checkrationals(*args):
		return red_quadrance(point(0,0),point(args[0],args[1]))
	else: raise Exception('need point or x,y coords')
def greenq( *args ):
	if checktypes(point,*args):
		if len(args)==1:
			return green_quadrance(point(0,0),args[0])
		elif len(args)==2:
			return green_quadrance(args[0],args[1])
		else: raise Exception('need 1 or 2 pts')
	elif checkrationals(*args):
		return green_quadrance(point(0,0),point(args[0],args[1]))
	else: raise Exception('need point or x,y coords')

def blue_quadrance_coordinates(x1,y1,x2,y2):
	return blue_quadrance_coords(x1,y1,x2,y2)
def red_quadrance_coordinates(x1,y1,x2,y2):
	return red_quadrance_coords(x1,y1,x2,y2)
def green_quadrance_coordinates(x1,y1,x2,y2):
	return green_quadrance_coords(x1,y1,x2,y2)

def blue_quadria(p1,p2,p3):
	return blue_quadrea(p1,p2,p3)
def red_quadria(p1,p2,p3):
	return red_quadrea(p1,p2,p3)
def green_quadria(p1,p2,p3):
	return green_quadrea(p1,p2,p3)

def blue_circum_center( tri ):
	return blue_circumcenter( tri )
def red_circum_center( tri ):
	return red_circumcenter( tri )
def green_circum_center( tri ):
	return green_circumcenter( tri )


def drawtriangles(tris): plot_triangles(tris)
def drawtriangle(tri): plot_triangles([tri])
def draw_triangle(tri): plot_triangles([tri])
def plottriangles(tris): plot_triangles(tris)
def plottriangle(tri): plot_triangles([tri])
def plot_triangle(tri): plot_triangles([tri])

def plotpoints(circs): plot_points(circs)
def plotpoint(circ): plot_points([circ])
def plot_point(circ): plot_points([circ])
def drawpoints(circs): plot_points(circs)
def drawpoint(circ): plot_points([circ])
def draw_point(circ): plot_points([circ])

def plotcircles(circs): plot_circles(circs)
def plotcircle(circ): plot_circles([circ])
def plot_circle(circ): plot_circles([circ])
def drawcircles(circs): plot_circles(circs)
def drawcircle(circ): plot_circles([circ])
def draw_circle(circ): plot_circles([circ])

def plotbluecircles(circs): plot_blue_circles(circs)
def plotbluecircle(circ): plot_blue_circles([circ])
def plot_blue_circle(circ): plot_blue_circles([circ])
def drawbluecircles(circs): plot_blue_circles(circs)
def drawbluecircle(circ): plot_blue_circles([circ])
def draw_blue_circle(circ): plot_blue_circles([circ])

def plotredcircles(circs): plot_red_circles(circs)
def plotredcircle(circ): plot_red_circles([circ])
def plot_red_circle(circ): plot_red_circles([circ])
def drawredcircles(circs): plot_red_circles(circs)
def drawredcircle(circ): plot_red_circles([circ])
def draw_red_circle(circ): plot_red_circles([circ])

def plotgreencircles(circs): plot_green_circles(circs)
def plotgreencircle(circ): plot_green_circles([circ])
def plot_green_circle(circ): plot_green_circles([circ])
def drawgreencircles(circs): plot_green_circles(circs)
def drawgreencircle(circ): plot_green_circles([circ])
def draw_green_circle(circ): plot_green_circles([circ])


def blue_ninepoint_center( *args ): return blue_ninepointcenter(*args)
def red_ninepoint_center( *args ): return red_ninepointcenter(*args)
def green_ninepoint_center( *args ): return green_ninepointcenter(*args)
def nine_point_triangle( tri ): return ninepoint_triangle( tri )
