#!/usr/bin/env python3
# complexity of natural numbers
# see https://youtu.be/EUvFXd1y1Ho

# python3 - for unicode
# ▵ = unicode 25B5
# m▵n = m ^ m ^ m ^ m ... n times
import itertools
import sys,os

symbolsstr = '0 1 2 3 4 5 6 7 8 9 ( ) + * ^ ▵'
symbols = symbolsstr.split(' ')+[' ']

class Treenode:
	left,right,data=None,None,None
	def __init__(self,l,r,d):
		left,right,data=l,r,d

def tokens(sym):
	if sym in ['0','1','2','3','4','5','6','7','8','9',' ']:
		pass
	if sym in ['+','*','(',')']:
		pass
	if sym in ['^']:
		pass
	if sym in ['▵']:
		pass

#    a
#  b   c
#
def opplus(a,b):
	return a+b

a=Treenode(None,None,opplus)
b=Treenode(None,None,1)
c=Treenode(None,None,2)
a.left=b
a.right=c

def evalleafs(node):
	if node.left==None and node.right==None:
		return node.data
	else:
		a=evalleafs(node.left)
		b=evalleafs(node.right)
		node.data=c(a,b)

# find lowest complexity expression that evaluates to the value n
# return new expression. if all else fails, give back n itself.
def findc(n):
	shortestexpr = str(n)
	shortestlen = len(shortestexpr)
	ns=str(n)
	numdigits = len(ns)
	print('length of ',n,':',numdigits)
	for e in itertools.product(symbols[0:16],repeat=numdigits):
		print(e)
		expr=convert_to_expression(e)
		print(expr)
		testn=eval_pexpression(expr)
		print('testn',testn)
		if n==testn:
			pass
			# if len less than shortest, new shortest
	return shortestlen, shortestexpr

def main():
	n=150
	complexity,expression = findc(n)
	print('lowest complexity('+str(n)+') =',complexity,',"'+expression+'"')
