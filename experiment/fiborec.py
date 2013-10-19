from fractions import Fraction as f
import sys

# draw points of squares->tiling a rectangle
# size of squares = fibonacci seq

def sqr(x): return x*x
def greenq(x,y,x2,y2): return 2*(x2-x)*(y2-y)
def redq(x,y,x2,y2): return sqr(x2-x)-sqr(y2-y)
def blueq(x,y,x2,y2): return sqr(x2-x)+sqr(y2-y)
xs,ys=[],[]

depth=50
class Cursor:
	direction=[0,1]
	position=[0,0]
	def forward(self,n):
		self.position[0]=self.position[0]+self.direction[0]*n
		self.position[1]=self.position[1]+self.direction[1]*n
	def turnleft(self): 
		# North->West->South->East->North
		# 0,1 -> -1,0 -> 0,-1 -> 1,0 -> 0,1
		tmp=self.direction[0]
		self.direction[0]=-1*self.direction[1]
		self.direction[1]=tmp

cursor=Cursor()
rabbits=[0,1]
for i in range(depth):
	p1 = [cursor.position[0],cursor.position[1]]
	cursor.forward(rabbits[-1])
	p2 = [cursor.position[0],cursor.position[1]]
	cursor.turnleft()
	cursor.forward(rabbits[-1])
	p3 = [cursor.position[0],cursor.position[1]]
	xs += [p1[0]]
	ys += [p1[1]]
	xs += [p2[0]]
	ys += [p2[1]]
	xs += [p3[0]]
	ys += [p3[1]]
	xs += [p1[0]]
	ys += [p1[1]]

	rabbits+=[rabbits[-1]+rabbits[-2]]

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
#ax.scatter(xs,ys)
ax.plot(xs,ys)
plt.show()
