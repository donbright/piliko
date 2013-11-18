import sys
import numpy as np
import matplotlib.pylab as plt


def plot(xs, ys):
	maxx=max(xs)
	minx=min(xs)
	maxy=max(ys)
	miny=min(ys)
	fig,ax = plt.subplots(figsize=(5,5))
	ax.set_ylim([miny-2,maxy+2])
	ax.set_xlim([minx-2,maxx+2])
	ax.scatter(xs,ys)
	ax.plot(xs,ys)
	plt.show()

xs,ys=[],[]
s=open('t').read()
toks = s.split()
i=0
for tok in toks:
	if i%2==0: xs += [float(tok)]
	else: ys += [float(tok)]
	i+=1
xs += [xs[0]]
ys += [ys[0]]
plot(xs,ys)
