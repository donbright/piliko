from piliko import *
###### anti-symmetric polynomials

# special polynomials used in many areas of geometry, especially 
# chromogeometry.
# 
# an anti-symmetrical polynomial is generated from an 'input monomial' 
# by transposing subscripts/indexes of variables
#
# example:
# input 'x1y2' returns six terms, by transposing '1' and '2' in a pattern:
# +x1y2 -x1y3 +x2y3 -x3y2 +x3y1 -x2y1
# 
# this particular sum is twice the signed area of the triangle of the 3 points
# x1,y1 x2,y2 x3,y3 
#
# It can be a bit confusing b/c the 'input' doesnt list x3,y3. But if 
# you get the hang of the transpositions it can help to understand. 
# Another way to think about it is to consider input monomial as 
# sort of like a 'seed' and the six-term polynomial 'grows' out of it.
# 
# The easiest function to use in this code is eval_asympoly(): You give 
# it a monomial and some values for x1,y1 x2,y2 x3,y3. It generates the 
# complete antisymmetric polynomial and plugs in the values for you into 
# the six generated terms, then sums them together and gives the 
# resulting sum.
#
# eval_asympoly( 'x1*y2', 3,4, 3,0, 1,-2 ) -> returns 20
#
# The other functions are 'helpers'


# More examples of antisymmetric polynomials:
#
# given: a monomial
#
# follow these 6 steps to generate the six terms of the antisymmetric 
# polynomial:
#
# start with the subscripts as given. 
# replace '2' with '3', and vice versa
# replace '1' with '2', and vice versa
# replace '2' with '3', and vice versa
# replace '1' with '2', and vice versa
# replace '2' with '3', and vice versa
# now assign positive and negative: like so: + - + - + -

# examples:
#
# input x1y2 returns six terms:
# +x1y2 -x1y3 +x2y3 -x3y2 +x3y1 -x2y1
#
# input x1*x1*x2*y2 returns six terms:
# +x1*x1*x2*y2 -x1*x1*x3*y3 +x2*x2*x3*y3 -x3*x3*x2*y2 +x3*x3*x1*y1 -x2*x2*x1*y1
#
# input x1*x1*x1*y1 returns six terms:
# +x1*x1*x1*y1 -x1*x1*x1*y1 +x2*x2*x2*y2 -x3*x3*x3*y3 +x3*x3*x3*y3 -x2*x2*x2*y2



# replace s1 for s2, and vice versa, in the input string s.
# example: given 'xabx','a','b' return 'xbax'
def transpose( s, s1, s2 ):
	s = s.replace(s1,'______term1______').replace(s2,'_____term2_____')
	s = s.replace('______term1______',s2).replace('_____term2_____',s1)
	return s

# given string representation of input monomial, generate a string
# with the six terms of the antisymmetric polynomial
def gen_antisymmetric_polynomial_string( s ):
	term1 = s
	term2 = transpose( term1, '2', '3' )
	term3 = transpose( term2, '1', '2' )
	term4 = transpose( term3, '2', '3' )
	term5 = transpose( term4, '1', '2' )
	term6 = transpose( term5, '2', '3' )
	#term1 = '+'+term1
	term2 = '-'+term2
	term3 = '+'+term3
	term4 = '-'+term4
	term5 = '+'+term5
	term6 = '-'+term6
	return term1+term2+term3+term4+term5+term6

# generate and calc the value of an antisymmetric polyonmial, given an 
# input monomial and some values for the input variables.
#
# first input must be a string representing a monomial python expression
# second input must be a python dictionary mapping strings to Rationals.
# example:
# dic = { 'x1': 4, 'y1': 5, 'x2': 3, 'y2': 0, 'x3': 1, 'y3': -2 }
# calc_antisymmetric_polynomial( 'x1*y2', dic )
# result: 20
def calc_antisymmetric_polynomial( monomial, vardict ):
	asp_str = gen_antisymmetric_polynomial_string( monomial )
	return eval(asp_str,{},vardict)

#### antisymmetric polynomial convenience functions

def gen_asymp_dict_from_points( p1, p2, p3 ):
	dic = {}
	dic['x1'],dic['y1']=p1.x,p1.y
	dic['x2'],dic['y2']=p2.x,p2.y
	dic['x3'],dic['y3']=p3.x,p3.y
	return dic

def gen_asymp_dict_from_triangle( t ):
	return gen_asymp_dict_from_points( t.p0, t.p1, t.p2 )

def gen_asymp_dict_from_rationals( x1,y1,x2,y2,x3,y3 ):
	p1 = point(x1,y1)
	p2 = point(x2,y2)
	p3 = point(x3,y3)
	return gen_asymp_dict_from_points( p1, p2, p3 )

def eval_asympoly_from_triangle( monomial, tri ):
	vardict = gen_asymp_dict_from_triangle( tri )
	return calc_antisymmetric_polynomial( monomial, vardict )

def eval_asympoly_from_points( monomial, p1, p2, p3 ):
	vardict = gen_asymp_dict_from_points( p1, p2, p3 )
	return calc_antisymmetric_polynomial( monomial, vardict )

def eval_asympoly_from_rationals( monomial, x1,y1,x2,y2,x3,y3 ):
	vardict = gen_asymp_dict_from_rationals( x1,y1,x2,y2,x3,y3 )
	return calc_antisymmetric_polynomial( monomial, vardict )

# easiest version to use. Examples:
# eval_asympoly('x1*y2',3,4,3,0,1,-2) -> returns 20
# p1,p2,p3 = point(3,4),point(3,0),point(1,-2) 
# eval_asympoly('x1*y2',p1,p2,p3) -> returns 20
# t = triangle(p1,p2,p3)
# eval_asympoly('x1*y2',t) -> returns 20
def eval_asympoly( *args ):
	if len(args)<2: raise Exception('need monomial, pointdata')
	if not isinstance(args[0],str):
		raise Exception('arg[0] s/b string')
	monomial = args[0]
	if checktype(triangle, args[1]):
		return eval_asympoly_from_triangle( monomial, args[1] )
	if checktype(point, args[1]) and checktype(point, args[2]):
		if checktype(point, args[3]):
			p1,p2,p3=args[1],args[2],args[3]
			return eval_asympoly_from_points( monomial, p1, p2, p3 )
	if checktype(Fraction, args[1]):
		x1,y1,x2,y2,x3,y3 = args[1],args[2],args[3],args[4],args[5],args[6]
		return eval_asympoly_from_rationals( monomial, x1,y1,x2,y2,x3,y3 )
	if checktype(int, args[1]):
		x1,y1,x2,y2,x3,y3 = args[1],args[2],args[3],args[4],args[5],args[6]
		return eval_asympoly_from_rationals( monomial, x1,y1,x2,y2,x3,y3 )
	



# fun fact
#
#              A1 A2 A3
# determinant( B1 B2 B3 )  is the antisymmetric of A1*B2*C3
#              C1 C2 C3
#
# ( A1*B2*C3-A1*B3*C2+A2*B3*C1-A3*B2*C1+A3*B1*C2-A2*B1*C3 )
