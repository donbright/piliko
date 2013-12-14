# random objects

from piliko import *
from random import randint

def random_point(*args):
	x1,x2=-10,10
	y1,y2=-10,10
	if checktypes(point,*args) and len(args)==2: #bound rect by points
		x1,x2,y1,y2=args[0].x,args[1].x,args[0].y,args[1].y
	elif checkrationals(*args) and len(args)==2: # bound square by coords
		x1,x2=args[0],args[1]
		y1,y2=x1,x2
	else: raise Exception('unknown args for random_point')
	xmin,xmax=min(x1,x2),max(x1,x2)
	ymin,ymax=min(y1,y2),max(y1,y2)
	return point(randint(xmin,xmax),randint(ymin,ymax))

def random_triangle(*args):
	if checktypes(point,*args) and len(args)==2: # bounding rectangle
		p1=random_point(*args)
		p2=random_point(*args)
		p3=random_point(*args)
	elif checkrationals(*args) and len(args)==2: # bounding square
		p1=random_point(*args)
		p2=random_point(*args)
		p3=random_point(*args)
	else: raise Exception('unknown args for random_triangle')
	return triangle(p1,p2,p3)
