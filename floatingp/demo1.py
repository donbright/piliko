# find a floating point value for x such that 
# x+1.0 is not the same thing as x+1
# in other words, where the smallest amount you can add to a 
# float becomes greater than one(.5).

x=1.0
while True:
	x*=2
	y=x
	xint=int(x)
	x+=1.0
	x2int=int(x)
	diffint=x2int-xint
	print x, y, xint, x2int, diffint
	if diffint!=1: break


