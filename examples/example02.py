from piliko import *

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

