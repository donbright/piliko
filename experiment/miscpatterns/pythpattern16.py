from fractions import Fraction as f
import sys
import math
# strange patterns by looking at pythagorean triples
#
# this is using the '1-t^2,1+t^2' paramterization of the circle
#

# but with attempting to make 'rings' instead of the circle itself

# using fractions as input to 't', we get a pretty smooth rational tessellation
# of the unit circle, where rational means that each point has rational
# coordinates.
#
# as with pythpattern12, this is not symmetrical. its easy to see this
# by looking at the 'crowding' near the middle (on the top-bottom axis)
#
# also, as with pythpattern 12, if you try to 'make' it symmetrical
# by inserting y,x for every x,y point, you get a sort of messy
# tessellation with lots of tiny bits... and its not really symmetrical
# either along every axis. 
#
#
# note - blue, red, and green quadrance are from Norman Wildberger's 
# Chromogeometry

def sqr(x): return x*x
def greenq(x,y,x2,y2): return 2*(x2-x)*(y2-y)
def redq(x,y,x2,y2): return sqr(x2-x)-sqr(y2-y)
def blueq(x,y,x2,y2): return sqr(x2-x)+sqr(y2-y)
xs,ys=[],[]
xs2,ys2=[],[]

depth=15
layers=[[]]
for j in range(0,depth):
	layer=layers[j]
	layers+=[[]]
	for i in range(2*j):
		num = i
		denom = 2*j
		layers[j] += [f(num,denom)]
	layers[j+1]+=[f(1,1)]

#for i in layers:
#	print i,'\n'

for layer in layers:
	for t in layer:
		if blueq(0,0,1,t)==0: continue
		x = len(layer)*f(redq(0,0,1,t),blueq(0,0,1,t))
		y = len(layer)*f(greenq(0,0,1,t),blueq(0,0,1,t))
		xs += [x]
		ys += [y]
		xs += [-x]
		ys += [y]
		xs += [-x]
		ys += [-y]
		xs += [x]
		ys += [-y]


xs=[]
ys=[]
for nn in range(1,15): # layers[0:4]:
	angle = 0
	for t in range(0,4*nn+1):
		#angle += 360/len(layer)
		angle = (float(t)/float(4*nn))*(math.pi)
		x = nn*math.cos(angle)
		y = nn*math.sin(angle)
		print t,nn,float(t)/float(nn),angle,angle/math.pi,x,y
		xs+=[x]
		ys+=[y]
		xs+=[x]
		ys+=[-y]

max=max(xs+ys)

for i in range(0,len(xs)):
	#xs[i] = f(xs[i], max )
	#ys[i] = f(ys[i], max )
	xs[i] = xs[i] / max
	ys[i] = ys[i] / max

#print len(xs), 'points'
import numpy as np
import matplotlib.pylab as plt
fig,ax = plt.subplots(figsize=(8,8))
ax.set_ylim([-1.2,1.2])
ax.set_xlim([-1.2,1.2])
ax.scatter(xs,ys)
plt.show()

for p in range(len(xs)):
	print xs[p],ys[p]
print len(xs), 'points'

