# 3 4 5 triangle inscribed in a square.

#
#      J      K
# ._______.______.
# |     s /-_    |
# | P    /   -_ s|
# |     /   3  -_|
# |    /4       -|
# |   /      _-` |
# |  /    _-`    |
# | /  _-`  5    |
# |/_-___________|
#
# Find P


from sympy import *
import math
from fractions import Fraction
P,J,K=symbols('P,K,J')

J=16-P
K=Fraction(9,16)*P
eq=2*(J**2+K**2+P**2)-(J+K+P)**2

print solve(eq,P)

