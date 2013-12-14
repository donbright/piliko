from piliko import *

# given 3 kissing circles, find curvatures of 2 new kissing circles
def descartes_kissing_curvatures(c1,c2,c3):
	# k4 = k1+k2+k3+/- 2 * sqrt( k1k2 + k2k3 + k3k1 )
	r1 = babylonian_square_root( c1.radial_quadrance )
	r2 = babylonian_square_root( c2.radial_quadrance )
	r3 = babylonian_square_root( c3.radial_quadrance )
	k1 = Fraction(1, r1)
	k2 = Fraction(1, r2)
	k3 = Fraction(1, r3)
	k4a = k1+k2+k3+2*babylonian_square_root(k1*k2+k2*k3+k3*k1)
	k4b = k1+k2+k3-2*babylonian_square_root(k1*k2+k2*k3+k3*k1)
	return k1,k2,k3,k4a,k4b

# given 3 kissing circles, find the centers of 2 new kissing circles
def descartes_kissing_centers(c1,c2,c3):
	# z4k4 = k1z1+k2z2+k3z3+/- 2 * sqrt( k1z1k2z2 + k2z2k3z3 + k3z3k1z1 )
	k1,k2,k3,k4a,k4b = descartes_kissing_curvatures(c1,c2,c3)
	#print k1,k2,k3,k4a,k4b,c1.center,c2.center,c3.center
	z1 = complex(c1.center.x,c1.center.y)
	z2 = complex(c2.center.x,c2.center.y)
	z3 = complex(c3.center.x,c3.center.y)
	term0 = k1*z1+k2*z2+k3*z3
	term1 = k1*z1*k2*z2 + k2*z2*k3*z3 + k3*z3*k1*z1
	#print term0,term1
	z4k4a = term0 + 2*term1.sqrt()[0]
	z4k4b = term0 - 2*term1.sqrt()[0]
	p1,p2 = None,None
	print 'term0',term0,', 2 * term1 sqrt ',2*term1.sqrt()[0]
	if k4a==0:
		print '0: k4a, z4k4a, k4b',k4a,z4k4a,k4b
		print '   term0/k4b',term0/k4b,', 2 * term1 sqrt/k4b',2*term1.sqrt()[0]/k4b
		xc = term0.x/k4b
		yc = term0.y/k4b
		xp=term0.x/k4b+2*term1.sqrt()[0].x/k4b
		yp=term0.y/k4b+2*term1.sqrt()[0].y/k4b
		xm=term0.x/k4b-2*term1.sqrt()[0].x/k4b
		ym=term0.y/k4b-2*term1.sqrt()[0].y/k4b
		plot_triangles(triangle(xc,yc,xp,yp,xm,ym))
		print triangle(xc,yc,xp,yp,xm,ym)
		plot_points([xc,xp,xm],[yc,yp,ym])
		#p1 = point(term0.x,term0.y)
		p1 = point(xp,yp)
	else:
		z4a = z4k4a / k4a
		p1 = point(z4a.x,z4a.y)
	if k4b==0:
		print '0: k4b, z4k4b, k4a',k4b,z4k4b,k4a
		print '   term0/k4a',term0/k4a,', 2 * term1 sqrt/k4a',2*term1.sqrt()[0]/k4a
		xc = term0.x/k4a
		yc = term0.y/k4a
		xp=term0.x/k4a+2*term1.sqrt()[0].x/k4a
		yp=term0.y/k4a+2*term1.sqrt()[0].y/k4a
		xm=term0.x/k4a-2*term1.sqrt()[0].x/k4a
		ym=term0.y/k4a-2*term1.sqrt()[0].y/k4a
		plot_triangles(triangle(xc,yc,xp,yp,xm,ym))
		print triangle(xc,yc,xp,yp,xm,ym)
		plot_points([xc,xp,xm],[yc,yp,ym])
		p2 = point(xp,yp)
		#p2 = point(xp,yp)
	else:
		z4b = z4k4b / k4b
		p2 = point(z4b.x,z4b.y)
	return p1,p2

def descartes_kissing_circles(c1,c2,c3):
	k1,k2,k3,k4,k5=descartes_kissing_curvatures(c1,c2,c3)
	p4,p5=descartes_kissing_centers(c1,c2,c3)
	c4,c5=None,None
	if k4 == 0: c4 = circle(p4,1)
	else: c4 = circle( p4,sqr(Fraction(1,k4)) )
	if k5 == 0: c5 = circle(p5,1)
	else: c5 = circle( p5,sqr(Fraction(1,k5)) )
	return c4,c5


ox,oy=11,1

circs =[]

circle1 = circle( 1+Fraction(1,2),1+0,Fraction(1,4) )
circle3 = circle( 1+Fraction(1,8),1+Fraction(1,2),Fraction(1,64) )
circle2 = circle( 1+Fraction(1,2),1+1,Fraction(1,4) )

circle1 = circle( Fraction(0,1),5+Fraction(1,2),Fraction(1,4) )
circle3 = circle( Fraction(1,2),5+Fraction(1,8),Fraction(1,64) )
circle2 = circle( Fraction(1,3),5+Fraction(1,18),Fraction(1,18*18) )

circle1 = circle( Fraction(0,1),7+Fraction(1,2),Fraction(1,4) )
circle3 = circle( Fraction(1,2),7+Fraction(1,8),Fraction(1,64) )
circle2 = circle( Fraction(1,3),7+Fraction(1,18),Fraction(1,18*18) )

#circle1 = circle( Fraction(0,1),7+Fraction(1,2),Fraction(1,4) )
#circle3 = circle( Fraction(1,4),7+Fraction(1,32),Fraction(1,32*32) )
#circle2 = circle( Fraction(1,3),7+Fraction(1,18),Fraction(1,18*18) )

#circle1 = circle( 5+Fraction(1,2),1+Fraction(0,1),Fraction(1,4) )
#circle3 = circle( 5+Fraction(1,8),1+Fraction(1,2),Fraction(1,64) )
#circle2 = circle( 5+Fraction(1,18),1+Fraction(1,3),Fraction(1,18*18) )

#circle1 = circle( 7+Fraction(1,2),3+Fraction(0,1),Fraction(1,4) )
#circle3 = circle( 7+Fraction(1,8),3+Fraction(1,2),Fraction(1,64) )
#circle2 = circle( 7+Fraction(1,18),3+Fraction(1,3),Fraction(1,18*18) )

circle1 = circle( ox+Fraction(-3,10),oy+Fraction( 4,10),Fraction(1,4) )
circle2 = circle( ox+Fraction(13,40),oy+Fraction(16,40),Fraction(1,64) )
circle3 = circle( ox+Fraction(5,10),oy+Fraction(10,10),Fraction(1,4) )

circs = [circle1,circle2,circle3]
kiss1,kiss2 = descartes_kissing_circles( circle1, circle2, circle3 )
print 'kiss 1,2,3',circs
print 'kissing 4,5:',kiss1,kiss2
plot_points( circle1.center,circle2.center,circle3.center,kiss1.center,kiss2.center)
plot_circles( circs+[kiss1,kiss2] )
plot_lineseg(lineseg(ox+0,oy+0,ox+Fraction(4,5),oy+Fraction(3,5)))
print line(ox+0,oy+0,ox+Fraction(4,5),oy+Fraction(3,5))
plotshow()

	
