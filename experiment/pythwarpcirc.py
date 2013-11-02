from fractions import Fraction
import sys

# rational approximation of unit circle... with 'warping'
# introduced by playing around with inputs to the quadrance functions

# for example, instead of 0,0,m,n use '-n,0,m,n'

def sqr(x): return x*x
def greenq(x,y,x2,y2): return 2*(x2-x)*(y2-y)
def redq(x,y,x2,y2): return sqr(x2-x)-sqr(y2-y)
def blueq(x,y,x2,y2): return sqr(x2-x)+sqr(y2-y)
xs,ys=[],[]
depth = 5
for m in range(-depth,depth):
	for n in range(-depth,depth):
		if blueq(0,0,m,n)==0: continue
		x = Fraction(redq(0,0,m,n),blueq(-n,0,m,n))
		y = Fraction(greenq(0,0,m,n),blueq(0,0,m,n))
		xs += [x]
		ys += [y]

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
