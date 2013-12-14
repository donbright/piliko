from piliko import *
import math

# attempt generate somewhat regularly spaced rational points on a 
# circle. using spread polynomials. 
#
# now technically, you cannot go all the way around the circle using 
# exactly regularly spaced rational points. look at the regular polygons 
# - the points are irrational coordinates. however, can we approximate 
# regularity while using rational points?

# well. you can do pretty well.

# we have chosen the initial spread input to the spread 
# polynomial function such that all subsequent spreads will be a perfect 
# square. therefore we are only taking rational square roots. in theory. 
#
# in reality the implementation has some problems... its using 
# Babylonian square root finder which is not guaranteed to find the root 
# in a reasonable amount of time , especially for huge BigInts. . . and 
# as in any recursive rational arithmetic, we are quickly getting huge 
# BigInts when finding spreads with the spread polynomial. as you 
# continue with the polynomials, the digits in the rationals rises 
# exponentially so it even gets slow during calculation.
#
# so... we only draw 1/8th of the circle, in other words, 1/2 of the 
# first quadrant.... from spread 0 to roughly spread 1/2.
# then we 'flip'/'mirror' the coordinates to fill out the rest of the circle.
#

# however, this doesnt completely make the digit-size small. we still end up
# with x,y of roughly 52 bits in the final point. it may be possible to
# generate other sequences of points that approximate regularity well but
# use fewer bits. 
#
# on the other hand, perhaps there is some inherent fact of the universe 
# that the more regular the 'spread', the more digits the rational 
# points will require?

#
# the amount of the circle we draw at first, is depending on the
# number of iterations we go through in the spread polynomial.
# its edited by hand as 'maxn1'.
#

# see also spreadpoly8.py

def sqr(x): return x*x
def blueq(x,y): return sqr(x)+sqr(y)
def redq(x,y): return sqr(x)-sqr(y)
def greenq(x,y): return 2*x*y
sp=spread_polynomial
maxn1=9
xs,ys=[0],[0]
for i in range(0,maxn1):
	# note - you can find interesting starting spread using parts of 
	# the Stern Diatomic Sequence - see 'pythtrip_stern.py'
	# theres also some formulas you can use... not handy to me at 
	# the moment
	s = sp(i,Fraction(21*21,221*221))
	#s = sp(i,Fraction(19*19,181*181))
	# starting spread: y^2 / hypoteneuse^2
	# must be two parts of a pythagorean triple
	num = s.numerator
	dnm = s.denominator
	print ' spoly('+str(i)+',s)->',
	nx,nr=math.sqrt(abs(num)),math.sqrt(abs(dnm))
	print num,'/',dnm,'sqrts:',nx,nr
	#hypoteneuse_sqr = Fraction(4,25) # must be a perfect square
	hypoteneuse_q = Fraction(4096,1) # must be a perfect square
	y = perfect_square_root( hypoteneuse_q * s )
	x = perfect_square_root( hypoteneuse_q * ( 1-s ) )
	print x,y,float(x),float(y)
	print x.numerator.bit_length(),'bits'
	xs += [x]
	ys += [y]

	xs += [-x]
	ys += [y]
	xs += [x]
	ys += [-y]
	xs += [-x]
	ys += [-y]

	xs += [y]
	ys += [x]
	xs += [-y]
	ys += [x]
	xs += [y]
	ys += [-x]
	xs += [-y]
	ys += [-x]

for i in range(len(xs)):
	x,y = xs[i],ys[i]
	print x*x+y*y, '<-bq x,y:',x,y
plot_points(xs,ys)
plotshow()
