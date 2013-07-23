from piliko import *

# line equation -> ax+by+c = 0 
l1 = line(1,2,1)
l2 = line(3,2,5)
l3 = line(4,2,3)

print 'lines l1, l2, l3:', l1, l2, l3

s12 = spread( l1, l2 )
s23 = spread( l2, l3 )
s13 = spread( l1, l3 )

print 'spreads s12, s23, s13:', s12, s23, s13

t1 = triangle( l1, l2, l3 )

print 'triangle of l1, l2, l3:', t1

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

qls0 = lsquadrance( ls0 )
qls1 = lsquadrance( ls1 )
qls2 = lsquadrance( ls2 )

print 'quadrances of linesegs ls0, ls1, ls2', qls0, qls1, qls2

