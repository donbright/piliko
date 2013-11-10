import sys

# very simple rational paramterization / approximation of blue circle
# (x^2+y^2=1) useful as base for building other ideas

xs,ys=[],[]
x,y=-12.1568,2.5989
xs+=[x]
ys+=[y]
x,y=-21.4749,2.5989
xs+=[x]
ys+=[y]
x,y=-21.6506,2.65144e-15
xs+=[x]
ys+=[y]
x,y=-21.6506,1.32572e-15
xs+=[x]
ys+=[y]
x,y=-12.4315,7.61211e-16
xs+=[x]
ys+=[y]
x,y=-12.4315,1.30661
xs+=[x]
ys+=[y]




maxx=max(xs)
minx=min(xs)
maxy=max(ys)
miny=min(ys)
print xs
print ys
print len(xs), 'points'
import numpy as np
import matplotlib.pylab as plt
fig,ax = plt.subplots(figsize=(8,8))
ax.set_ylim([-5,5])
ax.set_xlim([-25,5])
ax.scatter(xs,ys)
plt.show()
