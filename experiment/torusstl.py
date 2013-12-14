from piliko import *

import sys

# experiment

# draw a rational paramterization of a torus
# render it into triangle faces.
#
#
# then output into an STL format for use in other programs.

# problem: STL is ASCII decimal, so we convert to float before output
# which reduces precision, possibly too much (2 points that are 
# separate with big-int rationals might become the same after conversion
# to float)

# note
# code is highly inefficient and repeats triangles. lulz


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

def points_to_triangles( points ):
	triangles=[]
	points.sort( pointcmp )
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
			triangles+=[triangle(p1,p2,p3)]
			if p3!=p4: triangles+=[triangle(p4,p3,p2)]
			print p1,p2
		print ','
	return triangles

def torus_tessellation( cx, cy, cz, cr ):
	depth=5
	small_radius = 1
	big_radius = 2
	triangles=[]
	points=[]
	pointsinner=[]
	pointsouter=[]
        for m in range(0,depth):
		for n in range(0,depth):
		        for m1 in range(0,depth):
	       			for n1 in range(0,depth):
       		                 	if m+n==0: continue
       		                 	if m1+n1==0: continue
                                	bq,rq,gq = blueq(m,n),redq(m,n),greenq(m,n)
	                                bq1,rq1,gq1 = blueq(m1,n1),redq(m1,n1),greenq(m1,n1)
        	                        z = small_radius * Fraction( rq1, bq1 )
                	                l = small_radius * Fraction( gq1, bq1 )
                        	        x = (big_radius-l) * Fraction( rq, bq )
	                                y = (big_radius-l) * Fraction( gq, bq )
	                        	#print 'x,y,x^2+y^2',x,y,x*x+y*y
					pointsinner += [point(x,y,z)]
                        	        x2 = (big_radius+l) * Fraction( rq, bq )
	                                y2 = (big_radius+l) * Fraction( gq, bq )
					pointsouter += [point(x2,y2,z)]
	triangles  = points_to_triangles( pointsinner )
	triangles += reverse_orientation(points_to_triangles( pointsouter ))
	#for t in triangles:
	#	print t
	triangles2 = []
	for t in triangles:
		triangles2 += [reverse_orientation(mirrory( t ))]
	#	triangles2 += [reverse_orientation(mirrorz( t ))]
	triangles += triangles2
	return triangles

triangles = torus_tessellation( 0, 0, 0, 1 )
stl = triangles_to_stl( triangles )
open('torus.stl','w').write(stl)
print 'wrote to torus.stl'
