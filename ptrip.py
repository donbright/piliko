# generate pythagorean triples as svg picture
import sys

points = {}

pmax=[0,0]
pmin=[0,0]

# print 'generating',

for r in range(0,30):
	if r % 100 == 1: pass
#		print '.',
#		sys.stdout.flush()
	for s in range(0,30):
		x = r*r - s*s
		y = 2 * r * s
		z = r*r + s*s
		# print x,y,z, ' => ', x*x+y*y, '=?=' , z*z
		points[str(x)+','+str(y)] = [x,y]
		pmax = [max(pmax[0],x),max(pmax[1],y)]
		pmin = [min(pmin[0],x),min(pmin[1],y)]

# print points
#print '. . count: ',len(points)
#print pmin, pmax
def sqr(x): return x*x

maxw = pmax[0] - pmin[0]
maxh = pmax[1] - pmin[1]
w = h = 1000
scale = '1'
r = '1'
print '<svg xmlns="http://www.w3.org/2000/svg" width="'+str(w)+'" height="'+str(h)+'">'
print '<g transform="scale('+scale+')" style="stroke: black; fill: none;">'
#print '<path d=" M0 0 '
for p in points:
	x=float(points[p][0])/maxw * w + w/2
	y=float(points[p][1])/maxh * h 
	xs,ys=str(x),str(y)
	# s='<circle cx="'+xs+'" cy="'+ys+'" r="'+xs+'"/>' 
	# s='<circle cx="'+xs+'" cy="'+ys+'" r="'+str( x+y / 580.0)+'"/>' 
	# s='<circle cx="'+xs+'" cy="'+ys+'" r="'+str( 18  )+'"/>' 
	s='<rect x="'+xs+'" y="'+ys+'" width="'+str( 1 )+'" height="'+str ( 1 ) +'"/>' 
	#s = 'L' + x + ' ' + y + ' '  # fill='none'
	print s
print '"/>'
print '</g>'
print '</svg>'
