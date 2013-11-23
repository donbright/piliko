from piliko import *
import math

# the successive numbers of this intial spread input 
# will create numerators and denominators that are all perfect squares.

# note that 25/169 is the square of 5 over the square of 13.... the leg and
# hypoteneuse of a pythagorean triple.

# it works with 3/5 ^ 2 as well. 
sp=spread_polynomial
maxn=15
for n in range(0,maxn):
	s = sp(n,Fraction(25,169))
	num = s.numerator
	dnm = s.denominator
	print num,dnm,math.sqrt(num),math.sqrt(dnm)
print
