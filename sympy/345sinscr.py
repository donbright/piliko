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
P,J,K,M,N,L,s=symbols('P,K,J,M,N,L,s')

P=16*s
K=9*s
J=16*(1-s)
eq=2*(J**2+K**2+P**2)-(J+K+P)**2
s1,s2=solve(eq,s)

print s1,s2
P1=16*s1
K1=9*s1
J1=16*(1-s1)
P2=16*s2
K2=9*s2
J2=16*(1-s2)
print 's1,P1,K1,J1',s1,P1,K1,J1
print map(lambda x:float(math.sqrt(x)),[s1,P1,K1,J1])
print 's2,P2,K2,J2',s2,P2,K2,J2
print map(lambda x:float(math.sqrt(x)),[s2,P2,K2,J2])

