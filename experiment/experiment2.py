from fractions import Fraction
import sys

def pyth():
	for i in range(1,100):
		for j in range(1,100):
			for k in range(1,100):
				if i*i+j*j==k*k: print i,j,k	
	print
	

def checkp(x,y,z):
	if x*x+y*y==z*z: return True
	if z*z+y*y==x*x: return True
	if x*x+z*z==y*y: return True

def newlayer(l1):
	l2=[]
	for i in range(len(l1)-1):
		#newnumerator = l1[i].numerator + l1[i+1].numerator
		#newdenominator = l1[i].denominator + l1[i+1].denominator
		#l2+=[Fraction(newnumerator,newdenominator)]
		l2 += [l1[i]+l1[i+1]]
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


def dopyth1():
	for m in range(0,20):
		for n in range(0,20):
			a=m*m-n*n # note - this is red quadrance
			b=2*m*n # note - this is green quadrance
			c=m*m+n*n # note - this is blue quadrance
			print a,b,c,checkpl([a,b,c])

def dopyth2():
	for m in range(1,110):
		for n in range(1,110):
			for k in range(1,110):
				print m,n,k,checkpl([m,n,k]),checkpr([m,n,k])
import math
def dopyth3():
	for m in range(1,110000):
		msq = m*m+(m-2)*(m-2)
		if checkp(m,m-2,math.trunc(math.sqrt(msq))): print m,m-2,math.sqrt(msq)

dopyth3()
sys.exit()

# pattern 1.. legs 1 apart?
# adjacent in stern diatomic network
# one per odd row
# in stern numerator, accumulate in every row!
# 3 4 5
# 5 12 13
# 7 24 25
# 9 40 41
# 11 60 61
# 13 , , 
# depth in tree = directly related to first #, formula for 2nd two order(n^2)

# pattern 2..??? legs 2 apart
#-1,0,1
#4,3,5
#8,15,17
#12,35,37
#16,63,65
#20,99,101
#24,143,145
#28,195,197
# again, order n^2  (2n,n^2+/-1, n=0,2,4,8,10,12,..). row = ?


# pattern 3
# legs will be 3 apart? (sqrt blue quadrance - sqrt green q = 3 )????

# or... pattern 3, legs will be 9 apart?
# 5, -4, 3
# 9, 0, 9
# 17 8 15               (also 2 apart)
# 29 20 21            
# 45 36 27            (also 3,4,5)

# or..... 7 apart?
# 12 5 13
# 15 8 17
# 28 21 35  (aleo 4 , 3, 5 )
# . . .

# note that pyth trigs with a prime leg do smth weird.

#dopyth2()
#sys.exit()
#l1=[0,0] # zero
#l1=[0,1] # numerator
l1=[1,1] # denominator (stern diamotic) 
prlen=1000
for j in range(0,21):
	print l1[0:prlen],'...',len(l1)
	nl = newlayer(l1)
	ml = mixlayer(l1, nl)
	l1 = ml
	print nl[0:prlen], '...',len(nl)
	print ml[0:prlen], '...',len(ml)
	ptl = checkpl(ml)
	print "pth:", ptl
	#for sublist in ptl:
	#	print "prm:", checkpr(sublist)
	print
