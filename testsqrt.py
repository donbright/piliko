from piliko import *

# test babylonian square root bounds

def test(num):
	print '---'
	print 'estimate sqrt',num
	if not isinstance(num, Fraction):
		print 'rough low,high:',square_root_rough_bounds_int( num )
	root = babylonian_square_root( num )
	print 'root',root,'sqr of root:',sqr(root),'sqr of root:',float(sqr(root))

test( 1111831 )
test( Fraction(1111831,234894) )
test( Fraction(10244*10244,34709*34709) )
test(Fraction(9,4))
test(Fraction(9,3))
test(Fraction(1,5))
test(5)
test(-5)
