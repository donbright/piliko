from fractions import Fraction
import sys

# rational paramterization / approximation of bernoulli's lemniscate
# in a 3 dimensional 'dumbbell' arrangement.

# (note - this uses terms from Norman Wildberger's rational 
# trigonometry/chromogeometry. briefly for a vector from 0,0 to x,y:
#
# blue quadrance (x,y) = x^2 + y^2
# red quadrance (x,y) = x^2 - y^2
# green quadrance (x,y) = 2*x*y
# )

# theory:
#
# step one is the rational paramterization of bernoulli's lemniscate
# we found this in pythbern.py
#
# step two is to 'grow' it into three d as some kind of dumbbell shape.
#
# how..? hrm.
# 
# consider each 'x' as a 'distance' from origin for generating a circle.
# consider 'y' as the radius of the circle.
# now, draw the circle--- using rational points
# we will end up with a 'stack' of circles in the dumbbell shape
# as though we had sliced the dumbbell.

# imagine 
def sqr(x): return x*x
def greenq_pts(x,y,x2,y2): return 2*(x2-x)*(y2-y)
def redq_pts(x,y,x2,y2): return sqr(x2-x)-sqr(y2-y)
def blueq_pts(x,y,x2,y2): return sqr(x2-x)+sqr(y2-y)

def greenq(m,n): return greenq_pts(0,0,m,n)
def redq(m,n): return redq_pts(0,0,m,n)
def blueq(m,n): return blueq_pts(0,0,m,n)

xs,ys,zs=[],[],[]
depth = 10
for m in range(-depth,depth):
	for n in range(0,depth):
		if redq(m,n)==0: continue
		x = Fraction(blueq(m,n),redq(m,n))
		y = Fraction(greenq(m,n),redq(m,n))
		oh = blueq(x,y)
		lambd = Fraction( 1, oh )
		x = x * lambd
		y = y * lambd
		distance = x
		radius = y
		circpts = int(radius*20)
		for m2 in range(-circpts,circpts):
			for n2 in range(-circpts,circpts):
				if blueq(m2,n2)==0: continue
				xdumb = distance
				ydumb = Fraction(redq(m2,n2),blueq(m2,n2))
				zdumb = Fraction(greenq(m2,n2),blueq(m2,n2))
				ydumb *= radius
				zdumb *= radius
				xs += [xdumb]
				ys += [ydumb]
				zs += [zdumb]
				
max=max(xs+ys+zs)
for i in range(0,2):
	print str(xs[i])+','+str(ys[i])+','+str(zs[i]),
print '....'
for i in range(0,len(xs)):
	xs[i] = Fraction( xs[i], max )
	ys[i] = Fraction( ys[i], max )
	zs[i] = Fraction( zs[i], max )

print len(xs), 'points'
import numpy as np
import matplotlib.pylab as plt
fig,ax = plt.subplots(figsize=(8,8))

ax.set_ylim([-1.2,1.2])
ax.set_xlim([-1.2,1.2])
for i in range(0,len(xs)):
	xs[i]=xs[i]+zs[i]/4
	ys[i]=ys[i]+zs[i]/4
ax.scatter(xs,ys)
plt.show()
