from fractions import Fraction as f
import sys

# rational paramterization of a 'green' hyperbola, using Norman 
# Wildberger's Chromogeometry.

# for a full explanation see the file 'pythhyp1.py'. 

# this file, pythhyp2, differs only in that we generate the 'green' 
# hyperbola ( based on the equation 2xy = r^2 = constant ) instead of 
# the 'red' one.

# a very simple rational paramterization would be something like y=2/x. 
# and then x is something like 0, 1/3, 2/3, 3/3, 4/3, 5/3, . . . 

# but it seems kind of cool that we can also do it with chromogeometry
# and get a pretty good looking 'green disc' tessellation:
#
# 
# namely, x = green quadrance(0,0,1,t)/red quadrance(0,0,1,t)
#         y = red quadrance(0,0,1,t)/green quadrance(0,0,1,t)
#
# where t is between 0 and 1

def sqr(x): return x*x
def greenq(x,y,x2,y2): return 2*(x2-x)*(y2-y)
def redq(x,y,x2,y2): return sqr(x2-x)-sqr(y2-y)
def blueq(x,y,x2,y2): return sqr(x2-x)+sqr(y2-y)
xs,ys=[],[]
xs2,ys2=[],[]

depth=30
layers=[[]]
for j in range(0,depth):
	layer=layers[j]
	layers+=[[]]
	for i in range(j):
		num = i
		denom = j
		layers[j] += [f(num,denom)]
#	layers[j+1]+=[f(1,1)]

for i in layers:
	print i,'\n'

for layer in layers:
	for t in layer:
		if greenq(0,0,1,t)==0: continue
		if redq(0,0,1,t)==0: continue
		x = len(layer)*f(greenq(0,0,1,t),redq(0,0,1,t))
		y = len(layer)*f(redq(0,0,1,t),greenq(0,0,1,t))
		xs += [x]
		ys += [y]

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

#for p in range(len(xs)):
#	print xs[p],ys[p]
