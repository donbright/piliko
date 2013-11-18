from piliko import *

# these are not regression tests nor unit tests.
# they are just plain old examples of the code

def example1():
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


def example2():
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

def example3():
	print
	print 'example 3'

	l0 = line(1,-2,3)
	l1 = line(4,-3,7)
	print 'lines l0,l1', l0, l1
	print 'blue spread: ', blue_spread( l0, l1 )
	print 'red spread: ', red_spread( l0, l1 )
	print 'green spread: ', green_spread( l0, l1 )
	csl = colored_spread_lhs( l0, l1 )
	csr = colored_spread_rhs( l0, l1 )
	print 'colored spread theorem (1/g+1/b+1/r=2): lhs:', csl, ' rhs: ', csr

def example4():
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


def example5():
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

def example6():
	print
	print 'example 6'
	print 'determinant, with vectors as input-rows'
	det = determinant
	va,vb = vector(3,1),vector(4,5)
	print 'va, vb, determinant(va,vb), det(vb,va):',va,vb,det(va,vb),det(vb,va)	
	v1,v2,v3=vector(3,0,0),vector(0,4,0),vector(0,0,5)
	print 'v1,v2,v3:',v1,v2,v3
	print 'determinant of ( v1,v2,v3 ):',det(v1,v2,v3)

	v4,v5=vector(1,3),vector(-1,4)	
	print 'v4,v5,det(v4,v5),det(v4,v4+v5)',v4,v5,det(v4,v5),det(v4,v5+v4*3)	
	
	print 'solid spread of v1,v2,v3:',solid_spread(v1,v2,v3)
	print 'solid spread of v1,v2,(3,2,-2):',solid_spread(v1,v2,vector(3,2,-2))

def example7():
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
	print 'harmonic range?:', is_harmonic_range_points( m0,m1,m2,m3 )

	print
        p1,p2,p3,p4 = point(0,0),point(Fraction(1,2),0),point(Fraction(1,3),0),point(1,0)
	print 'p1,p2,p3,p4',p1,p2,p3,p4
	print 'squared cross ratio:', squared_cross_ratio( p1, p2, p3, p4 )
	print 'harmonic range?:', is_harmonic_range_points( p1, p2, p3, p4 )


def example8():

	print '\nexample8'

	p0,p1,p2=point(0,0),point(1,0),point(0,1)

	print 'p0,p1,p2',p0,p1,p2

	A = quadria( p0, p1, p2 )

	print 'quadria of p0, p1, p2: ', A


def example9():
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

def example10():
	print '\n\nexample 10'
        a1=projective_point(1,0)
        a2=projective_point(2,3)
        a3=projective_point(4,-1)
        a4=projective_point(3,5)
        
        f=blue_projective_form
        q12=projective_quadrance(a1,a2,f)
        q23=projective_quadrance(a2,a3,f)
        q34=projective_quadrance(a3,a4,f)
        q14=projective_quadrance(a1,a4,f)
        
        print 'projective points a1, a2, a3, a4:',a1,a2,a3,a4
        print 'projective form: ', f
        print 'projective quadrances:',q12,q23,q34,q14

	print 'blue, red, and green projective quadrance between a2 and a3:'
	qb = projective_quadrance(a2,a3,blue_projective_form)
	qg = projective_quadrance(a2,a3,green_projective_form)
	qr = projective_quadrance(a2,a3,red_projective_form)
	print 'qb, qg, qr', qb, qg, qr
	print 'colored projective quadrance theorem 1/qb+1/qg+1/qr=2'
	print 'lhs,rhs: ',Fraction(1,qb)+Fraction(1,qg)+Fraction(1,qr),',',2
	print ''
	print 'projective point perpendiculars for a1. blue, red, green'
	a1pb = ppoint_perpendicular( a1, color='blue' )
	a1pr = ppoint_perpendicular( a1, color='red' )
	a1pg = ppoint_perpendicular( a1, color='green' )
	print a1pb, a1pr, a1pg
	print 'projective point perpendiculars for a2. blue, red, green'
	a2pb = ppoint_perpendicular( a2, color='blue' )
	a2pr = ppoint_perpendicular( a2, color='red' )
	a2pg = ppoint_perpendicular( a2, color='green' )
	print a2pb, a2pr, a2pg
	print 'theorem: colored p-quadrance of colored ppoint perpendiculars'
	print ' qblue(  ppoint_red_perp,   ppoint_green_perp ) = 1'
	print ' qred(   ppoint_green_perp, ppoint_blue_perp  ) = 1'
	print ' qgreen( ppoint_blue_perp,  ppoint_red_perp   ) = 1'
	print ' test with a2', a2, ' and a2 perps', a2pb, a2pr, a2pg, ':',
	print projective_quadrance_blue( a2pg, a2pr ),
	print projective_quadrance_red( a2pb, a2pg ),
	print projective_quadrance_green( a2pb, a2pr )

def example11():
	print '\n\nexample 11'

	print 'spread_polynomials'
	sp=spread_polynomial
	maxn = 8

	print 's=0, n=0,1,2,...'
	print 'spoly(n,s):',
	for n in range(0,maxn): print sp(n,0),
	print

	print 's=1, n=0,1,2,...'
	print 'spoly(n,s):',
	for n in range(0,maxn): print sp(n,1),
	print

	print 's=1/2, n=0,1,2,...'
	print 'spoly(n,s):',
	for n in range(0,maxn): print sp(n,Fraction(1,2)),
	print

	print 's=1/4, n=0,1,2,...'
	print 'spoly(n,s):',
	for n in range(0,maxn): print sp(n,Fraction(1,4)),
	print

	print 's=3/4, n=0,1,2,...'
	print 'spoly(n,s):',
	for n in range(0,maxn): print sp(n,Fraction(3,4)),
	print

	print 's=1/3, n=0,1,2,...'
	print 'spoly(n,s):',
	for n in range(0,maxn): print sp(n,Fraction(1,3)),
	print

	print 's=16/25, n=0,1,2,...'
	print 'spoly(n,s):',
	for n in range(0,maxn): print sp(n,Fraction(16,25)),
	print

	print 's=5, n=0,1,2,...'
	print 'spoly(n,s):',
	for n in range(0,maxn): print sp(n,Fraction(5,1)),
	print

examples = [example1,example2,example3,example4,example5,example6,example7,
	example8, example9, example10,example11 ]

for i in examples:
	i()

