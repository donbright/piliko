#
# Build a Geodesic sphere based on the Icosahedron
#
# Basic Algorithm:
#
# Start with an Icosahedron, one of the Platonic solids, and one of the very
# few tessellations of the sphere that is made of Regular polygons. 
#
# Now, divide each face of the Icosahedron into tiny triangles. Now,
# 'blow up' the icosahedron into a sphere, so that those tiny triangles
# now cover the surface of the sphere. The result is a 'geodesic' spherical
# polyhedron, a la Buckminster Fuller, that has somewhat similarly shaped
# triangles all over its surface.
#
# output is to STL format which can be read by many 3d programs

# References
# Weisstein, Eric W. "Geodesic Dome." From MathWorld--A Wolfram Web Resource. 
# http://mathworld.wolfram.com/GeodesicDome.html 
# Geodesic Domes, Tom Davis, http://www.geometer.org/mathcircles
# Antiprism project, Adrian Rossiter, antiprism.com, see uniform.cc
# Divine Proportions, Norman J Wildberger, 2010

from piliko import *

# splitn( triangle, n )
#
# split triangle into subtriangles, where n = number of splits to occur 
# on the edge of the triangle. return the list of new triangles. for 
# example n=2 creates 4 new triangles, n=3 creates 9, n=4 creates 
# ..uhm.. 16.. wow.. i think theres a pattern. triangles = n squared.
#
# it works by basically the same method one would use if creating 
# triangles in every 1x1 cell of a square grid that we have sliced along 
# one big diagonal. but instead of working on 1x1 square cells as the 
# basic cell, we use a vector1 x vector2 paralellogram as the 'basic 
# cell'. each vector is -1/nth of one of the sides of the triangle, 
# chosen to make the pattern work out.
#
# consider a triangle w 3 points, 0,0 2,0 0,2, in that order. (counterclockwise)
# lets do an 'n=2' split.
#
#  tp3
#   |\ 
#   | \
#   |  \  
#   |   \
#   |____\
#   |\    |\ 
#   | \   | \
#   |  \  |  \  
#   |   \ |   \
#   |____\|____\
#  tp1         tp2
#
#  ^ 
#  |                   first triangle = tp1, tp1+v1+v2, tp1+v1
#  | vector1                            (0,0) (1,0) (0,1)
#  |
#  |
#
#    \   vector 2 
#     \
#      \
#       \
#       _\|
#
# orientation of the input triangle is preserved in the output triangles
def splitn(tri,n):
	tris = []
	tp1,tp2,tp3 = tri[0],tri[1],tri[2]
	#print tp1,tp2,tp3	
	v1 = -vector(tp1-tp3)/n
	v2 = -vector(tp3-tp2)/n
	#print v1, v2
	for idx in range(0,n+1):
		for jdx in range(0,idx):
			i,j = idx-1,jdx
			p1 = tp1 + i*v1 + j*v2
			p2 = p1 + v1
			p3 = p1 + v1 + v2
			p4 = p1 + v2
			nt1 = triangle(p1,p3,p2)
			nt2 = triangle(p1,p4,p3)
			#print 'i,j',i,j
			#print 'ps,nts',p1,p2,p3,p4,nt1,
			tris += [nt1]
			if (j<i):
				#print nt2
				tris += [nt2]
			else: 
				pass
				#print
	return tris

def sqr(x): return x*x
def blueq( p1, p2 ):
	return sqr(p1.x-p2.x)+sqr(p1.y-p2.y)+sqr(p1.z-p2.z)
# project a point x onto the sphere with quadrance sq
def projpt( p, sq ):
	pq = blueq( point(0,0,0),p )
	ratio = babylonian_square_root(Fraction( sq,pq ),maxbits=512)
	p.x *= ratio
	p.y *= ratio
	p.z *= ratio
	return p

def project( tris, sq ):
	sphtris = []
	for t in tris:
		p1,p2,p3 = t[0],t[1],t[2]
		#np1,np2,np3 = t[0],t[1],t[2]
		np1,np2,np3 = projpt(p1,sq),projpt(p2,sq),projpt(p3,sq)
		sphtris += [triangle(np1,np2,np3)]
	return sphtris

def rotl(p): return point(p.y,p.z,p.x)
pts = {}
tris = []
sphtris = []
pts[0] = point(0,1,Fraction(161803,100000))
pts[1] = pts[0]*vector(1,1,-1)
pts[2] = pts[0]*vector(1,-1,1)
pts[3] = pts[0]*vector(1,-1,-1)
pts[4],pts[5],pts[6],pts[7] = rotl(pts[0]),rotl(pts[1]),rotl(pts[2]),rotl(pts[3])
pts[8],pts[10],pts[9],pts[11] = rotl(pts[4]),rotl(pts[5]),rotl(pts[6]),rotl(pts[7])
faces=[[1,3,11],[2,0,10],[2,5,8],[3,7,11],[4,1,6],[5,2,7],[5,3,9],
 [6,0,4],[7,2,10],[7,3,5],[8,0,2],[8,4,0],[8,5,9],[9,1,4],[9,3,1],
 [9,4,8],[10,0,6],[10,6,11],[11,6,1],[11,7,10]]
sphere_quadrance = blueq(point(0,0,0),pts[0])
#print float(sphere_quadrance)
for f in faces:
	#print f,pts[f[0]],pts[f[1]],pts[f[2]]
	tri = triangle(pts[f[0]],pts[f[1]],pts[f[2]])
	newtris = splitn( tri, 13 ) 
	sphtris = project( newtris, sphere_quadrance )
	tris += sphtris 
#tris = splitn(tri,4)
stl = triangles_to_stl( tris )
print stl
#plot_triangles( tris )
#plot_show()

