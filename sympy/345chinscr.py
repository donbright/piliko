# 3 4 5 triangle inscribed in a square.

#      j      k
# ._______.______.
# |     s /-_    |
# | p    /  3-_ s| m
# |     /      -_|
# |    /4       -|
# |   /    5 _-` |
# |  /    _-`    | n
# | /  _-`       |
# |/_-___________|
#        l
#
# find p
#
#
# Rational Trig view, quadrance, which is like distances squared
# theta = spread s, which is similar to sine-squared
#
#      J      K
# ._______.______.
# |     s /-_    |
# | P    /  9-_ s| M
# |     /      -_|
# |    /16      -|
# |   /   25 _-` |
# |  /    _-`    | N
# | /  _-`       |
# |/_-___________|
#        L
#
#
# Find P


from sympy import *
import math
from fractions import Fraction
P,J,K,M,N,L=symbols('P,K,J,M,N,L')
import sys

geometry='blue' # or green or red. see Quadrance()

def Quadrance(x,y):
	if geometry=='blue': return x**2+y**2
	if geometry=='green': return 2*x*y
	if geometry=='red': return x**2-y**2
#blue
#J=16-P
#K=Fraction(9,16)*P
#eq=2*(J**2+K**2+P**2)-(J+K+P)**2

#green
#
Pa,Pb=solve(eq,P)
print J,K,Pa,Pb
sys.exit


J=16-Pb
K=Fraction(9,16)*Pb
M=9-K
N=25-Pb
L=Pb
New16=J+Pb
New9=M+K
New25=N+Pb
legsa=[Pb,J,K,M,N,L,New16,New9,New25]
print legsa
print 'P,J=16-P,K=P*9/16,M=9-K,N=25-P,L=P'
print map(lambda x:float(math.sqrt(x)),legsa)



# for the other solution, J is the long side
Pa=Pa
J=16-Pa
K=Fraction(9,16)*Pa
M=9-K
L=J
N=symbols('N')
eq2=2*(M**2+N**2+J**2)-(M+N+J)**2
print 'eq2',eq2
Na,Nb=solve(eq2,N)
legsa=[Pa,J,K,M,Na,L]
print legsa
print 'Pa,J,K,M,N,L'
print map(lambda x:float(math.sqrt(x)),legsa)
print 'N+J',Na+J

