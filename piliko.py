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
		init_from_points( p0, p1, p2 )

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

class circle:
	def __init__(self, *args):
		if (len(args)<2): raise Exception('need center x,y and radius')
		if checkrationals(*args) and len(args)>=3:
			p = point(args[0],args[1])
			self.init_from_point_and_radius( p, args[2] )
		elif checktypes(point,args[0]) and checktypes(int,args[1]):
			self.init_from_point_and_radius( args[0], args[1] )
		elif checktypes(int,args[0]) and checktypes(point,args[1]):
			self.init_from_point_and_radius( args[1], args[0] )
		elif checktypes(point,args[0]) and checktypes(Fraction,args[1]):
			self.init_from_point_and_radius( args[0], args[1] )
		elif checktypes(Fraction,args[0]) and checktypes(point,args[1]):
			self.init_from_point_and_radius( args[1], args[0] )
	def init_from_point_and_radius( self, p, r ):
		self.center = p
		self.radius = r
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

# are three points collinear?
def collinear( *args ):
	for i in range(len(args)):
		if not isinstance(args[i],point):
			raise Exception('coolinear() requires points')
	if len(args)<3: raise Exception('collinear() needs 3 pts or more')
	p1,p2,p3 = args[0],args[1],args[2]
	result = eval_asympoly( 'x1*y2', p1,p2,p3 )
	if result==0: return True
	return False
#	l = line(args[0],args[1])
#	for i in range(2,len(args)):
#		tmp_point = args[i]
#		if meet( l, tmp_point ) == None: return False 
#	return True

def cross( l0, l1 ):
	checktypes( line, [l0,l1] )
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
	return squared_cross_ratio_points( p0, p1, p2, p3 ) == 1

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

# special polynomials used in many areas of geometry, especially chromogeometry
# generated from an 'input monomial'
#
# example:
# input 'x1y2' returns six terms:
# +x1y2 -x1y3 +x2y3 -x3y2 +x3y1 -x2y1
#  
# given 3 points, these six terms are twice the signed area of the triangle. 

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
	if checktype(Rational, args[1]):
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


def red_centroid( tri ):
	raise Exception(" not implemented ")
def green_centroid( tri ):
	raise Exception(" not implemented ")
def blue_centroid( tri ):
	raise Exception(" not implemented ")


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



# circumquadrance -> basiclly the square of circumradius.
# whats circumradius? the radius of a circle that has all 3 points of the
# triangle lying exactly on the circle
def blue_circum_quadrance( tri ):
	p1 = blue_circumcenter( tri )
	p2 = tri.p0
	return blue_quadrance_points( p1, p2 )
def red_circum_quadrance( tri ):
	p1 = red_circumcenter( tri )
	p2 = tri.p0
	return red_quadrance_points( p1, p2 )
def green_circum_quadrance( tri ):
	p1 = green_circumcenter( tri )
	p2 = tri.p0
	return green_quadrance_points( p1, p2 )

circum_quadrance=blue_circum_quadrance



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







##################### render objects into text

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
	s = str('['+str(c.center)+','+str(c.radius)+']')
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


###### convenience - for bad spelling, or just grammatical variatinos

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



############33 plotting in graphics 

def plot_triangles( triangles ):
	print len(triangles), 'triangles'
	import numpy as np
	import matplotlib.pylab as plt
	fig,ax = plt.subplots(figsize=(8,8))
	xs,ys=[],[]
	for t in triangles:
		for i in 0,1,2:
			xs += [float(t[i].x)]
			ys += [float(t[i].y)]
	ax.set_xlim([min(xs)-2,max(xs)+2])
	ax.set_ylim([min(ys)-2,max(ys)+2])
	for t in triangles:
		xs,ys=[],[]
		for i in 0,1,2:
			xs+=[t[i].x]
			ys+=[t[i].y]
		xs += [xs[0]]
		ys += [ys[0]]
		ax.plot(xs,ys)
	plt.show()


def plot_circles( circles ):
	print len(circles), 'circles'
	import numpy as np
	import matplotlib.pylab as plt
	fig,ax = plt.subplots(figsize=(8,8))
	xs,ys=[],[]
	depth=10
	# rational paramterization. only have to convert to floats for
	# the plotter.
	minx,miny=circles[0].center.x,circles[0].center.y
	maxx,maxy=minx,miny
	for c in circles:
		xs,ys=[],[]
		pdic={}
		cx,cy,cr=c.center.x,c.center.y,c.radius
		for m in range(0,depth):
			for n in range(0,depth):
				if (blueq(m,n)==0): continue
				x = cr*Fraction(redq(m,n),blueq(m,n))
				y = cr*Fraction(greenq(m,n),blueq(m,n))
				pdic[x]=y
		sortkeys = pdic.keys()
		sortkeys.sort()
		# top half
		for key in sortkeys:
			x,y=key,pdic[key]
			xs += [float(cx+x)]
			ys += [float(cy+y)]
		sortkeys.reverse()
		# bottom half
		for key in sortkeys:
			x,y=key,pdic[key]
			xs += [float(cx+x)]
			ys += [float(cy-y)]
		ax.plot(xs,ys)
		minx=min(min(xs),minx)
		miny=min(min(ys),miny)
		maxx=max(max(xs),maxx)
		maxy=max(max(ys),maxy)
	wx = maxx-minx
	hy = maxy-miny
	ax.set_xlim([minx-wx*0.05,maxx+wx*0.05])
	ax.set_ylim([miny-hy*0.05,maxy+hy*0.05])
	ax.set_aspect(1)
	print ax.__doc__
	plt.show()


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
