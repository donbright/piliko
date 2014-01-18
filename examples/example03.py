from piliko import *

print
print 'example 3'

l0 = line(1,-2,3)
l1 = line(4,-3,7)
print 'lines l0,l1', l0, l1
print 'blue spread: ', blue_spread( l0, l1 )
print 'red spread: ', red_spread( l0, l1 )
print 'green spread: ', green_spread( l0, l1 )
csl = colored_spread_lhs( l0, l1 )
csr = colored_spread_rhs( l0, l1 )
print 'colored spread theorem (1/g+1/b+1/r=2): lhs:', csl, ' rhs: ', csr

