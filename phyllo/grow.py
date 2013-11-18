from fractions import Fraction as Fr
import sys
import numpy as np
import matplotlib.pylab as plt

def plot(xs, ys):
        maxx=max(xs)
        minx=min(xs)
        maxy=max(ys)
        miny=min(ys)
        fig,ax = plt.subplots(figsize=(8,8))
        ax.set_xlim([minx-2,maxx+2])
        ax.set_ylim([miny-2,maxy+2])
        ax.scatter(xs,ys)
        ax.plot(xs,ys)
        plt.show()

class vector:
	x,y=0,0
	def __init__(self,x1,y1):
		self.x=x1
		self.y=y1
	def __str__(self): return '['+str(self.x)+','+str(self.y)+']'
	def __repr__(self): return self.__str__()

def split(v):
	mx=Fr(v.x,2)
	my=Fr(v.y,2)
	qx=Fr(v.x,4)
	qy=Fr(v.y,4)
	nx = mx-qy
	ny = my-qx
	v1 = vector(nx,ny)
	v2 = vector(v.x-nx,v.y-ny)
	return v1, v2

vecs = [vector(1,0)]
xs,ys=[],[]
curs = vector(0,0)
depth=10
for i in range(depth):
	newvecs=[]
	for v in vecs:
		curs.x += v.x
		curs.y += v.y
		xs+=[curs.x]
		ys+=[curs.y]
		nv1, nv2 = split(v)
		newvecs += [nv1]
		newvecs += [nv2]
	vecs = newvecs

for i in range(len(xs)):
	xs[i] = float(xs[i])
	ys[i] = float(ys[i])
plot(xs,ys)
