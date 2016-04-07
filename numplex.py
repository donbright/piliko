#!/usr/bin/env python3
# complexity of natural numbers
# see https://youtu.be/EUvFXd1y1Ho

# python3 - for unicode
# ▵ = unicode 25B5
# m▵n = m ^ m ^ m ^ m ... n times
import itertools

symbolsstr = '0 1 2 3 4 5 6 7 8 9 ( ) + * ^ ▵'
symbols = symbolsstr.split(' ')

def eval_expression(expression):
	print('evaluating ',expression)
	s=expression
	s=s.replace('^','**')
	print(s)

print('symbols',symbols)

def convert_int_to_expression(i):
	pass

def convert_to_expression(e):
	print('converting e')
	return '0+0'

# find lowest complexity expression that evaluates to the value n
# return new expression. if all else fails, give back n itself.
def findc(n):
	ns=str(n)
	numdigits = len(ns)
	print('length of ',n,':',numdigits)
	for e in itertools.product(symbols[0:16],repeat=numdigits):
		print(e)
		expr=convert_to_expression(e)
		testn=eval_expression(expr)
		if n==testn: print("n==testn",n)
	return len(str(n)),str(n)

n=150
complexity,expression = findc(n)
print('lowest complexity('+str(n)+') =',complexity,',"'+expression+'"')
