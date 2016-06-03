# four ways of looking at a pentagon
#
# https://wordpress.com/post/sozvyezdami.wordpress.com/1975
#

from sympy import *
s=symbols('s')
a,b,c=symbols('a,b,c')

print solve( s*(5-20*s+16*s**2)**2, s )
