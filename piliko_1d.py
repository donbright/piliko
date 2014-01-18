# find interection of two 1d line segments
def intersection( a1,a2,b1,b2 ):
	alo, ahi = min(a1,a2),max(a1,a2)
	blo, bhi = min(b1,b2),max(b1,b2)
	l=[a1,a2,b1,b2]
	l.sort()
	lo,hi = l[1],l[2]
	if l[1]<blo and l[2]>ahi: lo,hi=None,None
	if l[1]<alo and l[2]>bhi: lo,hi=None,None
	return a1,a2,b1,b2,lo,hi


if __name__=='__main__':
	print intersection(1,2,3,4)
	print intersection(1,3,2,4)
	print intersection(1,2,2,4)
	print intersection(1,2,1,2)
	print intersection(3,4,1,2)
	print intersection(2,4,1,3)
	print intersection(2,4,1,2)
	print intersection(0,0,0,0)

	print intersection(1,5,3,4)
	print intersection(1,3,5,4)
	print intersection(1,5,5,4)
	print intersection(1,5,1,5)
	print intersection(3,4,1,5)
	print intersection(5,4,1,3)
	print intersection(5,4,1,5)

	print intersection(1,5,3,6)
	print intersection(1,3,8,0)
	print intersection(1,5,8,0)
	print intersection(1,5,7,0)
	print intersection(3,4,7,0)
	print intersection(5,4,6,0)
	print intersection(5,4,6,0)

