from fractions import Fraction
import sys,math

# compare two tessellations of a circular disk

# trascendental vs rational coordinates
# (aka cos/sin vs integer/integer)

# which is more compressible in data size?


# note - blue, red, and green quadrance are from Norman Wildberger's 
# Chromogeometry


filenametr='comprtest.transcdntl.txt'
filenamerat='comprtest.ratl.txt'


# part 1: rational coordinates (integer/integer)

def sqr(x): return x*x
def greenq(x,y,x2,y2): return 2*(x2-x)*(y2-y)
def redq(x,y,x2,y2): return sqr(x2-x)-sqr(y2-y)
def blueq(x,y,x2,y2): return sqr(x2-x)+sqr(y2-y)
xs,ys=[],[]
xs2,ys2=[],[]

depth=200
layers=[[]]
for j in range(0,depth):
	layer=layers[j]
	layers+=[[]]
	for i in range(2*j):
		num = i
		denom = 2*j
		layers[j] += [Fraction(num,denom)]
	layers[j+1]+=[Fraction(1,1)]

#for i in layers:
#	print i,'\n'

for layer in layers:
	for t in layer:
		if blueq(0,0,1,t)==0: continue
		x = len(layer)*Fraction(redq(0,0,1,t),blueq(0,0,1,t))
		y = len(layer)*Fraction(greenq(0,0,1,t),blueq(0,0,1,t))
		xs += [x]
		ys += [y]
		xs += [-x]
		ys += [y]
		xs += [-x]
		ys += [-y]
		xs += [x]
		ys += [-y]

maxv=max(xs+ys)

for i in range(0,len(xs)):
	xs[i] = Fraction(xs[i], maxv )
	ys[i] = Fraction(ys[i], maxv )

outs=''
for p in range(len(xs)):
	# print xs[p],ys[p]
	outs+=str(xs[p])+','+str(ys[p])+'\n'
print '      rational coords:',len(xs),'points. output .txt bytes:',len(outs)
f=open(filenamerat,'w')
f.write(outs)
f.close()

# transcendental (cos/sin)

layers=[]
layers=[[]]
txs=[]
tys=[]
for nn in range(1,depth): # layers[0:4]:
	angle = 0
	for t in range(0,4*nn+1):
		#angle += 360/len(layer)
		angle = (float(t)/float(4*nn))*(math.pi)
		x = nn*math.cos(angle)
		y = nn*math.sin(angle)
		# print t,nn,float(t)/float(nn),angle,angle/math.pi,x,y
		txs+=[x]
		tys+=[y]
		txs+=[x]
		tys+=[-y]

maxv=max(txs+tys)

for i in range(0,len(txs)):
	txs[i] = txs[i] / maxv
	tys[i] = tys[i] / maxv

outs=''
for p in range(len(txs)):
	outs+=str(txs[p])+','+str(tys[p])+'\n'
print 'transcendental coords:',len(txs),'points. output .txt bytes:',len(outs)
f=open(filenametr,'w')
f.write(outs)
f.close()
print 'files written',filenamerat, filenametr

# calc binary size
bytecount=0
for p in xs+ys:
	for dig in p.numerator,p.denominator:
		if dig.numerator>256*256*256*256*256: bytecount+=5
		elif dig.numerator>256*256*256*256: bytecount+=4
		elif dig.numerator>256*256*256: bytecount+=3
		elif dig.numerator>256*256: bytecount+=2
		elif dig.numerator>256: bytecount+=1 

floatcount = len(txs)*4*4 # assume 32bit float x, 32 bit float y

print 'bytecounts: ratl, transdtl', bytecount, floatcount
