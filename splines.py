# given three points, find the equation of the Conic that fits them. 
# (also given a 'weight' for the curve)
# From Rob Johnson's https://dl.dropboxusercontent.com/u/78279253/splines.pdf
# (by law Apple cannot copyright nor patent a math equation)
from sympy import *
from fractions import Fraction
x,y=symbols(['x','y'])

def find_equation(p1,p2,p3,weight):
	x1,y1,x2,y2,x3,y3=p1[0],p1[1],p2[0],p2[1],p3[0],p3[1]
	M=Matrix([[x1,x2,x3],[y1,y2,y3],[1,1,1]])
	cof=M.cofactorMatrix()
	u,v,w=cof.col(0),cof.col(1),cof.col(2)
	Q = weight*( u*w.transpose()+w*u.transpose() ) - v*v.transpose()
	eq = Q[0,0]*x**2+(Q[0,1]+Q[1,0])*x*y+Q[1,1]*y**2
	eq += (Q[2,0]+Q[0,2])*x+(Q[2,1]+Q[1,2])*y+Q[2,2]
	return eq

testpts = [[1,1],[2,3],[4,5]]
testeq = -12*x**2 + 18*x*y + 10*x - 7*y**2 - 6*y - 3
eq = find_equation(testpts[0],testpts[1],testpts[2],Fraction(1,2))
print 'given points',testpts,'\nconic equation is',eq
if (eq == testeq): print 'this matches the expected result'
else: print 'not matching expected result... test failed'
