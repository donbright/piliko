# showing that the length of an object varies with translation. 
# and comparison will thus be dependent on translation.

ax0=4.0
ax1=4.1
alength=ax1-ax0
bx0=4.0
bx1=4.1
blength=ax1-ax0
print 'object a, ',ax0, ax1
print 'object b, ',bx0, bx1
for i in range(0,100,10):
	bx0+=float(i) # translation by i
	bx1+=float(i) # translayion by i
	blength=bx1-bx0
	print '\nb translated by:',i
	print 'new b length:' + '%.54f' % blength
	print 'length of b', 
	if blength < alength: print '<',
	if blength > alength: print '>',
	if blength == alength: print '==',
	print 'length of a'

