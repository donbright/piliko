from sympy import *
zt,zr,zs,t,r,s=symbols('zt,zr,zs,t,r,s')
v1,v2,a,b,c,d=symbols('v1,v2,a,b,c,d')
x=symbols('x')

v1=a+b*I
v2=c+d*I
ratvec = (1-x**2)/(1+x**2) + (I*2*x) / (1+x**2)
zt = ratvec.subs(x,t)
zr = ratvec.subs(x,r)
zs = ratvec.subs(x,s)
a1=zs.subs(s,(t+r)/(1-t*r))
a2=zt*zr
print(a1)
print()
print(a2)
