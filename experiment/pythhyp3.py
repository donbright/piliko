from fractions import Fraction as f
import sys

# rational paramterization of hyperbola, using Norman Wildberger's 
# Chromogeometry.


#
# step 1. lets review the rational paramterization of an ordinary circle 
# (blue circle). in an ordinary circle, x^2+y^2 = radius^2. for a unit 
# circle, you can say x^2+y^2=1. in chromogeometry, you can say the blue 
# quadrance between 0,0 and x,y is 1. 
# 
# now, a 'rational parametirzation' of a circle will give you the x,y 
# coordinates of the circle where x and y are both rational numbers. if 
# your radius is rational too, this basically means you are generating 
# points that are exactly on the circle, with no sin/cos approximation 
# involved. fun fact: if your radius is rational, you are basically 
# generating pythagorean triples.
#
#
# here is a common rational parameterization of the circle you will see 
# in various places, like so: first, generate a bunch of integers, m and 
# n. then make x,y coordinates like so:
#
#
#  x,y = m^2-n^2  /  m^2+n^2  ,  2*m*n / m^2+n^2
#
# 
#  this can be thought of in chromogeometry using red,blue,and green quadrances
#  between 0,0 and a sequence of made-up coordinates, m,n. like so:
#  
#  x,y = red q(0,0,m,n)/blue q(0,0,m,n), green q(0,0,m,n)/blue q(0,0,m,n)
#

# Note here that another popular rational circle paramterization that 
# you see, '1-t^2 / 1+t^2, 2t / 1+t^2' is just setting m to '1' and 
# varying n. or vice versa. we can also rerite that paramterization with 
# chromogeometry

#  x,y = red q(0,0,1,t)/blue q(0,0,1,t), green q(0,0,1,t)/blue q(0,0,1,t)

# to simplify,....

# x,y = redq/blueq, greenq/blueq



# what does this have to do with hyperbolas?

# in chromogeometry, the x^2-y^2=k hyperbola is called a 'red circle' 

#
# lets just switch around the terms in our paramterization. 
# for the blue circle we had 
#
# x,y = red q/blue q, green q/blue q
# 
# after playing around with the above alot (see the pythpattern*py programs)
# it becomes evident the 'divisor' or 'denominator' term kind of has a lot
# to do with the shape here. 
#
#
# well, what if for the 'red circle' we can try this:
#
# x,y = blue q/red q, green q/red q ??
#
# plot it out and what do we get?
#
# a hyperbola! interesting.
#
# but lets not stop there.

# pythpattern15 gave a rational 'tessellation' of a disk, or a filled circle.
# in other words, it drew a bunch of concentric rational approximations of
# circles. 

# can we have a 'red disk' in chromogemtry? can we 'tessellate' it with 
# 'concentric red circles'? yes, yes we can. this program does it. the 
# resulting shape looks like some kind of single-wing glider from outer 
# space or maybe like a fish fin.

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
	for i in range(j):
		num = i
		denom = j
		layers[j] += [f(num,denom*2)]
	layers[j+1]+=[f(1,1)]

for i in layers:
	print i,'\n'

for layer in layers:
	for t in layer:
		if redq(0,0,1,t)==0: continue
		x = len(layer)*f(blueq(0,0,1,t),redq(0,0,1,t))
		y = len(layer)*f(greenq(0,0,1,t),redq(0,0,1,t))
		xs += [x]
		ys += [y]
		xs += [x]
		ys += [-y]

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

for p in range(len(xs)):
	print xs[p],ys[p]
