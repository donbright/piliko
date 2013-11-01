from fractions import Fraction
import sys

# rational approximation of a unit circle using farey sequence and a 
# Chromogeometry - ish paramterization of unit pts on circle. requires 
# numpy, matplotlib

layer = [Fraction(0,1),Fraction(1,1)]
newlayer = []
depth=4
for i in range(1,depth):
	for i in range(len(layer)-1):
		new_numer = layer[i].numerator+layer[i+1].numerator
		new_denom = layer[i].denominator+layer[i+1].denominator
		new_number = Fraction( new_numer, new_denom )
		newlayer += [layer[i], new_number]
	newlayer += [1]
	print newlayer
	layer=newlayer
	newlayer=[]
xs,ys=[],[]
for i in range(0,len(layer)):
	newnumerator = layer[i].numerator
	newdenominator = layer[i].denominator
	n = newnumerator
	m = newdenominator
	x = Fraction( m*m-n*n , m*m+n*n )
	y = Fraction( 2*m*n , m*m+n*n )
	print x,y,layer[i]
	xs += [x]
	ys += [y]
	xs += [y]
	ys += [x]

	xs += [-x]
	ys += [y]
	xs += [-y]
	ys += [x]

	xs += [-x]
	ys += [-y]
	xs += [-y]
	ys += [-x]

	xs += [x]
	ys += [-y]
	xs += [y]
	ys += [-x]


print len(xs)
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
