from piliko import *
import math

# the successive numbers of this intial spread input 
# will create numerators and denominators that are all perfect squares.

# note that 9/25 is the square of 3 over the square of 5.... the leg and
# hypoteneuse of a pythagorean triple.

sp=spread_polynomial
maxn=10
for n in range(0,maxn):
	s = sp(n,Fraction(9,25))
	num = s.numerator
	dnm = s.denominator
	print num,dnm,math.sqrt(num),math.sqrt(dnm)
print
