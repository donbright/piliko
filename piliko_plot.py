from piliko_bbox import *
from piliko_scuts import *
from piliko import *

##################### render objects into text

def bounding_box_txt( b ):
	s = '[ ' + str(b.min) + ' , ' + str(b.max) + ' ]'
	return s

def complex_txt( c ):
	s = '[ '+str(c.x)+' + '+str(c.y)+'*i ]'
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

def plane_txt( l ):
	s = '<'+str(l.a)+":"+str(l.b)+":"+str(l.c)+":"+str(l.d)
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

def sphere_txt( c ):
	s = str('['+str(c.center)+','+str(c.radial_quadrance)+'<->'+str(c.curvature_quadrance)+']')
	return s

def triangle_txt( tri ):
	#spreads = str(tri.s0)+','+str(tri.s1)+','+str(tri.s2)
	#line_eqns = str(tri.l0)+','+str(tri.l1)+','+str(tri.l2)
	#linesegs = str(tri.ls0)+' '+str(tri.ls1)+' '+str(tri.ls2)
	#points = str(tri.p0)+','+str(tri.p1)+','+str(tri.p2)
	#quadrances = str(tri.q0)+','+str(tri.q1)+','+str(tri.q2)
	#s ='\ntriangle: '
	#s+='\n line eqns: ' + line_eqns
	#s+='\n line segs: ' + linesegs
	#s+='\n points: ' + points
	#s+='\n blue quadrances: ' + quadrances
	#s+='\n blue spreads: ' + spreads
	s = '['+str(tri.p0)+','+str(tri.p1)+','+str(tri.p2)+']'
	return s

def spherical_triangle_txt( tri ):
	s = '['+str(tri.p1)+','+str(tri.p2)+','+str(tri.p3)+']'
	return s

############################## render objects into MatPlotLib graphics
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

def getax():
	global ax
	return ax

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
def plot_show(): plotshow()
	
def plot_triangles( *args ):
	if checktypes(list,*args):
		plot_triangles(*args[0])
		return
	if checktypes(tuple,*args):
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

def plot_line_seg( ls ):
	plotinit( ls[0] )
	xs = [ls[0].x,ls[1].x]
	ys = [ls[0].y,ls[1].y]
	ax_floatplot( xs, ys, ax.plot )
plot_lineseg=plot_line_seg

def plot_line_segs( segs ):
	for ls in segs: plot_line_seg( ls )

def plot_vector( v ):
	plot_line_seg( lineseg(0,0,v.x,v.y) )

def plot_vectors( vecs ):
	for v in vecs: plot_vector( v )

def plot_line( l ):
	if l.a==0 and l.b==0:
		plot_point(0,0)
		return
	plotinit(point(0,0))
	xaxis = line(0,1,0)
	yaxis = line(1,0,0)
	p1,p2 = meet(l,xaxis),meet(l,yaxis)
	if p1==None and p2!=None: p1 = p2 + point(p2.x+1,0)
	elif p2==None and p1!=None: p2 = p1 + point(0,p1.y+1)
	if p1==p2: p2=p1+vector(Fraction(l.b),Fraction(-l.a))
	if p1!=None and p2!=None:
		ls = line_seg( p1, p2 )
		v = vector(p2-p1)
		ls2 = translate( ls, v )
		v = vector(p1-p2)
		ls3 = translate( ls, v )
		plot_line_seg( ls )
		plot_line_seg( ls2 )
		plot_line_seg( ls3 )

def plot_lines( *args ):
	if checktypes( line, *args):
		for a in args: plot_line(a)
	elif checktypes(list,*args):
		if checktypes(line,*args[0]):
			plot_lines(*args[0])
		else: raise Exception('unknown type for plot lines')
	else: raise Exception('unknown type for plot lines')

def plot_points( *args ):
	#print args
	if checktypes(point,*args):
		plotinit( args[0] )
		print len( args ), 'points'
		xs,ys=[],[]
		for p in args:
			xs += [p.x]
			ys += [p.y]
		ax_floatplot(xs,ys,ax.scatter) # scatter plot
	elif checktypes(list,*args):
		if checktypes(point,args[0]):
			print len(args),'points'
			plot_points(*args[0])
		elif checktypes(list,args[0]):
			if checkrationals(args[0][0]) and len(args)==2:
				plotinit( point(args[0][0],args[1][0]) )
				ax_floatplot(args[0],args[1],ax.scatter) # scatter plot
			elif checktypes(point,args[0][0]):
				plot_points(*args[0])
			else: raise Exception('unknown type fed to plot_points')
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




#############################
### 3d
def triangles_to_stl(*args):
	if checktypes(list,*args):
		return triangles_to_stl(*args[0])
	triangles = list(args)
	#if checktypes(spherical_triangle,*args):
	#	for t in args: newargs+=[t]
	#	triangles_to_stl( newargs )
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

# shortcuts
# for bad spellers etc

def plot_circles(*args): plot_blue_circles(*args)




def drawtriangles(tris): plot_triangles(tris)
def drawtriangle(tri): plot_triangles([tri])
def draw_triangle(tri): plot_triangles([tri])
def plottriangles(tris): plot_triangles(tris)
def plottriangle(tri): plot_triangles([tri])
def plot_triangle(tri): plot_triangles([tri])

def plotpoints(points): plot_points(points)
def plotpoint(*args): plot_point(*args)
def plot_point(*args):
	if checkrationals(*args) and len(args)==2:
		ax_floatplot([args[0]],[args[1]],ax.scatter)
	else: plot_points(*args)
def drawpoints(points): plot_points(points)
def drawpoint(point): plot_points([point])
def draw_point(point): plot_points([point])

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


