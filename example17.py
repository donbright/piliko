from piliko import *
from random import randint
# piliko has very simple complex number ability (x + y*i)
c1 = complex( 5, 12 )
c2 = complex( 3, 2 )
c3 = complex( 0, 32)
print 'complex numbers c1, c2:',c1,c2
print 'double:',c1*2,c2*2
print 'sum:',c1+c2
print 'difference:',c1-c2
print 'squares:',c1*c1,c2*c2
print 'product:',c1*c2
print 'square root c1:',c1.sqrt()
print 'complex number c3:',c3
print 'square root c3:',c3.sqrt()
for i in range(0,5):
	c=complex(randint(0,100),randint(0,100))
	csq=c*c
	print c,'sqr>',csq,'sqrt>',csq.sqrt()
