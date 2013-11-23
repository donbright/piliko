from piliko import *
import math

# ok so uhm

# see spoly4.py for explanation.

# basically we are taking a generator of pythagorean triples,
# and plugging the output from that into the spread polynomial function
# (well, plugging in a leg and a hypoteneuse, both squared)
# 
# the result is a bunch of perfect squares. seems lovely to me.. maybe
# obvious to others of course.
#


def sqr(x): return x*x
def blueq(x,y): return sqr(x)+sqr(y)
def redq(x,y): return sqr(x)-sqr(y)
def greenq(x,y): return 2*x*y
sp=spread_polynomial
maxn1=5
for m in range(1,20):
	for n in range(1,20):
		x = redq(m,n)
		y = greenq(m,n)
		print 'for m,n',m,n
		inputnum = y*y # y*y # opposite leg of triangle (squared)
		inputdnm = blueq(x,y) # hypoteneuse of triangle (squared)
		print ' s= (',inputnum,') / (',inputdnm, ')'
		for i in range(0,maxn1):
			s = sp(i,Fraction(inputnum,inputdnm))
			num = s.numerator
			dnm = s.denominator
			print ' spoly('+str(i)+',s)->',
			print num,'/',dnm,'sqrts:',math.sqrt(num),math.sqrt(dnm)
print
