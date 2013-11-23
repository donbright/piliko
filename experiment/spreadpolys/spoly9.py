from piliko import *
import math

# the successive numbers of this intial spread input 
# will create numerators and denominators that are all perfect squares.

# note that 9/25 is the square of 3 over the square of 5.... the leg and
# hypoteneuse of a pythagorean triple.

sp=spread_polynomial
maxn=15
x,y=0,0
for n in range(0,maxn):
	s = sp(n,Fraction(9,25))
	num = s.numerator
	dnm = s.denominator
	p = dnm-num
	nx=Fraction(num,dnm)
	ny=Fraction(p,dnm)
	diff=blue_quadrance_coordinates(nx,ny,x,y)
	#print num,dnm,p,math.sqrt(num),math.sqrt(dnm),math.sqrt(p)
	x,y=nx,ny
	print float(diff)
print
