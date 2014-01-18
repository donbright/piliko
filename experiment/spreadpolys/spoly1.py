from piliko import *
import math

# the successive numbers of this intial spread input 
# will create numerators and denominators that are all perfect squares.

# note that 9/25 is the square of 3 over the square of 5.... the leg and
# hypoteneuse of a pythagorean triple.

sp=spread_polynomial
maxn=15
print 's(s,n) -> result numerator, denominator, dnm-num, sqrt(numerator), sqrt(denominator), sqrt(dnm-num)'
starts = Fraction(9,25)
for n in range(0,maxn):
	s = sp(n,starts)
	num = s.numerator
	dnm = s.denominator
	p = dnm-num
	print 'S(s=',starts,'n=',n,')',num,dnm,p,math.sqrt(num),math.sqrt(dnm),math.sqrt(p)
print
