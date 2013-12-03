from piliko import *
import math

# see spoly1 thru spoly5.py for explanation.

# spread polynomial
# it can generate spreads that are 'even', in other words, 
# its kind of like the addition of a single angle, over and over,
# but we are doing it with spreads. 

# since spreads cant be added simply, like angles, this is another 
# way to do it.

def sqr(x): return x*x
def blueq(x,y): return sqr(x)+sqr(y)
def redq(x,y): return sqr(x)-sqr(y)
def greenq(x,y): return 2*x*y
sp=spread_polynomial
maxn1=10
for i in range(0,maxn1):
	s = sp(i,Fraction(25,169))
	num = s.numerator
	dnm = s.denominator
	print ' spoly('+str(i)+',s)->',
	nx,nr=math.sqrt(abs(num)),math.sqrt(abs(dnm))
	print num,'/',dnm,'sqrts:',nx,nr
	print 'angle:',(math.asin(nx/nr)/3.1415926536)*180
print
