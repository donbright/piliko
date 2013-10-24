from fractions import Fraction
import sys,math

# compare two tessellations of a circular disk

# trascendental vs rational coordinates
# (aka cos/sin vs integer/integer)

# roughly equal density and number of points

# which is more compressible in data size?

#####
## result
#
# when using standard python ASCII output for floats:
#
# the .txt ascii files are much smaller for rationals
# for small number of points. as the number of points grows,
# the sizes become similar
#
# interesting: a plain .zip of the .txt files results in the rationals
# being larger after zip than the transcendentals! interesting. 

# 
# mythical binary format:
#
# assuming you could create a UTF8 style reader/writer for rationals
# that would put numbers like 23/129 into 16 bits, (two 8-bit #s)
# but larger digits like 12003/47304 into 32 bits, (two 16-bit #s)
# you could theoretically store rationals with 1/3 the size of 32-bit floats
# or 1/3 the size of 64-bit floats, roughly. (make depth=200 for example to see)
# of course you need to invent such a reader/writer... shall we assume
# 3 bits of each byte is 'control bits'?
#
#



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

depth=50
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

# Rational - assume some format like UTF8 where size is related to data stored
# with 3 bits per number being used up as 'control bits' (8-3, 16-3, 32-3, ...)
bytecount=0
for p in xs+ys:
	for dig in p.numerator,p.denominator:
		if dig.numerator>2**109: print 'overflow > 2**(112-3)'
		elif dig.numerator>2**93: bytecount+=6
		elif dig.numerator>2**77: bytecount+=5
		elif dig.numerator>2**61: bytecount+=4
		elif dig.numerator>2**29: bytecount+=3
		elif dig.numerator>2**12: bytecount+=2
		elif dig.numerator>2**5: bytecount+=1 

floatcount32 = (len(txs)+len(tys))*4 # assume 32bit float x, 32 bit float y
floatcount64 = (len(txs)+len(tys))*8 # assume 64bit float x, 64bit float y

print 'bytecounts: ratl, transdtl 32bit, transdtl 64bit', bytecount, floatcount32,floatcount64
