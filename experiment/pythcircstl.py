from piliko import *

# draw a rational paramterization of a circle,
# into an STL format for use in other programs.

# problem: STL is ASCII so we convert to float before output
# which may result in coincident points 

def stl_circle( cx, cy, cr ):
	depth=20
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

	triangles=[]
	for i in range(0,len(xs)+1):
		x1=xs[(i+0)%len(xs)]
		y1=ys[(i+0)%len(xs)]
		x2=xs[(i+1)%len(xs)]
		y2=ys[(i+1)%len(xs)]
		x3,y3=cx,cy
		t=triangle(x1,y1,0,x2,y2,0,x3,y3,0)
		triangles+=[t]

	stl='solid piliko_model'
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
	stl+='endsolid piliko_model'
	print stl
	
stl_circle( 0, 0, 1 )
