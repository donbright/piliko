from __future__ import division
from sympy import *
import sys
init_printing()
# given 3 points on a Quadratic Spline, a,b,c, and weight l
# find Implicit conic equation Ax^2+Bxy+Cy^2+Dx+Ey+F = 0
# note when l = 1, conic = parabola.
# https://dl.dropboxusercontent.com/u/78279253/splines.pdf
# paper "Conic Splines, By Rob Johnson, Apple Inc 1991"
def find_conic( ax, ay, bx, by, cx, cy, l ):
	u = Matrix( [by-cy,cx-bx,bx*cy-cx*by] )
	v = Matrix( [cy-ay,ax-cx,cx*ay-ax*cy] )
	w = Matrix( [ay-by,bx-ax,ax*by-bx*ay] )
	ut = u.transpose()
	vt = v.transpose()
	wt = w.transpose()
	QL=2*l**2*(u*wt+w*ut)
	QR=-v*vt
	Q = QL+QR
	IA = Q[0,0]
	IB = Q[1,0]+Q[0,1]
	IC = Q[1,1]
	ID = Q[2,0]+Q[0,2]
	IE = Q[2,1]+Q[1,2]
	IF = Q[2,2]
	ix,iy = symbols("x y")
	implicit_form = simplify(IA*ix**2+IB*ix*iy+IC*iy**2+ID*ix+IE*iy+IF)
	# debug
	#pprint( QL )
	#pprint( QR )
	#print
	#pprint( simplify(Q) )
	# isolate y^2 term in implicit equation
	#pprint( QL[1,1] )
	#pprint( QR[1,1] )
	#print
	#pprint( simplify(Q[1,1]) )
	return implicit_form

def self_test():
	ax,ay,bx,by,cx,cy,l = 1,1,2,3,4,5,Rational(1,2)
	coniceq = find_conic( ax,ay,bx,by,cx,cy,l )
	x,y = symbols("x y")
	expected = -12*x**2 + 18*x*y + 10*x - 7*y**2 - 6*y - 3
	print 'test OK:',repr(coniceq)==repr(expected)
	pprint( repr(coniceq) )

def misc():
	# miscellaneous interesting stuff
	ax,ay,bx,by,cx,cy,l = symbols("ax ay bx by cx cy l")
	dx,dy,ex,ey,fx,fy,l = symbols("dx dy ex ey fx fy l")
	l=1
	h,v = symbols("h,v")
	ax,ay,cx,cy=bx-h,by+v,bx+h,by+v
	implicit_form = find_conic( ax,ay,bx,by,cx,cy,l )
	pprint( implicit_form )
	dx,dy,ex,ey,fx,fy=cx,cy,cx+v,cy-h,cx+v+v,cy
	implicit_form = find_conic( dx,dy,ex,ey,fx,fy,l )
	pprint( implicit_form )


ax,ay,bx,by,cx,cy,l = -1,1,0,0,1,1,Rational(2)
pprint(find_conic( ax,ay,bx,by,cx,cy,l ))
