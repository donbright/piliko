#
# From Append B of Divine Proportions by Norman J Wildberger
#
# x,y,z satisfying
# (x+y+z)^2=2(x^2+y^2+z^2)+4xyz
#
# i.e. x,y,z are 'spread triples'. 
#
# Strategy. 
# Spread triples are the spreads of triangles. 
from pytools import generate_permutations
from fractions import Fraction
from random import randint
class point2d:
	def __init__( self,x,y ): self.x,self.y=x,y
def sqr(x): return x*x
def blueq(p1,p2): return sqr(p2.x-p1.x)+sqr(p2.y-p1.y)
depth=50
for x in range(0,depth):
	for y in range(0,depth):
		p1=point2d(x,y)
		p2=point2d(0,depth)
		p3=point2d(0,0)
		q1,q2,q3=blueq(p1,p2),blueq(p2,p3),blueq(p3,p1)
		if q1*q2*q3==0: continue
		s3 = Fraction( -sqr( q1+q2-q3 ) ,4*q1*q2) + 1
		s2 = Fraction(s3,q3) * q2
		s1 = Fraction(s3,q3) * q1
		#print s1,s2,s3
		print float(s1),float(s2),float(s3)
		print float(s2),float(s3),float(s1)
		print float(s3),float(s1),float(s2)
		print float(s1),float(s3),float(s2)
		print float(s2),float(s1),float(s3)
		print float(s3),float(s2),float(s1)

# Cross:          q0+q1-q2 sqred = 4*q0*q1*(1-s2)
# sqr q0+q1-q2 / 4q0q1 = 1 - s2
# sqr q0+q1-q2 / 4q0q1   - 1 =  - s2
# - sqr q0+q1-q2 / 4q0q1   + 1 =  s2

# to run, install antiview package, then do python ellipson.py | conv_hull | antiview
