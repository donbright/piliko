from piliko import *

print 'anti-symmetric polynomials'
ex1 = gen_antisymmetric_polynomial_string('x1*y2')
ex2 = gen_antisymmetric_polynomial_string('x1*x1*x2*y2')
ex3 = gen_antisymmetric_polynomial_string('x1*x1*x1*y1')

print 'input monomial: x1*y2        output anti-symmetric polynomial:'
print ' ',ex1
print
print 'input monomial: x1*x1*x2*y2  output anti-symmetric polynomial:'
print ' ',ex2
print
print 'input monomial: x1*x1*x1*y1  output anti-symmetric polynomial:'
print ' ',ex3
print

def test_asym(asymstring,p1,p2,p3):
	print
	print 'test ',asymstring,
	print 'p1,p2,p3:',p1,p2,p3 
	x1,y1,x2,y2,x3,y3=p1[0],p1[1],p2[0],p2[1],p3[0],p3[1] 
	asp1s = gen_antisymmetric_polynomial_string('x1*y2') 
	print 'antisym(x1*y2):',asp1s 
	print 'eval with x1,y1,x2,y2,x3,y3:',x1,y1,x2,y2,x3,y3,'. result:',eval(asp1s) 
	print 'eval asym(x1y2) squared:',sqr(eval(asp1s))
	print 'quadrea p1 p2 p3:', quadrea(p1, p2, p3)
	print ' antisym "x1y2" should be twice the area of triangle p1,p2,p3'
	print ' quadrea should be sixteen times the squared area of triangle p1,p2,p3'
	print ' therefore asym(x1y2)^2:quadrea should be 1:4 ... actual ratio->',
	ratio = Fraction(eval(asp1s)*eval(asp1s),quadrea(p1, p2, p3))
	print ratio.numerator,':',ratio.denominator

p1,p2,p3=point(0,0),point(4,0),point(4,3)
test_asym('x1*y2',p1,p2,p3)

print 'test eval_asympoly function'
print " eval_asympoly('x1*y2',p1,p2,p3): ",
print eval_asympoly('x1*y2',p1,p2,p3)

