from piliko import *

############## square root 
### the square root of a rational number is often irrational. 
### we can find a rational approximation, thanks to the ancient Iraqis / 
### Babylonians / Mesopotamians.
### 
### there is also a 'is perfect square?' test function
###
### we ignore negative roots here. and imaginary roots.

# return [r1, r2] such that the sqrt(s) is guaranteed to be between them
def square_root_rough_bounds_int( s ):
	bitlength = int(Fraction(s.bit_length()-1,2))
	guess = 1
	for i in range(0,bitlength): guess *= 2
	return guess,guess*2

# return rational approximation of square root using Babylonian's method
# iterate for maxdepth iterations or until answer>maxbits. 
def babylonian_square_root_int( s, maxdepth=10, maxbits=2048, firstguess=1 ):
	guesses=[firstguess]
	breason = 'max depth reached'
	for i in range(1,maxdepth):
		lastguess = guesses[i-1]
		newguess = avg(lastguess,Fraction(s,lastguess))
		if lastguess==newguess: break
		if sqr(long(newguess))==s: # perfect square
			breason='found perfect square'
			guesses += [ long(newguess) ]
			break
		# prevent digit ballooning causing Big Int freezing
		if (newguess.numerator.bit_length()+newguess.denominator.bit_length())>maxbits:
			breason='bitlength too large:' + str(newguess.numerator.bit_length()+newguess.denominator.bit_length())
			break
		guesses += [newguess]
	debug=0
	if debug>0:
		print 'guesses for root of ',s,float(s)
		for g in guesses: print ' ',g,float(g),float(g*g)
		print 'break reason:',breason
	return guesses[-1]

def babylonian_square_root_for_fraction( s, maxdepth=10,maxbits=2048 ):
	lo_n,hi_n = square_root_rough_bounds_int( s.numerator )
	lo_d,hi_d = square_root_rough_bounds_int( s.denominator )
	numer=babylonian_square_root_int( s.numerator, maxdepth, maxbits, lo_n )
	denom=babylonian_square_root_int( s.denominator, maxdepth, maxbits, lo_d )
	return Fraction(numer,denom)

def is_perfect_square(s):
	x = babylonian_square_root(s)
	if x*x==s: return True
	return False

# return rational approximation of square root of s
def babylonian_square_root( s, maxdepth=10, maxbits=2048 ):
	if s<0: raise Exception('cant do sqrt(-1). try "complex" type')
	if checktype(int,s) or checktype(long,s):
		lo,hi = square_root_rough_bounds_int( s )
		return babylonian_square_root_int( s, maxdepth, maxbits,firstguess=lo )
	elif checktype(Fraction,s):
		return babylonian_square_root_for_fraction( Fraction(s),maxdepth,maxbits )
	else: raise Exception('bad type')

def quadratic_formula( a, b, c ):
	term1 = babylonian_square_root( sqr(b) - 4 * a * c )
	return Fraction(-b + term1,2*a), Fraction(-b - term1, 2*a )

def perfect_square_root( s, maxbits=4096 ):
	root = babylonian_square_root(s,maxdepth=20,maxbits=maxbits)
	if root*root==s: return root
	else: raise Exception('Cant find perfect root of '+str(s)+'. Please modify algorithm to guarantee perfect squares or to use less bits')
