from piliko import *

import sys

# experiment

# draw a rational paramterization of a circle,
# render it into triangle faces.
#
#
# then output into an STL format for use in other programs.

# problem: STL is ASCII decimal, so we convert to float before output
# which reduces precision, possibly too much (2 points that are 
# separate with big-int rationals might become the same after conversion
# to float)


def pointcmp( a, b ):
	if a.z==b.z:
		if a.x==b.x:
			return cmp(a.y,b.y)
		return cmp(a.x,b.x)
	return cmp(a.z,b.z)

def triangles_to_stl(triangles):
	stl='solid piliko_model\n'
	for t in triangles:
		x0,y0,z0=str(float(t[0].x)),str(float(t[0].y)),str(float(t[0].z))
		x1,y1,z1=str(float(t[1].x)),str(float(t[1].y)),str(float(t[1].z))
		x2,y2,z2=str(float(t[2].x)),str(float(t[2].y)),str(float(t[2].z))
		stl+=' facet normal 0 0 1\n'
		stl+='  outer loop\n'
		stl+='   vertex '+x0+' '+y0+' '+z0+'\n'
		stl+='   vertex '+x1+' '+y1+' '+z1+'\n'
		stl+='   vertex '+x2+' '+y2+' '+z2+'\n'
		stl+='  endloop\n'
		stl+=' endfacet\n'
	stl+='endsolid piliko_model\n'
	return stl

def sphere_tessellation( cx, cy, cz, cr ):
	depth1,depth2=6,6
	triangles=[]
	points=[]
	q = cr*cr
        for m in range(0,depth1):
		s = spread_polynomial(m,Fraction(13*13,85*85))
		l = perfect_square_root( q * s )
		z = perfect_square_root( q * ( 1 - s ) )
		for n in range(0,depth2):
			s2 = spread_polynomial(n,Fraction(13*13,85*85))
			x = perfect_square_root( l*l * s2 )
			y = perfect_square_root( l*l * ( 1 - s2 ) )
			points += [point(x,y,z)]
			points += [point(y,x,z)]
			print n,n,':',bitcount(x,y,z),'bits',
			print (sqr(x)+sqr(y)+sqr(z)),'<xyz radius'
			x2 = perfect_square_root( z*z * s2 )
			y2 = perfect_square_root( z*z * ( 1 - s2 ) )
			points += [point(x2,y2,l)]
			points += [point(y2,x2,l)]
			print n,n,':',bitcount(x2,y2,l),'bits, 3 pts',
			print (sqr(x2)+sqr(y2)+sqr(l)),'xyz'

	print 'sort'
	points.sort( pointcmp )
	print 'ok'
	points2=[]
	for p in points:
		if not p in points2:
			points2 += [p]
	zlayersd={}
	for p in points2:
		if zlayersd.has_key(p.z): zlayersd[p.z] += [p]
		else: zlayersd[p.z] = [p]
	zlist = sorted(zlayersd.keys())
	zlayers = []
	for z in zlist:
		zlayer = []
		for p in zlayersd[z]:
			zlayer += [p]
		zlayers += [zlayer]
	for j in range(0,len(zlayers)-1):
		layerpts = zlayers[j]
		layerz = layerpts[0].z
		nextlayerpts = zlayers[j+1]
		nextlayerz = nextlayerpts[0].z
		layerpts.sort( pointcmp )
		for i in range(len(layerpts)-1):
			p1 = layerpts[(i+0)%len(layerpts)]
			p2 = layerpts[(i+1)%len(layerpts)]
			p3 = nextlayerpts[(i+0)%len(nextlayerpts)]
			p4 = nextlayerpts[(i+1)%len(nextlayerpts)]
			triangles+=[triangle(p2,p1,p3)]
			if p3!=p4: triangles+=[triangle(p3,p4,p2)]
			#print p1,p2,p3,p4
		print ',',
		sys.stdout.flush()
	#for t in triangles:
	#	print t
	triangles2 = []
	for t in triangles:
		print ';',
		sys.stdout.flush()
		triangles2 += [reverse_orientation(mirrorx( t ))]
		triangles2 += [reverse_orientation(mirrory( t ))]
		triangles2 += [mirrorx(mirrory( t ))]
		triangles2 += [mirrorz(mirrorx( t ))]
		triangles2 += [mirrorz(mirrory( t ))]
		triangles2 += [mirrorz(reverse_orientation(mirrorx(mirrory( t ))))]
		triangles2 += [mirrorz(reverse_orientation(t))]
	triangles += triangles2
	return triangles

triangles = sphere_tessellation( 0, 0, 0, 1 )
stl = triangles_to_stl( triangles )
open('sphere2.stl','w').write(stl)
print 'wrote to sphere2.stl'
