import sys
import numpy as np
import matplotlib.pylab as plt


def plot(xs, ys):
	maxx=max(xs)
	minx=min(xs)
	maxy=max(ys)
	miny=min(ys)
	fig,ax = plt.subplots(figsize=(5,5))
	ax.set_ylim([-50,50])
	ax.set_xlim([-50,50])
	ax.scatter(xs,ys)
	ax.plot(xs,ys)
	plt.show()

lines=open('/tmp/pfile').readlines()
i = 0
trip = False
for l in lines:
	if l[0:len('pdata=')]=='pdata=':
		data=l[len('pdata='):]
		xs,ys=[],[]
		for x,y in eval(data):
			xs+=[x]
			ys+=[y]
		print len(xs), 'points read'
		xs+=[xs[0]]
		ys+=[ys[0]]
		if len(xs)<25:
			plot(xs,ys)
			trip=True

	if l[0:len('edata=')]=='edata=':
		data=l[len('edata='):]
		xs,ys=[],[]
		for x,y in eval(data):
			xs+=[x]
			ys+=[y]
		for i in range(len(xs)): print xs[i],ys[i],' ',
		print len(xs), ' <ear points read'
		xs+=[xs[0]]
		ys+=[ys[0]]
		if trip: plot(xs,ys)
		
