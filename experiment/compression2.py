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
# when using standard python ASCII output for floats: rationals can be 
# much smaller, up until you get into bigger numbers... when the python 
# ASCII roundoff of floats comes into play and filesizes become roughly 
# equal. for example compare a run with ringcount set to 40 vs ringcount 
# set to 220

# interestingly, running compression, like 'zip' or 'xz', on the .txt 
# files shows the ASCII transcendental to be more 'compressible' than 
# ascii rationals?

# in binary: well, rationals are bigger than 32 bit floats. 

# however, if you assume there is a mythical utf8-style storage format for
# rationals, that allows variable-width numbers (1 byte, 2 bytes, etc) 
# rationals size becomes smaller than 64 bit floats. 

# but nothing crazily smaller, its all very dependent on the situation. 

# in conclusion its all quite dependent on the situation. 

# there is no automatic guarantee of space saving by using rationals.... 
# on the flip side, there is no automatic space saving by using floats 
# either. 

ringcount=60 # how many 'rings' will the circles tessellation have?
filenametr='comprtest.transcdntl.txt'
filenamerat='comprtest.ratl.txt'


# part 1: rational coordinates (integer/integer)

# note - blue, red, and green quadrance are from Norman Wildberger's 
# Chromogeometry
def sqr(x): return x*x
def greenq(x,y,x2,y2): return 2*(x2-x)*(y2-y)
def redq(x,y,x2,y2): return sqr(x2-x)-sqr(y2-y)
def blueq(x,y,x2,y2): return sqr(x2-x)+sqr(y2-y)
xs,ys=[],[]
xs2,ys2=[],[]

layers=[[]]
for m in range(0,ringcount*3/2):
	for n in range(0,ringcount*3/2):
		if blueq(0,0,m,n)==0: continue
		x = m*Fraction(redq(0,0,m,n),blueq(0,0,m,n))
		y = m*Fraction(greenq(0,0,m,n),blueq(0,0,m,n))
		if x<0: continue
		xs += [x]
		ys += [y]
                xs += [-x]
                ys += [y]
                xs += [x]
                ys += [-y]
                xs += [-x]
                ys += [-y]

#for j in range(0,ringcount):
#	layer=layers[j]
#	layers+=[[]]
#	for i in range(2*j):
#		num = i
#		denom = 2*j
#		layers[j] += [Fraction(num,denom)]
#	layers[j+1]+=[Fraction(1,1)]

#for i in layers:
#	print i,'\n'

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
for nn in range(1,ringcount): # layers[0:4]:
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
biggest=0
biggestval=0
for p in xs+ys:
	for dig in p.numerator,p.denominator:
		if biggestval<dig: biggestval=dig
		if dig>2**77:
			print 'overflow > 2**(77)'
		elif dig>2**61:
			if biggest<72: biggest=72
			bytecount+=9
		elif dig>2**53:
			if biggest<64: biggest=64
			bytecount+=8
		elif dig>2**45:
			if biggest<56: biggest=56
			bytecount+=7
		elif dig>2**37:
			if biggest<48: biggest=48
			bytecount+=6
		elif dig>2**29:
			if biggest<40: biggest=40
			bytecount+=5
		elif dig>2**21:
			if biggest<32: biggest=32
			bytecount+=4
		elif dig>2**12:
			if biggest<24: biggest=24
			bytecount+=3
		elif dig>2**5:
			if biggest<16: biggest=16
			bytecount+=2
		elif dig<2**5:
			bytecount+=1
			if biggest<8: biggest=8

floatcount32 = (len(txs)+len(tys))*4 # assume 32bit float x, 32 bit float y
floatcount64 = (len(txs)+len(tys))*8 # assume 64bit float x, 64bit float y
biggestcount = (len(xs)+len(ys))*(biggest/8)*2 # assume constant width of bytes
print 'bytecounts: ratl, transdtl 32bit, transdtl 64bit:', biggestcount, floatcount32,floatcount64
print 'biggest rational numerator or denominator:', biggestval, ',', biggest, 'bits'
print 'mythical utf-8ish ratl:', bytecount, 'bytes'
