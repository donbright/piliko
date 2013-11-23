from fractions import Fraction as Fract

##########
#
# rational parameterization of the torus
#
#########

#
# consider a basic torus
#
# x^2 + y^2 = 1 - l ^2
# l^2 + z^2 = 1 
# 
# use similar method to param of sphere, we get m1,n1,m2,n2 forming the torus.
#

xs,ys,zs=[],[],[]

depth=8
big_radius = 5
small_radius = 2
def blueq(m,n): return m*m+n*n
def redq(m,n): return m*m-n*n
def greenq(m,n): return 2*m*n
for m in range(-depth,depth):
	for n in range(-depth,depth):
		for m1 in range(-depth/2,depth/2):
			for n1 in range(-depth/2,depth/2):
				if m+n==0: continue
				if m1+n1==0: continue
				bq,rq,gq = blueq(m,n),redq(m,n),greenq(m,n)
				bq1,rq1,gq1 = blueq(m1,n1),redq(m1,n1),greenq(m1,n1)
				z = small_radius * Fract( rq1, bq1 )
				l = small_radius * Fract( gq1, bq1 )
				x = (big_radius-l) * Fract( rq, bq )
				y = (big_radius-l) * Fract( gq, bq )
				print x,y,z,' sq sum: ',x*x+y*y+z*z
				xs += [x]
				ys += [y]
				zs += [z]

max=max(xs+ys+zs)
for i in range(0,len(xs)):
        xs[i] = Fract( xs[i], max )
        ys[i] = Fract( ys[i], max )
        zs[i] = Fract( zs[i], max )


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

