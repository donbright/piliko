# show all solutions to Sn where Sn is the spread function

from sympy import *

s=symbols('s')
s0 = 0
s1 = s
s2 = 4*s*(1-s)
s3 = s*(3-4*s)**2
s4 = 16*s*(1-s)*(1-2*s)**2
s5 = s*(5-20*s+16*s**2)**2
s6 = 4*s*(1-s)*(3-4*s)**2*(1-4*s)**2

sses = [s0,s1,s2,s3,s4,s5,s6]
n=0
for sn in sses:
	print n,solve(sn,s),'eqn 0 =',sn
	n+=1
