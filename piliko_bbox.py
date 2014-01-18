from piliko import *
############## bounding box

def bounding_box_circle( c ):
	xmin = c.center.x-babylonian_square_root(abs(c.radial_quadrance))
	xmax = c.center.x+babylonian_square_root(abs(c.radial_quadrance))
	ymin = c.center.y-babylonian_square_root(abs(c.radial_quadrance))
	ymax = c.center.y+babylonian_square_root(abs(c.radial_quadrance))
	return point(xmin,ymin),point(xmax,ymax)

def bounding_box_triangle( t ):
	xmin = min(t.p0.x,t.p1.x,t.p2.x)
	ymin = min(t.p0.y,t.p1.y,t.p2.y)
	xmax = max(t.p0.x,t.p1.x,t.p2.x)
	ymax = max(t.p0.y,t.p1.y,t.p2.y)
	return point(xmin,ymin),point(xmax,ymax)
def bounding_box_triangles( ts ):
	minp,maxp = bounding_box_triangle(ts[0])
	tmpbox = bounding_box(minp,maxp)
	for t in ts: tmpbox.extend(bounding_box_triangle(t))
	return tmpbox.min,tmpbox.max
def bounding_box_circles( cs ):
	minp,maxp = bounding_box_circle(cs[0])
	tmpbox = bounding_box(minp,maxp)
	for c in cs: tmpbox.extend(bounding_box_circle(c))
	return tmpbox.min,tmpbox.max
def bounding_box_points( pts ):
	xmin,ymin,xmax,ymax=pts[0].x,pts[0].y,pts[0].x,pts[0].y
	for p in pts:
		xmin = min(xmin,p.x)
		ymin = min(ymin,p.y)
		xmax = max(xmax,p.x)
		ymax = max(ymax,p.y)
	return point(xmin,ymin),point(xmax,ymax)
def bounding_box_bboxes( boxes ):
	tmpbox = bounding_box(boxes[0].min,boxes[0].max);
	for b in boxes:
		tmpbox.extend( b.min, b.max )
	return tmpbox.min,tmpbox.max
def bounding_width( *args ):
	if checktypes(triangle,args) and len(args==1):
		minp,maxp = bbox_triangle( args[0] )
		return Fraction(minp.x+maxp.x,2)
def bounding_height( *args ):
	if checktypes(triangle,args) and len(args==1):
		minp,maxp = bbox_triangle( args[0] )
		return Fraction(minp.y+maxp.y,2)

class bounding_box:
	def __init__(self,*args):
		testmin,testmax = None,None
		if checktypes(triangle,*args):
			testmin,testmax = bounding_box_triangles( args )
		elif checktypes(point,*args):
			testmin,testmax = bounding_box_points( args )
		elif checktypes(bounding_box,*args):
			testmin,testmax = bounding_box_bboxes( args )
		elif checktypes(circle,*args):
			testmin,testmax = bounding_box_circles( args )
		elif checktypes(list,*args):
			if len(args)==2 and checkrationals(args[0][0]):
				xs,ys=args[0],args[1]
				testmin=point(min(xs),min(ys))
				testmax=point(max(xs),max(ys))
			else:
				for l in args:
					for item in l:
						self.extend(item)
		elif checktypes(tuple,*args):
			for l in args:
				for item in l:
					bb = bounding_box(item)
					self.min,self.max=bb.min,bb.max
		else:
			raise Exception('unknown types:'+str(args))
		self.min,self.max = testmin,testmax
	def extend(self,*args):
		testmin,testmax=self.min,self.max
		if checktypes(triangle,*args):
			testmin,testmax = bounding_box_triangles( args )
		elif checktypes(point,*args):
			testmin,testmax = bounding_box_points( args )
		elif checktypes(bounding_box,*args):
			testmin,testmax = bounding_box_bboxes( args )
		elif checktypes(circle,*args):
			testmin,testmax = bounding_box_circles( args )
		elif checktypes(list,*args):
			if len(args)==2 and checkrationals(args[0][0]):
				xs,ys=args[0],args[1]
				testmin=point(min(xs),min(ys))
				testmax=point(max(xs),max(ys))
			else:
				for l in args:
					for item in l:
						self.extend(item)
		elif checktypes(tuple,*args):
			for l in args:
				for item in l:
					self.extend(item)
		else: raise Exception('cannot extend,unknown type',args)
		self.min.x = min(testmin.x,self.min.x)
		self.min.y = min(testmin.y,self.min.y)
		self.max.x = max(testmax.x,self.max.x)
		self.max.y = max(testmax.y,self.max.y)
		return self
	def __add__( self, p): return self.extend( p )
	def add( self, p): return self.extend( p )
	def addto( self, p): return self.extend( p )
	def __str__(self): return bounding_box_txt(self)
	def width(self): return self.max.x-self.min.x
	def height(self): return self.max.y-self.min.y
	def frame(self): # slightly larger box
		newminx = self.min.x - self.width() * Fraction(5,100)
		newmaxx = self.max.x + self.width() * Fraction(5,100)
		newminy = self.min.y - self.height() * Fraction(5,100)
		newmaxy = self.max.y + self.height() * Fraction(5,100)
		return point(newminx,newminy),point(newmaxx,newmaxy)

