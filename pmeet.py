from fractions import Fraction

# polygon intersection.. doesnt work.


# assume - input polys are clockwise-ordered set of 3 or more points
# assume - points are using rational numbers for coordinates (Fractions)
# assume - polygons are simple

# design - dont use angles
# point = [x,y]
# line = [a,b,c] where ax+by+c = 0
# vector = [x,y]
# triangle = [point,point,point]
# polygon = [point,point,...]

# notes
# http://math.stackexchange.com/questions/74307/two-2d-vector-angle-clockwise-predicate
# http://stackoverflow.com/questions/243945/calculating-a-2d-vectors-cross-product
# https://www.youtube.com/watch?v=6XghF70fqkY&list=PL01A21B9E302D50C1

import sys

# -> determinant of 2x2 matrix of 2 2-d vectors
	# -> also cross product if you add a z=0 and return magnitude
# -> also area of paralellogram formed by v1, v2
# -> also is the 'multiple' by which all Grossman bi-vectors are related
def determinant( v1, v2 ):
	x1,y1,x2,y2 = v1[0],v1[1],v2[0],v2[1]
	return x1*y2-x2*y1

def vector( p0, p1 ):
	return [ p1[0] - p0[0], p1[1] - p0[1] ]

def line( p0, p1 ):
	v = vector( p0, p1 )
	a,b,c = v[1], v[0], crosshack( p0, p1 )
	return [a,b,c]

def meet( l0, l1 ):
	a,b,c=[l0[0],l1[0]], [l0[1],l1[1]], [l0[2],l1[2]]
	x = Fraction( crosshack(b,c), crosshack(a,b) )
	y = Fraction( crosshack(a,c), crosshack(b,a) ) 
	return x,y

def triangle_intersection( t1, t2 ):
	for p1 in t1:
		for p2 in t2:
			lines += line( p1, p2 )
			vectors += vector( p1, p2 )
	for line1 in lines:
		for line2 in lines:
			meets += meet( line1, line2 )
	for point in meets:
		ok = True
		for v in vectors:
			if not is_right_turn( v[0],v[1],point ): ok = False
		if ok: newpoints += [point]
	if not is_right_turn(newpoints[0],newpoints[1],newpoints[2]):
		newpoints = [newpoints[1],newpoints[0],newpoints[2]]
	return newpoints

def is_inside_triangle( tri, point ):
	p0,p1,p2 = tri[0],tri[1],tri[2]
	if not is_right_turn( p0, p1, point ): return False
	if not is_right_turn( p1, p2, point ): return False
	if not is_right_turn( p2, p0, point ): return False
	return True

def is_right_turn( p0, p1, p2 ):
	v1,v2=vector(p0,p1),vector(p1,p2)
	return crosshack( v1, v2 ) < 0

def triangle_inside_pgon( tri, pgon ):
	for point in pgon:
		if is_inside_triangle(tri,point) and not point in tri:
			return False
	return True

def find_ear( pgon ):
	n = len(pgon)
	for i in range( n ):
		p0,p1,p2 = pgon[i%n],pgon[(i+1)%n],pgon[(i+2)%n]
		print 'find ear test',p0,p1,p2
		if is_right_turn( p0, p1, p2 ):
			ok = True
			for point in pgon:
				#print 'subtest',point
				if is_inside_triangle( [p0,p1,p2], point ):
					ok=False
		else:
			print 'not right turn'
			ok=False
		if ok: return [p0,p1,p2]

def chop_ear( ear_tri, pgon ):
	newpgon = []
	for p in pgon:
		if p==ear_tri[1]: pass
		else: newpgon += [p]
	return newpgon

def tessellate( pgon, triangles ):
	print 'tess.  pgon: ' ,pgon, 'triangles:', triangles
	p0,p1,p2 = pgon[0],pgon[1],pgon[2]
	if len(pgon)>3:
		ear_tri = find_ear( pgon )
		print 'found ear',ear_tri
		newpgon = chop_ear( ear_tri, pgon )
		print 'choppd pgon: ',newpgon
		triangles += [ ear_tri ]
		return tessellate( newpgon, triangles )
	else:
		print 'at final triangle. recursion ending'
		return [[p0,p1,p2]] + triangles

def detessellate( triangles ):
	pgon = []
	for t1 in triangles:
		for t2 in triangles:
			if t1!=t2:
				print 'neq'
	return pgon

def pgon_intersection( pgon1, pgon2 ):
	global f
	triangles = []
	triangles1 = tessellate( pgon1, [] )
	#triangles2 = tessellate( pgon2, [] )
	sys.exit()
	print 'tessellated'
	print 'group1:', triangles1
	print 'group2:', triangles2
	for t1 in triangles1:
		for t2 in triangles2:
			triangles += triangle_intersection( t1, t2 )
	return detessellate( triangles )

def svg(pointlist):
	picsize,margin,maxcoord=400,20,float(max(max(pointlist)))
	def trans( coord ):
		return str( (coord / maxcoord) * (picsize * 0.90) + margin )
	s= '<svg xmlns="http://www.w3.org/2000/svg" width="%i" height="%i">\n' % ( picsize, picsize )
	s+= '<path d="M ' + trans( pointlist[0][0] ) + ' ' + trans( pointlist[0][1] )
	for p in pointlist: s+= 'L ' + trans( p[0] ) + ' ' + trans( p[1] )
	s+= ' Z " stroke="black" fill="none"/>\n </svg>\n'
	return s

pgon1=[[0,0],[0,4],[3,4],[5,10],[10,10],[3,0]]
pgon2=[[1,1],[0,5],[4,0]]
newpgon = pgon_intersection( pgon1, pgon2 )
print pgon1, '\n', pgon2, '\n', newpgon

