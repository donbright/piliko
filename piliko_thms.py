from piliko import *

def theorems_txt():
	s='''
Quadrance:      Blue: x^2+y^2 Red: x^2-y^2 Green: 2*x*y
Right Triangle: q0+q1=q2 s0+s1=1 s2=1 s0=q1/q2 s1=q0/q2 
Triple Quad:    (q0+q1+q2)^2 = 2*(q0^2+q1^2+q2^2)
Quadrea:        (q0+q1+q2)^2 - 2*(q0^2+q1^2+q2^2) = 16*triangle area
Triple Spread:  (s0+s1+s2)^2 = 2*(s0^2+s1^2+s2^2) + 4*s0*s1*s2
Cross:          (q0+q1-q2)^2 = 4*q0*q1*(1-s2)
Spread:         s0/q0 = s1/q1 = s2/q2
Color Quad:     blueq^2 + redq^2 + greenq^2 = 2
Color Spread:   1/blues + 1/reds + 1/greens = 2
Spread Poly:    sp(n,s) = 2*(1-2*s)*sp(n-1,s) - sp(n-2,s) + 2*s
Rat. Circle:    x^2+y^2=1 x=redq(m,n)/blueq(m,n) y=greenq(m,n)/blueq(m,n)
'''
	return s

####### calculate left hand side and right hand side of various formulas

