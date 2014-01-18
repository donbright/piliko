from piliko import *

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
