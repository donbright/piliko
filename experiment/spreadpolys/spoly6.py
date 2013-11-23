from piliko import *
import math

# ok so uhm

# see spoly1 thru spoly5.py for explanation.

# basically we are taking a generator of pythagorean triples,
# and plugging the output from that into the spread polynomial function
# 
# the result is a bunch of perfect squares. seems lovely to me.. maybe
# obvious to others of course.

#
# this version uhm... it flips around the pyth triple generator ...
# using cheomogeometry. 
#
# normally the unit circle is x=red/blue, y=green/blue
# the hyperbola is x=green/red y=blue/red
# so... uhm.. if you just flip those around here, you also get
# perfect squares, the problem is that some of them are Negative
# so you are technically getting the perfect square of complex numbers..
# anyways.

def sqr(x): return x*x
def blueq(x,y): return sqr(x)+sqr(y)
def redq(x,y): return sqr(x)-sqr(y)
def greenq(x,y): return 2*x*y
sp=spread_polynomial
maxn1=5
for m in range(1,20):
	for n in range(1,20):
		x = greenq(m,n)
		y = blueq(m,n)
		print 'for m,n',m,n
		inputnum = y*y 
		inputdnm = redq(x,y)
		print ' s= (',inputnum,') / (',inputdnm, ')'
		for i in range(0,maxn1):
			if inputdnm==0: continue
			s = sp(i,Fraction(inputnum,inputdnm))
			num = s.numerator
			dnm = s.denominator
			print ' spoly('+str(i)+',s)->',
			print num,'/',dnm,'sqrts:',math.sqrt(abs(num)),math.sqrt(abs(dnm))
print
