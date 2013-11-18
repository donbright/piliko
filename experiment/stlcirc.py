from fractions import Fraction
import sys
import numpy as np
import matplotlib.pylab as plt

# very simple rational paramterization / approximation of blue circle
# (x^2+y^2=1) useful as base for building other ideas

def sqr(x): return x*x
def greenq_pts(x,y,x2,y2): return 2*(x2-x)*(y2-y)
def redq_pts(x,y,x2,y2): return sqr(x2-x)-sqr(y2-y)
def blueq_pts(x,y,x2,y2): return sqr(x2-x)+sqr(y2-y)

def greenq(m,n): return greenq_pts(0,0,m,n)
def redq(m,n): return redq_pts(0,0,m,n)
def blueq(m,n): return blueq_pts(0,0,m,n)

for depth in range(2,10):
	xs,ys=[],[]
	for m in range(0,depth):
		for n in range(0,depth):
			if blueq(m,n)==0: continue
			x = Fraction(redq(m,n),blueq(m,n))
			y = Fraction(greenq(m,n),blueq(m,n))
			xs += [x]
			ys += [y]

	print len(xs), 'points'
	maxn=max(xs+ys)
	i=0
	print xs[i]*xs[i]+ys[i]*ys[i]
	for i in range(0,len(xs)):
		xs[i] = Fraction( xs[i], maxn )
		ys[i] = Fraction( ys[i], maxn )
	fig,ax = plt.subplots(figsize=(7,7))	

	ax.set_ylim([-1.2,1.2])
	ax.set_xlim([-1.2,1.2])
	ax.scatter(xs,ys)
	plt.show()
