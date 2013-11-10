from fractions import Fraction
import sys

# this is a demonstration of the 'fox head' algorithm for finding
# the 'side' of a line that a point is on. 

# consider two points, p1, and p2. then imagine a line between p1, p2
# lets call it l. the foxhead of p1, p2, p3 will tell you which 'side'
# of the line l that p3 is on. or, if p3 is on the line, foxhead will
# tell you that as well.

# it uses the name 'fox head' because if you draw out the three 
# parallellograms formed by the three pairs of vectors, in a simple case 
# like (3,4) (4,3) (5,5), it kind of looks like a fox's head with two 
# big pointy ears.

def wedge( p1, p2 ):
	x1,y1,x2,y2=p1[0],p1[1],p2[0],p2[1]
	return x1*y2-x2*y1

def foxhead(p1,p2,p3):
	w1 = wedge( p1, p2 )
	w2 = wedge( p1, p3 )
	w3 = wedge( p3, p2 )
	print '1,2,3',w1,w2,w3
	if w3+w2 > w1: return 1
	elif w3+w2 < w1: return -1
	elif w3+w2==w1: return 0

xs,ys=[],[]
xs2,ys2=[],[]
xs3,ys3=[],[]
depth = 20

p1 = [-5,-5]
p2 = [-13,-15]
xs2 += [p1[0]]
ys2 += [p1[1]]
xs2 += [p2[0]]
ys2 += [p2[1]]
for m in range(-depth,depth):
	for n in range(-depth,depth):
		p3 = [m,n]
		if foxhead( p1, p2, p3 )<0:
			xs += [m]
			ys += [n]
		if foxhead( p1, p2, p3 )==0:
			xs2 += [m]
			ys2 += [n]
		if foxhead( p1, p2, p3 )>0:
			xs3 += [m]
			ys3 += [n]

print len(xs), 'points'
import numpy as np
import matplotlib.pylab as plt
fig,ax = plt.subplots(figsize=(8,8))
ax.set_ylim([-depth,depth])
ax.set_xlim([-depth,depth])
ax.scatter(xs,ys,c="red")
ax.scatter(xs2,ys2,c="yellow")
ax.scatter(xs3,ys3,c="blue")
plt.show()
print ax.scatter.__doc__
