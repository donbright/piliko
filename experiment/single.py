# find pythagorean triples in adjacent numbers in the 
# stern diatomic sequence (denominators of stern brocot tree... farey sequence
# sqrt ford circle radiuses, etc etc etc)

def pyth():
	for i in range(1,100):
		for j in range(1,100):
			for k in range(1,100):
				if i*i+j*j==k*k: print i,j,k	
	print
	

def checkp(x,y,z):
	if x*x+y*y==z*z: return True
	#if z*z+y*y==x*x: return True
	#if x*x+z*z==y*y: return True

def newlayer(l1):
	l2=[]
	for i in range(len(l1)-1):
		l2+=[l1[i]+l1[i+1]]
	return l2

def mixlayer(l1,l2):
	l3=[]
	for i in range(0,len(l1)-1):
		l3+=[l1[i],l2[i]]
	l3 += [l1[len(l1)-1]]
	return l3

def checkpl(ml):
	r=[]
	for i in range(0,len(ml)-2):
		x=ml[i]
		y=ml[i+1]
		z=ml[i+2]
		if checkp(x,y,z): r+=[[x,y,z]]
	return r

def checkpr(nlist):
	primes=[]
	for n in nlist:
		prime=True
		for i in range(2,n):
			if n % i == 0: prime=False
		if prime: primes += [n]
	return primes

l1=[0,0] # zero
l1=[0,1] # numerator
# l1=[1,1] # denominator
for j in range(0,23):
	print l1[0:10],'...',len(l1)
	nl = newlayer(l1)
	ml = mixlayer(l1, nl)
	l1 = ml
	print nl[0:10], '...',len(nl)
	print ml[0:10], '...',len(ml)
	ptl = checkpl(ml)
	print "pth:", ptl
	#for sublist in ptl:
	#	print "prm:", checkpr(sublist)
	print
