from fractions import Fraction as Fract
import sys

# rational paramterization / approximation of bernoulli's lemniscate
# traditional form: ( x^2 + y^2 ) ^2 = 2*( x^2 - y^2 )
# chromogeometry form:
# x = (blueq/redq)  / blueq( blueq/redq, greenq/redq )
# y = (greenq/redq) / blueq( blueq/redq, greenq/redq )
# where q = quadrance between 0,0 and integer point m,n 
# please see pythbernlem.py for full explanation

def sqr(x): return x*x
def greenq(x,y,x2,y2): return 2*(x2-x)*(y2-y)
def redq(x,y,x2,y2): return sqr(x2-x)-sqr(y2-y)
def blueq(x,y,x2,y2): return sqr(x2-x)+sqr(y2-y)
xs,ys=[],[]
depth = 20
for m in range(-depth,depth):
	for n in range(-depth,depth):
		if redq(0,0,m,n)==0: continue
		if greenq(0,0,m,n)==0: continue
		bq,rq,gq = blueq(0,0,m,n),redq(0,0,m,n),greenq(0,0,m,n)
		x = Fract( Fract(bq,gq), blueq(0,0,Fract(rq,gq),Fract(bq,gq)) )
		y = Fract( Fract(rq,gq), blueq(0,0,Fract(bq,gq),Fract(rq,gq)) )
		xs += [x]
		ys += [y]
		# note ... just by switching a single rq and bq, we 'flip' 
		# the entire shape across the x=y line, or rotate by spread=1
		x = Fract( Fract(rq,gq), blueq(0,0,Fract(rq,gq),Fract(bq,gq)) )
		y = Fract( Fract(bq,gq), blueq(0,0,Fract(bq,gq),Fract(rq,gq)) )
		xs += [x]
		ys += [y]
		# another note--- this leminscate is quite similar to the 
		# one with rq on the bottom instead of gq

max=max(xs+ys)
for i in range(0,2):
	print xs[i],',',ys[i],
print '....'
for i in range(0,len(xs)):
	xs[i] = Fract( xs[i], max )
	ys[i] = Fract( ys[i], max )

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
