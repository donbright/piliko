from piliko import *

print 'example 1'

# line equation -> ax+by+c = 0 
l1 = line(0,1,0)
l2 = line(1,0,0)
l3 = line(1,1,-1)

print 'lines l1, l2, l3:', l1, l2, l3

s12 = spread( l1, l2 )
s23 = spread( l2, l3 )
s13 = spread( l1, l3 )

print 'spreads s12, s23, s13:', s12, s23, s13

t1 = triangle( l1, l2, l3 )

print 'triangle t1 of l1, l2, l3:', t1
print 'cross law lhs for t1: ', cross_law_lhs( t1 )
print 'cross law rhs for t1: ', cross_law_rhs( t1 )
print 'spread law for t1:', spread_law( t1 )
print 'triple spread lhs for t1: ', triple_spread_lhs( t1 )
print 'triple spread rhs for t1: ', triple_spread_rhs( t1 )
print 'pythagoras lhs:', pythagoras_lhs( t1 ) , 'rhs:', pythagoras_rhs( t1 )


