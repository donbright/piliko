from piliko import *
import math

# ok so uhm

# so it turns out that if you feed the leg and hypoteneuse of 
# pythagorean triples, squared, into the spread polynomial function, you 
# get these perfect squares as output. maybe this is obvious to some 
# people but it seems kind of nice to me.
#
# but how can we generate pythagorean triples? well, there is the
# ol' paramterization of the unit circle style of generation, 
# which I sort of remember someone calling Euclid's method but I can't
# remember at the moment. 
#
# but i like to use chromogeometry for that. its the same thing but it 
# saves space in my head to just think of it as 'red/blue, green/blue'
# isntead of the long formula
#
# anyways. we take the pythagorean triple generator output, and put
# it into the input of the spread polynomial function. 
#
# this generates a bunch of perfect squares. kind of interesting. 
#


# this version uses unit circle. uhm. yeah. you dont have to. 
# see spoly4.py

def sqr(x): return x*x
def blueq(x,y): return sqr(x)+sqr(y)
def redq(x,y): return sqr(x)-sqr(y)
def greenq(x,y): return 2*x*y
sp=spread_polynomial
maxn1=5
for m in range(1,10):
	for n in range(1,10):
		x = Fraction(redq(m,n),blueq(m,n))
		y = Fraction(greenq(m,n),blueq(m,n))
		print 'for m,n',m,n
		inputnum = y*y # opposite leg of triangle (squared)
		inputdnm = blueq(x,y) # hypoteneuse of triangle (squared)
		print ' s= (',inputnum,') / (',inputdnm, ')'
		for i in range(0,maxn1):
			s = sp(i,Fraction(inputnum,inputdnm))
			num = s.numerator
			dnm = s.denominator
			print ' spoly('+str(i)+',s)->',
			print num,'/',dnm,'sqrts:',math.sqrt(num),math.sqrt(dnm)
print
