from fractions import Fraction
import sys

# strange patterns by looking at pythagorean triples

def sqr(x): return x*x
def greenq(x,y,x2,y2): return 2*(x2-x)*(y2-y)
def redq(x,y,x2,y2): return sqr(x2-x)-sqr(y2-y)
def blueq(x,y,x2,y2): return sqr(x2-x)+sqr(y2-y)
blueqlimit=1000000
xs,ys=[],[]
for m in range(-40,40):
	for n in range(-40,40):
		x = redq(0,0,m,n)
		y = greenq(0,0,m,n)
		if blueq(0,0,x,y)<blueqlimit:
			xs += [x]
			ys += [y]
			xs += [y]
			ys += [x]

max=max(xs+ys)

for i in range(0,len(xs)):
	xs[i] = Fraction( xs[i], max )
	ys[i] = Fraction( ys[i], max )

print len(xs), 'points'
import numpy as np
import matplotlib.pylab as plt
fig,ax = plt.subplots(figsize=(8,8))

ax.set_ylim([-1.2,1.2])
ax.set_xlim([-1.2,1.2])
for i in range(0,len(xs)):
	xs[i]=xs[i]#+zs[i]/4
	ys[i]=ys[i]#+zs[i]/4
ax.scatter(xs,ys)
plt.show()
