from fractions import Fraction as f
import sys

# strange patterns by looking at pythagorean triples
#
# in this example the rational paramterization of the circle
# is superimposed upon the 'raw' pythagorean triples
#
# it forms a sort of weird non-symmetrical rational tesellation of the circle
# (in that all the points have rational coordinates)
#
# note the parastiches (apparent spirals) coming from the center
# (or are they apparent parabolas?)
#


# this example 'symmetrifies' pythpattern 8 by copying x,y to y,x
# and upping the number of points.

# note - blue, red, and green quadrance are from Norman Wildberger's 
# Chromogeometry

def sqr(x): return x*x
def greenq(x,y,x2,y2): return 2*(x2-x)*(y2-y)
def redq(x,y,x2,y2): return sqr(x2-x)-sqr(y2-y)
def blueq(x,y,x2,y2): return sqr(x2-x)+sqr(y2-y)
xs,ys=[],[]
xs2,ys2=[],[]
r=24
for m in range(-r,r):
	for n in range(-r,r):
		if blueq(0,0,m,n)==0: continue
		x = f(redq(0,0,m,n),1)
		y = f(greenq(0,0,m,n),1)
		x2 = f(redq(0,0,m,n),blueq(0,0,m,n))
		y2 = f(greenq(0,0,m,n),blueq(0,0,m,n))
		xs += [x]
		ys += [y]
		xs += [y]
		ys += [x]
		xs2 += [x2]
		ys2 += [y2]

max=max(xs+ys)

for i in range(0,len(xs)):
	xs[i] = 2*f(xs[i], max )
	ys[i] = 2*f(ys[i], max )


print len(xs), 'points'
import numpy as np
import matplotlib.pylab as plt
fig,ax = plt.subplots(figsize=(8,8))

ax.set_ylim([-1.2,1.2])
ax.set_xlim([-1.2,1.2])
for i in range(0,len(xs)):
	xs[i]=xs[i]#+zs[i]/4
	ys[i]=ys[i]#+zs[i]/4
ax.scatter(xs+xs2,ys+ys2)
plt.show()
