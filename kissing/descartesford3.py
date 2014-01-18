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
	if k4a==0:
		print '0:',k4a,k4b,z4k4a
	else:
		z4a = z4k4a / k4a
		p1 = point(z4a.x,z4a.y)
	if k4b==0:
		print '0:',k4a,k4b,z4k4b
	else:
		z4b = z4k4b / k4b
		p2 = point(z4b.x,z4b.y)
	return p1,p2

def descartes_kissing_circles(c1,c2,c3):
	p4,p5=descartes_kissing_centers(c1,c2,c3)
	k1,k2,k3,k4,k5=descartes_kissing_curvatures(c1,c2,c3)
	c4,c5=None,None
	if k4!=0: c4 = circle( p4,sqr(Fraction(1,k4)) )
	if k5!=0: c5 = circle( p5,sqr(Fraction(1,k5)) )
	return c4,c5

circs =[]
for j in range(0,3):
	fordcircs = ford_circles(j)
	for i in range(0,len(fordcircs)-2):
       		a,b,c = fordcircs[i],fordcircs[i+1],fordcircs[i+2]
		if a.center.x.numerator+c.center.x.numerator!=b.center.x.numerator: continue 
		circs += [descartes_kissing_circles(a,b,c)[0]]
print circs
plot_circles( circs + ford_circles(3) )
plotshow()

	
