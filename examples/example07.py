from piliko import *
print '\nexample7'
print 'lines: ax+by+c = 0, so <a:b:c> = line notation'
p0,p1,p2,p3 = point(1,0),point(4,0),point(1,4),point(5,4)
print 'points p0,p1,p2,p3:',p0,p1,p2,p3
print 'p0,p1,p2 collinear?',collinear(p0,p1,p2)
line0 = line( p0, p1 )
line1 = line( p0, p2 )
line2 = line( p2, p3 )
print 'line, l0, meeting p0, p1:', line0
print 'line, l1, meeting p0, p2:', line1
print 'line, l2, meeting p2, p3:', line2
print 'meet l0,l1:', meet( line0, line1 )
print 'meet l0,l2:', meet( line0, line2 )
print 'meet of l0 and p0?', meet( line0, p0 ), "p1?", meet( line0, p1 )
p4, p5, p6 = point(3,3), point(4,5), point(5,7)
print 'p4, p5, p6:', p4, p5, p6, 'collinear?', collinear(p4,p5,p6)
	
p=point
a,b,c,d=p(1,0),p(4,0),p(6,0),p(11,0)
print 'points a,b,c,d:',a,b,c,d
print 'squared cross ratio( a,b,c,d ): ',squared_cross_ratio(a,b,c,d)
a,b,c,d=p(1,1),p(4,4),p(6,6),p(11,11)
print 'points a,b,c,d:',a,b,c,d
print 'squared cross ratio( a,b,c,d ): ',squared_cross_ratio(a,b,c,d)
a,b,c,d=p(0,1),p(0,4),p(0,6),p(0,11)
print 'points a,b,c,d:',a,b,c,d
print 'squared cross ratio( a,b,c,d ): ',squared_cross_ratio(a,b,c,d)
e = p(4,3)
l0,l1,l2,l3 = line(a,e), line(b,e), line(c,e), line(d,e)
import random
l4 = line(random.randint(-10,10),random.randint(-10,10),random.randint(-10,10))
m0,m1,m2,m3 = meet(l4,l0), meet(l4,l1), meet(l4,l2), meet(l4,l3)
print 'points m0,m1,m2,m3:',m0,m1,m2,m3
print 'squared cross ratio ( m0,m1,m2,m3 ):',squared_cross_ratio(m0,m1,m2,m3)
print 'collinear?',collinear(p1,p2,p3,p4)
print 'harmonic range?:', is_harmonic_range_points( m0,m1,m2,m3 )

print
p1,p2,p3,p4 = point(0,0),point(Fraction(1,2),0),point(Fraction(1,3),0),point(1,0)
print 'p1,p2,p3,p4',p1,p2,p3,p4
print 'squared cross ratio:', squared_cross_ratio( p1, p2, p3, p4 )
print 'collinear?',collinear(p1,p2,p3,p4)
print 'harmonic range?:', is_harmonic_range_points( p1, p2, p3, p4 )
