from fractions import Fraction

##########
##########
#
# rational parameterization of a hyperbolic 3 dimensional sheet thing.
# take 2.
#
# equation:
#
# x^2 - y^2 - z^2 = 1
#
#########
#########

# this is the same theory used to make the paramterization of the unit sphere
# using four integers, m,n,m1,n1. 

# Chromogeometry is used for the sake of aesthetics.
# q is short for 'quadrance'
#
# qblue(x,y)=x^2+y^2  qred(x,y)=x^2-y^2  qgreen(x,y)=2xy
#
# please see pthhypsheet.py for the full theory and derivation. 

# basically, consider a simple hyperbola.
# x^2 - y^2 = 1 
#
# it has has a paramteriztaion like this: 
#
# x=qblue(m,n)/qred(m.n) y=qgreen(m,n)/qred(m,n)
#

# so. x^2-y^2=l^2, and l^2-z^2=1
#
# so l = qblue(m,n)/qred(m,n), z=qgreen(m,n)/qred(m,n), for integers m,n
#
# also
#
# x^2/l^2 - y^2/l^2 = 1, so use a new set of m,n, call them m1,n1
#
# x/l = qblue(m1,n1)/qred(m1,n1)    y/l = qgreen(m1,n1)/qred(m1,n1)
#
# so put l back in, solve for x or y:
#
# x = l * qblue/qred(m,n)
# y = l * qblue/qred(m,n)
# z = qgreen/qred(m,n)
#
# now x^2+y^2-z^2=1
#

xs,ys,zs=[],[],[]

def sqr(x): return x*x
def qblue(x,y): return sqr(x)+sqr(y)
def qred(x,y): return sqr(x)-sqr(y)
def qgreen(x,y): return 2*x*y

depth=8
for m in range(0,depth):
	for n in range(0,depth):
		for m1 in range(0,depth):
			for n1 in range(0,depth):
				if qred(m,n)==0: continue
				if qblue(m,n)==0: continue
				if qred(m1,n1)==0: continue
				l = Fraction( qblue(m,n), qred(m,n) )
				x = l * Fraction( qblue(m1,n1), qred(m1,n1) )
				y = l * Fraction( qgreen(m1,n1), qred(m1,n1) )
				z = Fraction( qgreen(m,n), qred(m,n) )
				print x,y,z,' sq rq(rq(x,y),z): ',x*x-y*y-z*z

				xs += [x]
				ys += [y]
				zs += [z]

				xs += [x]
				ys += [-y]
				zs += [z]

print len(xs)
import numpy as np
import matplotlib.pylab as plt
fig,ax = plt.subplots(figsize=(8,8))

ax.set_ylim([-5.2,5.2])
ax.set_xlim([-5.2,5.2])
for i in range(0,len(xs)):
	xs[i]=xs[i]+zs[i]/4
	ys[i]=ys[i]+zs[i]/4
ax.scatter(xs,ys)
plt.show()

