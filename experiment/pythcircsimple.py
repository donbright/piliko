from fractions import Fraction
import sys

# very simple rational paramterization / approximation of blue circle
# (x^2+y^2=1) useful as base for building other ideas

def sqr(x): return x*x
def greenq_pts(x,y,x2,y2): return 2*(x2-x)*(y2-y)
def redq_pts(x,y,x2,y2): return sqr(x2-x)-sqr(y2-y)
def blueq_pts(x,y,x2,y2): return sqr(x2-x)+sqr(y2-y)

def greenq(m,n): return greenq_pts(0,0,m,n)
def redq(m,n): return redq_pts(0,0,m,n)
def blueq(m,n): return blueq_pts(0,0,m,n)

xs,ys=[],[]
depth = 10
for m in range(-depth,depth):
	for n in range(-depth,depth):
		if blueq(m,n)==0: continue
		x = Fraction(redq(m,n),blueq(m,n))
		y = Fraction(greenq(m,n),blueq(m,n))
		xs += [x]
		ys += [y]

max=max(xs+ys)
i=0
print xs[i]*xs[i]+ys[i]*ys[i]
for i in range(0,len(xs)):
	xs[i] = Fraction( xs[i], max )
	ys[i] = Fraction( ys[i], max )

print len(xs), 'points'
import numpy as np
import matplotlib.pylab as plt
fig,ax = plt.subplots(figsize=(8,8))

ax.set_xlim([min(xs)-2,max(xs)+2])
ax.set_ylim([min(ys)-2,max(ys)+2])
for i in range(0,len(xs)):
	xs[i]=xs[i]#+zs[i]/4
	ys[i]=ys[i]#+zs[i]/4
ax.scatter(xs,ys)
plt.show()
