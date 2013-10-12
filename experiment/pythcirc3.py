from fractions import Fraction
import sys

# rational approximation of a unit circle using 
# Chromogeometry - ish paramterization of unit pts on circle. requires 
# numpy, matplotlib

# uses 'flat' list of input fractions. not farey sequence as in other
# experiments

# also this version limits blue quadrance between points... so you get a 
# sort of rational approximation of a 'regularly divided' circle as 
# formed by a geographer's latitude lines  ( hopefully )

def sqr(x): return x*x
def blueq(x,y,x2,y2): return sqr(x2-x)+sqr(y2-y)

layer=[]
n=1064
for i in range(0,n+1):
	layer+=[Fraction(i,n)]
print layer[0:2],'...(',len(layer),')...',layer[-1]
blueqlimit = Fraction(1,64)
xs,ys=[0],[1]
print 'blue q limit',blueqlimit
for i in range(0,len(layer)):
	newnumerator = layer[i].numerator
	newdenominator = layer[i].denominator
	n = newnumerator
	m = newdenominator
	x = Fraction( m*m-n*n , m*m+n*n )
	y = Fraction( 2*m*n , m*m+n*n )
	ptOK=True
	for j in range(len(xs)):
		if blueq(x,y,xs[j],ys[j])<blueqlimit:
			ptOK=False
		if blueq(-x,y,x,y)<blueqlimit:
			ptOK=False
	if ptOK:
		print x,y,layer[i]
		xs += [x]
		ys += [y]
		xs += [-x]
		ys += [y]


print len(xs), 'points'
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
