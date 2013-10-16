from fractions import Fraction

##########
##########
#
# rational parameterization of the unit sphere
#
#########
#########

# for basic theory see pythsphere and pythsphere2.py
#
# this version differs in that it limits distance between points to a minimum

def sqr(x): return x*x
def blueq(p1,p2): return sqr(p2[0]-p1[0])+sqr(p2[1]-p1[1])+sqr(p2[2]-p1[2])

xs,ys,zs=[],[],[]

blueqlimit=Fraction(1,8*8*8)
depth=6
for m in range(0,depth):
	for n in range(0,depth):
		for m1 in range(0,depth):
			for n1 in range(0,depth):
				if m+n==0: continue
				if m1+n1==0: continue
				l = Fraction( m*m-n*n , m*m+n*n )
				z = Fraction( 2*m*n , m*m+n*n )
				x = l * Fraction( m1*m1-n1*n1, m1*m1+n1*n1 )
				y = l * Fraction( 2*m1*n1    , m1*m1+n1*n1 )
				ptOK=True
				for j in range(len(xs)):
					p1=x,y,z
					p2=xs[j],ys[j],zs[j]
					if blueq(p1,p2)<blueqlimit:
						ptOK=False
				if ptOK:
					print x,y,z,' sq sum: ',x*x+y*y+z*z
					xs += [x]
					ys += [y]
					xs += [x]
					ys += [y]
					zs += [z]
					zs += [-z]

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

