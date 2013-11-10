from fractions import Fraction as Fract

##########
#
# rational parameterization of the torus
#
#
# this torus has a non-circular 'tube' cross-section. its kind of warped
# triangular.
#
#########

# theory,briefly: consider a torus.
#
# x^2 + y^2 = 1 - l ^2
# l^2 + z^2 = 1 
# 
# use similar method to param of sphere, we get m1,n1,m2,n2 forming the torus.
# 
# note chromogeometry notation is used.
# 
#
# the 'warped' cross section comes as follows:
#
# see pythcircwarp.py 
#
# an ordinary circle has this paramterization for rationals m,n:
#  x=red(0,0,m,n)/blue(0,0,m,n), y=green(0,0,m,n)/blue(0,0,m,n) 
#
# a 'warped' circle can go like this:
#  x=red(0,0,m,n)/blue(-n,0,m,n), y=green(0,0,m,n)/blue(0,0,m,n) 
# 
# so... for the torus... if you use this 'warped' version for 'z' and 
# 'l' instead of x,y you get a warped cross-section for your torus tube 
# instead of a circle.
#
#
# in fact, i suspect you could use basically any 2d curve paramterization 
# here to create any kind of cross section for your torus that you want.
# (well almost any...its only stuff that has rational paramaterization )

xs,ys,zs=[],[],[]

depth=5
big_radius = 5
small_radius = 2
def blueq(m,n): return m*m+n*n
def redq(m,n): return m*m-n*n
def greenq(m,n): return 2*m*n
def blueq_pts(a1,b1,a2,b2): return (a2-a1)*(a2-a1)+(b2-b1)*(b2-b1)
for m in range(-depth,depth):
	for n in range(-depth,depth):
		for m1 in range(-depth,depth):
			for n1 in range(-depth,depth):
				if m+n==0: continue
				if m1+n1==0: continue
				bq,rq,gq = blueq(m,n),redq(m,n),greenq(m,n)
				bq1,rq1,gq1 = blueq(m1,n1),redq(m1,n1),greenq(m1,n1)
				wbq1 = blueq_pts(-n1,0,m1,n1)
				z = small_radius * Fract( rq1, wbq1 )
				l = small_radius * Fract( gq1, bq1 )
				x = (big_radius-l) * Fract( rq, bq )
				y = (big_radius-l) * Fract( gq, bq )
				print x,y,z,' sq sum: ',x*x+y*y+z*z
				xs += [x]
				ys += [z]
				zs += [y]

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

