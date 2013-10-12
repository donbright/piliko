from fractions import Fraction
import sys

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

xs,ys,zs=[],[],[]

for m in layer:
	for n in layer:
		for m1 in layer:
			for n1 in layer:
				if n+m==0: continue
				if n1+m1==0: continue
				l = Fraction( m*m-n*n , m*m+n*n )
				z = Fraction( 2*m*n , m*m+n*n )
				x = l * Fraction( m1*m1-n1*n1, m1*m1+n1*n1 )
				y = l * Fraction( 2*m1*n1    , m1*m1+n1*n1 )
				print x,y,z,' sq sum: ',x*x+y*y+z*z
				xs += [x]
				ys += [y]
				xs += [y]
				ys += [x]
				zs += [z]
				zs += [-1*z]

print len(xs)
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

