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

print
print 'example 2'

p0 = point( 0, 0 )
p1 = point( 3, 0 )
p2 = point( 3, 4 )

print 'points p0, p1, p2:', p0, p1, p2

ls0 = lineseg( p0, p1 )
ls1 = lineseg( p1, p2 )
ls2 = lineseg( p2, p0 )

print 'linesegs ls0, ls1, ls2:', ls0, ls1, ls2

q10 = quadrance( p1, p0 )
q21 = quadrance( p2, p1 )
q02 = quadrance( p0, p2 )

print 'quadrances between points p0, p1, p2:', q10, q21, q02

qls0 = quadrance( ls0 )
qls1 = quadrance( ls1 )
qls2 = quadrance( ls2 )

print 'quadrances of linesegs ls0, ls1, ls2:', qls0, qls1, qls2

print
print 'example 3'


l0 = line(1,-2,3)
l1 = line(4,-3,7)
print 'lines l0,l1', l0, l1
print 'blue spread: ', blue_spread( l0, l1 )
print 'red spread: ', red_spread( l0, l1 )
print 'green spread: ', green_spread( l0, l1 )


print
print 'example 4'
p0 = point(0,0)
p1 = point(3,4)
print 'points p0, p1', p0, p1
rq = red_quadrance( p0, p1 )
gq = green_quadrance( p0, p1 )
bq = blue_quadrance( p0, p1 )
print 'red, green, blue quadrances: ', rq, gq, bq
print 'redq squared + greenq squared:' , rq*rq + gq*gq , ' blueq squared: ', bq*bq
