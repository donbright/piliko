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
		else:
			crash_if_nonrationals( args )
			self.x,self.y=args[0],args[1]
			if (len(args)==3): self.z=args[2]
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
	def __mul__( self, scalar ):
		newv = vector( self.x * scalar, self.y * scalar )
		if hasattr(self,'z'): newv.z = self.z * scalar
		return newv
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
		if checktypes( point, *args ) and len(args)==3:
			self.init_from_points( args[0],args[1],args[2] )
		if checktypes( int, *args ) and len(args)==6:
			p1=point(args[0],args[1])
			p2=point(args[2],args[3])
			p3=point(args[4],args[5])
			self.init_from_points( p1, p2, p3 )

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

# circles are a bit different here. since the radius is not always rational
# even between two rational points, we instead store the 'radial quadrance',
# which is always rational between two rational points.
#
# in general, the hope is to avoid functions that require the use of radius.
# but in cases where we do need it, like plotting a graphical represnetation
# of the circle, please see the sqrt_bounds() function elsewhere in this code
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

def archimedes_function_3numbers(a,b,c): 
	return sqr(a+b+c) - 2*(a*a+b*b+c*c)

def archimedes_function( *args ):
	crash_if_nonrationals( *args )
	if not len(args)==3:
		raise Exception("Archimede's function requires 3 numbers")
	a=args[0]
	b=args[1]
	c=args[2]
	return archimedes_function_3numbers( a, b, c )

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
# chromogeometry generated from an 'input monomial' by transposing 
# subscripts/indexes of variables
#
# example:
# input 'x1y2' returns six terms, by transposing '1' and '2' in a pattern:
# +x1y2 -x1y3 +x2y3 -x3y2 +x3y1 -x2y1
# this particular sum is twice the signed area of the triangle of the 3 points
#  
#
# The easiest function to use here is eval_asympoly(): 
#
# eval_asympoly( 'x1*y2', 3,4, 3,0, 1,-2 ) -> returns 20
#
# The other functions are 'helpers'


# given: a monomial
#
# follow the 6 steps to generate the six terms of the antisymmetric 
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
	xmin = c.center.x-sqrt_bounds(c.radial_quadrance)[0]
	xmax = c.center.x+sqrt_bounds(c.radial_quadrance)[0]
	ymin = c.center.y-sqrt_bounds(c.radial_quadrance)[0]
	ymax = c.center.y+sqrt_bounds(c.radial_quadrance)[0]
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
	blue_ninepointcenter_from_triangle( t )
def red_ninepointcenter_from_points( p1, p2, p3 ):
	t = triangle( p1, p2, p3 )
	red_ninepointcenter_from_triangle( t )
def green_ninepointcenter_from_points( p1, p2, p3 ):
	t = triangle( p1, p2, p3 )
	green_ninepointcenter_from_triangle( t )

def blue_ninepointcenter( *args ):
	if checktype(triangle, args[0]):
		return blue_ninepointcenter_from_triangle( args[0] )
	if checktype(point, args[0]) and checktype(point, args[1]):
		if checktype(point, args[2]):
			p1,p2,p3=args[0],args[1],args[2]
			return blue_ninepointcenter_from_points( p1, p2, p3 )
def red_ninepointcenter( *args ):
	if checktype(triangle, args[0]):
		return red_ninepointcenter_from_triangle( args[0] )
	if checktype(point, args[0]) and checktype(point, args[1]):
		if checktype(point, args[2]):
			p1,p2,p3=args[0],args[1],args[2]
			return red_ninepointcenter_from_points( p1, p2, p3 )
def green_ninepointcenter( *args ):
	if checktype(triangle, args[0]):
		return green_ninepointcenter_from_triangle( args[0] )
	if checktype(point, args[0]) and checktype(point, args[1]):
		if checktype(point, args[2]):
			p1,p2,p3=args[0],args[1],args[2]
			return green_ninepointcenter_from_points( p1, p2, p3 )

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

################## omega triangle

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
### these routines provide rational 'bounds' that guarantee the irrational
### square root is 'between' them, as such. 
### 
### there is also a 'is perfect square?' test function
###
### we ignore negative roots here.

# return [r1, r2] such that the sqrt(s) is guaranteed to be between them
def square_root_rough_bounds( s ):
	bitlength = int(Fraction(s.bit_length(),2))
	guess = 2
	for i in range(0,bitlength-1): guess *= 2
	return guess,guess*2

# return r1 such that int( r1 squared ) = s
def babylonian_square_root_int( s, maxdepth=10, firstguess=1 ):
	guesses = [firstguess]
	for i in range(1,maxdepth):
		lastguess = guesses[i-1]
		newguess = avg(lastguess,Fraction(s,lastguess))
		if sqr(int(newguess))==s:
			newguess=int(newguess) # perfect sqr
		if int(sqr(newguess))==int(sqr(lastguess)): break
		guesses += [newguess]
	return guesses[-1]

# return [r1, r2] such that the sqrt(s) is guaranteed to be between them
# annnnd such that int(r1 squared) == int(r2 squared) == s 
# perfect squares's integer roots are detected and returned exactly.
def babylonian_square_root_bounds_for_int( s, maxdepth=10 ):
	# Thanks Wikipedia! Thanks Babylonians!
	lowerguess, upperguess = square_root_rough_bounds( s )
	lowerbound = babylonian_square_root_int( s, maxdepth, lowerguess )
	higherbound = babylonian_square_root_int( s, maxdepth, upperguess )
	return lowerbound,higherbound

# return [r1, r2] such that the sqrt(s) is guaranteed to be between them.
# how close is the approximation? i dont know. the numerator and 
# denominator are approximated separately with 
# babyloian_square_root_bounds_for_int() and then combined together in a 
# single fraction. 
#
# perfect squares are detected and returned exactly.
def babylonian_square_root_bounds_for_fraction( s, maxdepth=10 ):
	boundsn=babylonian_square_root_bounds_for_int( s.numerator, maxdepth )
	boundsd=babylonian_square_root_bounds_for_int( s.denominator, maxdepth )
	lower_numer,higher_numer = (boundsn[0]),(boundsn[1])
	lower_denom,higher_denom = (boundsd[0]),(boundsd[1])
	if s<1:
		lowbound = Fraction(lower_numer,lower_denom)
		highbound = Fraction(higher_numer,higher_denom)
	elif s>1:
		lowbound = Fraction(higher_numer,higher_denom)
		highbound = Fraction(lower_numer,lower_denom)
	else:
		lowbound = 1
		highbound = 1
	return lowbound,highbound

def is_perfect_square(s):
	lo,hi = babylonian_square_root_bounds(s)
	return lo==hi

def babylonian_square_root_bounds( s, maxdepth=10 ):
	return babylonian_square_root_bounds_for_fraction( Fraction(s) )

def sqrt_bounds( s ):
	return babylonian_square_root_bounds( s )

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
	s ='\n line eqns: ' + line_eqns
	s+='\n line segs: ' + linesegs
	s+='\n points: ' + points
	s+='\n quadrances: ' + quadrances
	s+='\n spreads: ' + spreads
	return s


############################## draw in graphics
# everything is done with rationals, except for a few
# calls to ax. functions that require floats.

plotstarted=False
fig,ax,plt=None,None,None
plotbbox=None

# call ax plot function 'func', but convert from rationals to floats first
# example ax_floatplot( [1],[2],ax.scatter) # < scatter plot point at 1,2
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
	
def plot_triangles( triangles ):
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

def plot_points( points ):
	plotinit( points[0] )
	print len(points), 'points'
	xs,ys=[],[]
	for p in points:
		xs += [p.x]
		ys += [p.y]
	ax_floatplot(xs,ys,ax.scatter) # scatter plot


# rational paramterization. 
def plot_blue_circles( circles ):
	print len(circles), 'circles'
	plotinit( circles[0] )
	xs,ys=[],[]
	depth=10
	for c in circles:
		print c
		xs,ys=[],[]
		pdic={}
		cx,cy,cr=c.center.x,c.center.y,sqrt_bounds(c.radial_quadrance)[0]
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

# (red circle = hyperbola)
# rational paramterization.
def plot_red_circle_core( cx, cy, cr, depth ):
	pdic={}
	xs,ys=[],[]
	for m in range(0,depth):
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
def plot_red_circles( circles ):
	print len(circles), 'red circles'
	plotinit( circles[0] )
	for c in circles:
		depth=5
		cx,cy=c.center.x,c.center.y
		crlo = sqrt_bounds(c.radial_quadrance)[0]
		crhi = sqrt_bounds(c.radial_quadrance)[1]
		plot_red_circle_core( cx, cy, crlo, depth )
		if crlo!=crhi: plot_red_circle_core( cx, cy, crhi, depth )
			

# (green circle = hyperbola)
# rational paramterization.
#
# bug - slow on small circles.
#
def plot_green_circles( circles ):
	print len(circles), 'green circles'
	plotinit( circles[0] )
	xs,ys=[],[]
	for c in circles:
		depth=10
		pdic={}
		cx,cy,cr=c.center.x,c.center.y,sqrt_bounds(c.radial_quadrance)[0]
		print cx,cy,cr
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
def blueq( m, n ):
	return blue_quadrance(point(0,0),point(m,n))
def redq( m, n ):
	return red_quadrance(point(0,0),point(m,n))
def greenq( m, n ):
	return green_quadrance(point(0,0),point(m,n))

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


def plotcircles(circs): plot_circles(circs)
def plotcircle(circ): plot_circles([circ])
def plot_circle(circ): plot_circles([circ])
def plottriangles(tris): plot_triangles(tris)
def plottriangle(tri): plot_triangles([tri])
def plot_triangle(tri): plot_triangles([tri])

def drawcircles(circs): plot_circles(circs)
def drawcircle(circ): plot_circles([circ])
def draw_circle(circ): plot_circles([circ])
def drawtriangles(tris): plot_triangles(tris)
def drawtriangle(tri): plot_triangles([tri])
def draw_triangle(tri): plot_triangles([tri])

def plotpoints(circs): plot_points(circs)
def plotpoint(circ): plot_points([circ])
def plot_point(circ): plot_points([circ])
def drawpoints(circs): plot_points(circs)
def drawpoint(circ): plot_points([circ])
def draw_point(circ): plot_points([circ])

