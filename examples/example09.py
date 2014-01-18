from piliko import *

print '\nexample 9\n'
a,b = vector(4,1),vector(2,3)
print 'vector a',a
print 'vector b',b
bv = bivector( a, b )
print 'bivector(a,a):', bivector(a,a)
print 'bivector(a,b):', bivector(a,b)
print 'bivector(b,a):', bivector(b,a)
print 'bivector(-a,-b):', bivector(-a,-b)
print 'bivector(-b,-a):', bivector(-b,-a)
print 'bv = bivector(a,b)'
print 'bv * 5 ' , bv * 5
print '5 * bv ' , 5 * bv
print '0 * bv', 0 * bv
print ''

e1,e2 = vector( 0, 1 ), vector( 1, 0 )
print 'basis vectors e1, e2:', e1, e2
e = bivector( e1, e2 )
print 'basic bivector ev = bivector(e1,e2): (aka unit bivector)', e
a = 2 * e1 + 5 * e2
b = 3 * e1 + 1 * e2
print 'vector a = 2*e1 + 5*e2 ', a
print 'vector b = 3*e1 + 1*e2 ', b
bv = bivector ( a, b )
print 'det a,b', determinant(a, b)
print 'bv = bivector( a,b )', bv
print 'bv is a multiple of e?'
multiple = bv.value() / e.value()
print 'bv.value = ', multiple, ' * e.value '
