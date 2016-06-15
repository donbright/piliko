#!/usr/bin/env python3
from sympy import *

for i in range(0,100):
	i=65537
	if i%4==0:
		print()
		for j in range(0,4):
			print('%2d'%(i+j),end=' ')
		print('  ',end=' ')
	factors = factorint(i)
	#print(factors,end=' ')
	sum_of_two_squares = True
	for k in factors.keys():
		exponent = factors[k]
		if k%4==3 and exponent%2==1: sum_of_two_squares = False
	if sum_of_two_squares:
		print('Σ',end=' ')
	else:
		print('.',end=' ')

