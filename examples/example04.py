from piliko import *

print
print 'example 4'
p0 = point(0,0)
p1 = point(3,4)
print 'points p0, p1', p0, p1
rq = red_quadrance( p0, p1 )
gq = green_quadrance( p0, p1 )
bq = blue_quadrance( p0, p1 )
print 'red, green, blue quadrances: ', rq, gq, bq
cql = colored_quadrance_lhs( p0, p1 )
cqr = colored_quadrance_rhs( p0, p1 )
print 'colored quadrance theorem (bq^2=rq^2+gq^2) lhs: ', cql, ' rhs: ', cqr
