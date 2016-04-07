# -*- coding: utf-8 -*-
from sympy import *
from collections import Counter

# explore primes and sums of squares and the pattern 4n+1 , 4n+3
#
# this uses 的 for sum of 2 squares and 質 for prime. These are chinese symbols.
# The symbols are parts of related phrases in Chinese.

squares = Counter()
squares[0]=0
squares[1]=1
squares[4]=2
squares[9]=3

def coprime(a,b):
	pa,pb=primefactors(a),primefactors(b)
	pc=set(pa).intersection(set(pb))
	if pc==set([]): return true
	return false

def extend_squares(n):
	global squares
	while n > max(squares.keys()):
		maxroot = squares[max(squares.keys())]
		squares[ (maxroot+1)**2 ] = maxroot+1
	#print squares

# given integer n, find the two squares that sum to it, or None,None if none do
def square_addends(n):
	if not n in squares.keys():
		extend_squares(n)
	for i in squares.keys():
		for j in squares.keys():
			if i+j==n:
				return i,j
	return None,None

# is the number n the sum of two square integers?
def issquaresum(n):
	if square_addends(n) == (None,None): return false
	return true

# latex pretty print factors of n
def ppfactorint(n):
	s=str(factorint(n))
	s=s.replace(': ','^')
	s=s.replace('}',',')
	#s=s.replace('}',')')
	s=s.replace('{','')
	s=s.replace(', ',' ')
	s=s.replace('^1 ',' ')
	s=s.replace('^1,',',')
	s=s.replace(' ','*')
	return s

tr = '   '
td = ''

for i in range(0,20):
	print td+'%0.3i' % (4*i+1),
	print td+'%0.3i' % (4*i+3),
	if isprime(4*i+1): print td+'質',
	else: print td+'--',
	if isprime(4*i+3): print td+'質',
	else: print td+'--',
	print square_addends(4*i+1),
	print square_addends(4*i+3),
	print factorint(4*i+1),
	print factorint(4*i+3),
	print


print
for i in range(0,20):
	print tr,
	print td+'%0.2i' % (4*i+0),
	print td+'%0.2i' % (4*i+1),
	print td+'%0.2i' % (4*i+2),
	print td+'%0.2i' % (4*i+3),
	if isprime(4*i+0): print td+'質',
	else: print td+'--',
	if isprime(4*i+1): print td+'質',
	else: print td+'--',
	if isprime(4*i+2): print td+'質',
	else: print td+'--',
	if isprime(4*i+3): print td+'質',
	else: print td+'--',
	if issquaresum(4*i+0): print td+'总',
	else: print td+'--',
	if issquaresum(4*i+1): print td+'总',
	else: print td+'--',
	if issquaresum(4*i+2): print td+'总',
	else: print td+'--',
	if issquaresum(4*i+3): print td+'总',
	else: print td+'--',
	print ppfactorint(4*i+0),
	print ppfactorint(4*i+1),
	print ppfactorint(4*i+2),
	print ppfactorint(4*i+3).strip(','),
	print

