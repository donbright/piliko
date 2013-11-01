from fractions import Fraction

##########
##########
#
# rational parameterization of a hyperbolic 3 dimensional sheet thing.
#
# equation:
#
# x^2 + y^2 - z^2 = 1
#
#########
#########

# this is the same theory used to make the paramterization of the unit sphere
# using four integers, m,n,m1,n1. 

## consider a basic unit hyperbolic sheet thing
#
# x^2 + y^2 - z^2 = radius = 1^2
#
#   x^2 + y^2 = l^2
#   l^2 - z^2 = radius^2
#   radius = 1, radius^2=1
#
# example: begin with very simple pythagorean triple numbers:, 3,4,5
#          now, assume x=3, y=4, l=5, z=3, radius=4. divide all by 4
#
#          x=3/4, y=4/4, l=5/4, z=3/4, radius=4/4=1
#
# to verify: , 3^2=9 4^2=16, 5^2=25, 3^2=9 
# (3/4)^2+(4/4)^2-(3/4)^2 = (4/4)^2     [ qx+qy-qz=r=1 ]
# (3/4)^2+(4/4)^2 = (5/4)^2             [ qx+qy = ql   ]
# (5/4)^2-(3/4)^2 = (4/4)^2             [ ql-qz = qr=1 ]
#                                        qn = blue quadrance(n) = n^2
#
# therefore the given point, with x,y,z coordinates [ 3/4, 4/4, 5/4 ] is 
# a rational point on the unit hyperbolic sheet thing.

# theory
#
# step 0. We use Chromogeometry here for the sake of aesthetics.
#
# Blue Quadrance(x,y) = QBlue(x,y)   = x^2 + y^2
# Red Quadrance(x,y) = QRed(x,y)     = x^2 - y^2
# Green Quadrance(x,y) = QGreen(x,y) = 2xy
#
# step 1. find a rational paramterization of the hyperbola!
# 
# well, there are many, but lets use one based on Chromogeometry:
#
# first, review the unit sphere paramterization
# x = QRed(m,n) / QBlue(m,n)   y = QGreen(m, n) / QBlue(m,n)
#
# it turns out if you expand these, you can kind of see a nice hyperbolic
# paramterization:
#
# x = QBlue(m,n) / QRed(m,n)   y = QGreen(m, n) / QRed(m, n)
#
# you can verify that x^2 - y^2 = 1 by some very simply algebra. 
# 
#
# Step 3: expand the paramterization to 3 dimensions for the eqn' x^2+y^2-z^2=1

# Well, first, lets say that x^2+y^2 = l.
#
# Use the rational paramterization of the hyperbola to find l and z in terms of
# two integers, m and n.
# 
# l = m^2+n^2 / m^2-n^2     z = 2*m*n / m^2-n^2
# l = QBlue/QRed z = QGreen/QRed

# ok great. We have l and z. What about x and y?
#
#
# Well, recall that x^2 + y^2 = l^2. 
# divide this equation by l^2, you get this:
#  (x/l)^2 + (y/l)^2 = 1
# 
# We can use the rational paramterization of a unit circle but
# our "x" will actually be x/l and "y" will be y/l. We are using different
# m and n as well, call them "m1" and "n1" here. 
#
# x/l = m1^2-n1^2 / m1^2+n1^2     y/l = 2*m1*n1 / m1^2+n1^2
#
# x/l = QRed/QBlue  y/l = QGreen/QBlue   for Q(m1,n1)
#
# Now. That is quite interesting. You can choose m1, n1 as integers and get
# values for x/l and y/l. But what if you want just x or y by itself?
#
#
# Ahh, remember, we calculated l up above, based on two other integers, m and n
# you can multiple the equations above by l to get your sol'n for x and y. 
#
# x = l * ( m1^2-n1^2 / m1^2+n1^2 )      y  = l * ( 2*m1*n1 / m1^2+n1^2 )
#
# x = l * QRed/QBlue    y = l * QGreen/QBlue
#
# you can use Algebra to rearrange all this, but basically, in the end, 
# we have x, y, and z as functions of m, n, m1, and n1, four separate integers.
#
# l = QBlue/QRed z = QGreen/QRed     Q(m,n)
#
# x = QBlue(m,n)/QRed(m,n) *   QRed(m1,n1)/QBlue(m1,n1)
# y = QBlue(m,n)/QRed(m,n) * QGreen(m1,n1)/QBlue(m1,n1)
# z = QGreen(m,n)/QRed(m,n)
#
#
# possible problem: i have no idea if this works. 
#
# and others have probably found better.

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
				if qblue(m1,n1)==0: continue
				l = Fraction( qblue(m,n), qred(m,n) )
				x = l * Fraction( qred(m1,n1), qblue(m1,n1) )
				y = l * Fraction( qgreen(m1,n1), qblue(m1,n1) )
				z = Fraction( qgreen(m,n), qred(m,n) )
				print x,y,z,' sq sum: ',x*x+y*y+z*z

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

