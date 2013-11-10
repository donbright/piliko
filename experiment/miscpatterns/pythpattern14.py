from fractions import Fraction as f
import sys

# strange patterns by looking at pythagorean triples
#
# this is using the '1-t^2,1+t^2' paramterization of the circle
#

# but with attempting to make 'rings' instead of the circle itself

# also using the farey seq as input to 't'

# result is an interesting sort of tessellation, but not quite as
# smooth as pythpattern12
#
# note - blue, red, and green quadrance are from Norman Wildberger's 
# Chromogeometry

def sqr(x): return x*x
def greenq(x,y,x2,y2): return 2*(x2-x)*(y2-y)
def redq(x,y,x2,y2): return sqr(x2-x)-sqr(y2-y)
def blueq(x,y,x2,y2): return sqr(x2-x)+sqr(y2-y)
xs,ys=[],[]
xs2,ys2=[],[]

depth=4
layers=[[f(0,1),f(1,1)]]
for j in range(0,depth):
	layer=layers[j]
	layers+=[[]]
	for i in range(len(layer)-1):
		num = layer[i].numerator+layer[i+1].numerator
		denom = layer[i].denominator+layer[i+1].denominator
		layers[j+1] += [layer[i],f(num,denom)]
	layers[j+1]+=[f(1,1)]

for i in layers:
	print i,'\n'

for layer in layers:
	for t in layer:
		if blueq(0,0,1,t)==0: continue
		x = len(layer)*f(redq(0,0,1,t),blueq(0,0,1,t))
		y = len(layer)*f(greenq(0,0,1,t),blueq(0,0,1,t))
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
