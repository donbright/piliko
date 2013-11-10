from fractions import Fraction as f
import sys

# strange patterns by looking at pythagorean triples
#
# this is an attempt to have different 'rings' of the circle
# instead of just a flat circle

# it provides a non-symmetrical but totally rational 'tessellation' of 
# some rational points on a circle ... in that all the points of the 
# tessellation, as well as the points on the circle, have rational x,y 
# coordinates.

# note - blue, red, and green quadrance are from Norman Wildberger's 
# Chromogeometry

def sqr(x): return x*x
def greenq(x,y,x2,y2): return 2*(x2-x)*(y2-y)
def redq(x,y,x2,y2): return sqr(x2-x)-sqr(y2-y)
def blueq(x,y,x2,y2): return sqr(x2-x)+sqr(y2-y)
xs,ys=[],[]
xs2,ys2=[],[]
r=24
rq=sqr(r)
for m in range(0,r):
	for n in range(0,r):
		if blueq(0,0,m,n)==0: continue
		x = m*f(redq(0,0,m,n),blueq(0,0,m,n))
		y = m*f(greenq(0,0,m,n),blueq(0,0,m,n))
		if (x<0): continue
		xs += [x]
		ys += [y]
		xs += [-x]
		ys += [y]
		xs += [x]
		ys += [-y]
		xs += [-x]
		ys += [-y]

max=max(xs+ys)

for i in range(0,len(xs)):
	xs[i] = f(xs[i], max )
	ys[i] = f(ys[i], max )

print len(xs), 'points'
import numpy as np
import matplotlib.pylab as plt
fig,ax = plt.subplots(figsize=(8,8))
ax.set_ylim([-1.2,1.2])
ax.set_xlim([-1.2,1.2])
ax.scatter(xs,ys)
plt.show()
