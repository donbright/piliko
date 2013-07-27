# very, very basic implementation of some Rational Geometry formulas
# in two dimensions.

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
#   enable omega triangle
# put 'of' in func names

# what is omega inverse?


# code design philosophia 
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

def checktypes( typename, *args ): # are all args of a given type? 
	for i in range(len(args)):
		if not isinstance(args[i],typename): return False
	return True

def checkrationals( *args ):
	for i in range(0,len(args)):
		if (type(args[i]) is float): #fixme - is not Fraction/int
			raise Exception("Rationals only please")
class point:
	def __init__(self, *args):
		checkrationals( args )
		self.x,self.y=args[0],args[1]
		if (len(args)==3): self.z=args[2]
	def __str__( self ):
		return point_txt(self)

class vector:
	def __init__( self, *args ):
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

class lineseg:
	def __init__(self,p0,p1):
		self.p0,self.p1=p0,p1
	def __str__( self ):
		return lineseg_txt( self )
	def quadrance( self ):
		return quadrance( self.p0, self.p1 )

class triangle:
	l0,l1,l2=line(0,0,0),line(0,0,0),line(0,0,0)
	p0,p1,p2=None,None,None
	ls0,ls1,ls2=None,None,None
	q0,q1,q2=None,None,None
	s0,s1,s2=[None]*3
	def __init__( self, l0, l1, l2 ):
		self.init_from_lines( l0, l1, l2 )

	def init_from_lines( self, l0, l1, l2 ):
		p0,p1,p2 = meet(l1,l2),meet(l0,l2),meet(l0,l1)
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


def red_quadrance_pts( p1, p2 ):
	if hasattr(p2,'z') and hasattr(p1,'z'):
		raise Exception(" 3d red quadrance not implemented ")
	return sqr( p2.x-p1.x ) - sqr( p2.y-p1.y )

def green_quadrance_pts( p1, p2 ):
	if hasattr(p2,'z') and hasattr(p1,'z'):
		raise Exception(" 3d green quadrance not implemented ")
	return 2*( p2.x-p1.x ) * ( p2.y-p1.y )

def blue_quadrance_pts( p1, p2 ):
	q = sqr( p2.x-p1.x ) + sqr( p2.y-p1.y )
	if hasattr(p2,'z') and hasattr(p1,'z'): q += sqr( p2.z-p1.z )
	return q

def red_quadrance_lineseg( ls ):
	return red_quadrance_pts( ls.p0, ls.p1 )
def green_quadrance_lineseg( ls ):
	return green_quadrance_pts( ls.p0, ls.p1 )
def blue_quadrance_lineseg( ls ):
	return blue_quadrance_pts( ls.p0, ls.p1 )

def quadrance_vector( v, color='blue' ):
	p0 = point( 0,0 )
	p1 = point( v.x, v.y )
	if hasattr(v,'z'):
		p0.z = 0
		p1.z = v.z
	if color=='red':
		return red_quadrance_pts( p0, p1 )
	elif color=='green':
		return green_quadrance_pts( p0, p1 )
	elif color=='blue':
		return blue_quadrance_pts( p0, p1 )

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
		quadrance_pts = blue_quadrance_pts
		quadrance_lineseg = blue_quadrance_lineseg
		quadrance_vector = blue_quadrance_vector
	elif color == 'green':
		quadrance_pts = green_quadrance_pts
		quadrance_lineseg = green_quadrance_lineseg
		quadrance_vector = green_quadrance_vector
	elif color == 'red':
		quadrance_pts = red_quadrance_pts
		quadrance_lineseg = red_quadrance_lineseg
		quadrance_vector = red_quadrance_vector

	if isinstance(args[0],point) and isinstance(args[1],point):
		return quadrance_pts( args[0],args[1] )
	if isinstance(args[0],lineseg):
		return quadrance_lineseg( args[0] )
	if isinstance(args[0],vector):
		return quadrance_vector( args[0] )
	return None



def quadria( *args ):
	if checktypes(point,*args):
		Q1=quadrance(args[0],args[1])
		Q2=quadrance(args[1],args[2])
		Q3=quadrance(args[2],args[0])
		return sqr(Q1+Q2+Q3)-2*(Q1*Q1+Q2*Q2+Q3*Q3)
	raise Exception('not implemented')

def blue_quadrance_quaternion( q ):
	# checktype( quaternion, q )
	t,x,y,z=q.t,q.x,q.y,q.z
	return t*t+x*x+y*y+z*z

def quadrance_quaternion( q ):
	return blue_quadrance_quaternion( q )

############### spreads



# fixme - if a1^2 - bq^2 = 0 then l1 = null line
# both must be non null
def red_spread_lines( l1, l2 ):
	a1,b1,c1 = l1.a, l1.b, l1.c
	a2,b2,c2 = l2.a, l2.b, l2.c
	numerator = -1 * sqr(a1*b2-a2*b1)
	denominator = (a1*a1-b1*b1)*(a2*a2-b2*b2)
	return Fraction( numerator, denominator )

def green_spread_lines( l1, l2 ):
	a1,b1,c1 = l1.a, l1.b, l1.c
	a2,b2,c2 = l2.a, l2.b, l2.c
	numerator = -1 * sqr(a1*b2-a2*b1)
	denominator = 4 * a1 * a2 * b1 * b2
	return Fraction( numerator, denominator )
	
def blue_spread_lines( l1, l2 ):
	a1,b1,c1 = l1.a, l1.b, l1.c
	a2,b2,c2 = l2.a, l2.b, l2.c
	numerator = sqr(a1*b2-a2*b1)
	denominator = (a1*a1+b1*b1)*(a2*a2+b2*b2)
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




#################### meet

# fixme - what if dont meet? what if same line?
# what if a,b,c all 0?
def meet_lines( l1, l2 ):
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



############################## misc stuff


def collinear( *args ):
	for i in range(len(args)):
		if not isinstance(args[i],point):
			raise Exception('coolinear() requires points')
	if len(args)<3: raise Exception('collinear() needs 3 pts or more')
	l = line(args[0],args[1])
	for i in range(2,len(args)):
		tmp_point = args[i]
		if meet( l, tmp_point ) == None: return False 
	return True

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
	return squared_cross_ratio_points( p0, p1, p2, p3 ) == 1

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

def is_pythagorean_triple_permutation( a, b, c )
	if a*a+c*c == b*b return True
	if c*c+b*b == a*a return True
	if a*a+b*b == c*c return True
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


def red_orthocenter( tri ):
	raise Exception(" not implemented ")
def green_orthocenter( tri ):
	raise Exception(" not implemented ")
def blue_orthocenter( tri ):
	raise Exception(" not implemented ")


def red_centroid( tri ):
	raise Exception(" not implemented ")
def green_centroid( tri ):
	raise Exception(" not implemented ")
def blue_centroid( tri ):
	raise Exception(" not implemented ")


def red_circumcenter( tri ):
	raise Exception(" not implemented ")
def green_circumcenter( tri ):
	raise Exception(" not implemented ")
def blue_circumcenter( tri ):
	raise Exception(" not implemented ")


def omega_triangle( tri ):
	o0 = red_orthocenter( tri )
	o1 = green_orthocenter( tri )
	o2 = blue_orthocenter( tri )
	return triangle( o0, o1, o2 )







##################### render objects into text

def point_txt( p ):
	s = '['+str(p.x)+','+str(p.y)
	if hasattr(p,'z'): s += ',' + str(p.z)
	s += ']'
	return s

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

def triangle_txt( tri ):
	spreads = 'spreads:'+str(tri.s0)+','+str(tri.s1)+','+str(tri.s2)
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



