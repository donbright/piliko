from piliko import *

print
print 'example 5'
v1,v2 = vector(3,0),vector(0,4)
print 'vectors v1, v2:', v1, v2
print ' v1 + v2, v1 - v2: ', v1 + v2, v1 - v2
print ' v1 * 5/4:', v1 * Fraction(5,4)
print ' v1 perpendicular v1? ', v1.perpendicular( v1 )
print ' v1 perpendicular v2? ', v1.perpendicular( v2 )
print ' v2 perpendicular v1? ', perpendicular( v2, v1 )
print ' v1 perpendicular v1+v2? ', perpendicular( v1, v1+v2 )
print ' v1 parallel v1? ', v1.parallel( v1 )
print ' v1 parallel v2? ', v1.parallel( v2 )
print ' v1 parallel 5*v1? ', parallel( v1, 5*v1 )
print ' v1 parallel v1+v2? ', parallel( v1, v1+v2 )
v3 = v2 - v1
print 'vector v3 = v2-v1: ', v3
lhs = quadrance( v1 ) + quadrance( v2 )
rhs = quadrance( v3 )
print 'v1 dot v2, v2 dot v3, v1 dot 5*v1:', v1.dot(v2), v2.dot(v3), v1.dot(5*v1)
print 'v1 dot (v2+v3), (v1 dot v2)+(v1 dot v3):', v1.dot(v2+v3), v1.dot(v2) + v1.dot(v3)
print ' pythagoras: Q(v1)+Q(v2)=Q(v3)?: lhs:', lhs, 'rhs:',rhs
v4 = vector( -5, 0 )
v5 = 3 * v4
v6 = v5 - v4
print 'vector v4, v5, and v6=v5-v4:', v4, v5, v6
lhs = sqr( quadrance( v4 ) + quadrance( v5 ) + quadrance( v6 ) )
rhs = 2*(sqr(quadrance(v4))+sqr(quadrance(v5))+sqr(quadrance(v6)))
print ' triplequad for v4,v5,v6 : lhs:', lhs, 'rhs:',rhs

print 'spread( v1, v1 ):', spread( v1, v1 )
print 'spread( v2, v1 ):', spread( v2, v1 )
print 'spread( v2, 5*v1 ):', spread( v2, 5*v1 )
print 'spread( v1, v2 ):', spread( v1, v2 )
print 'spread( v1, v3 ):', spread( v1, v3 )
print 'spread( v1, 5*v3 ):', spread( v1, 5*v3 )
print 'spread( v2, v3 ):', spread( v2, v3 )
print 'spread( 100*v2, -20*v2 ):', spread( 100*v2, -20*v2 )
 
print 'quadrance v1 == v1 dot v1?', quadrance(v1), '=?=', v1.dot(v1)

