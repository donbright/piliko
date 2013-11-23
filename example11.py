from piliko import *

print '\n\nexample 11'

print 'spread_polynomials'
sp=spread_polynomial
maxn = 8

print 's=0, n=0,1,2,...'
print 'spoly(n,s):',
for n in range(0,maxn): print sp(n,0),
print

print 's=1, n=0,1,2,...'
print 'spoly(n,s):',
for n in range(0,maxn): print sp(n,1),
print

print 's=1/2, n=0,1,2,...'
print 'spoly(n,s):',
for n in range(0,maxn): print sp(n,Fraction(1,2)),
print

print 's=1/4, n=0,1,2,...'
print 'spoly(n,s):',
for n in range(0,maxn): print sp(n,Fraction(1,4)),
print

print 's=3/4, n=0,1,2,...'
print 'spoly(n,s):',
for n in range(0,maxn): print sp(n,Fraction(3,4)),
print

print 's=1/3, n=0,1,2,...'
print 'spoly(n,s):',
for n in range(0,maxn): print sp(n,Fraction(1,3)),
print

print 's=16/25, n=0,1,2,...'
print 'spoly(n,s):',
for n in range(0,maxn): print sp(n,Fraction(16,25)),
print

print 's=5, n=0,1,2,...'
print 'spoly(n,s):',
for n in range(0,maxn): print sp(n,Fraction(5,1)),
print

