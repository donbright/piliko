from fractions import Fraction

layer = [1,1]
newlayer = []
for i in range(1,5):
	for i in range(len(layer)-1):
		newlayer += [layer[i],layer[i]+layer[i+1]]
	newlayer += [1]
	print newlayer
	layer=newlayer
	newlayer=[]

for m in layer:
	for n in layer:
		for m1 in layer:
			for n1 in layer:
				l = Fraction( m*m-n*n , m*m+n*n )
				z = Fraction( 2*m*n , m*m+n*n )
				x = l * Fraction( m1*m1-n1*n1, m1*m1+n1*n1 )
				y = l * Fraction( 2*m1*n1    , m1*m1+n1*n1 )
				print x,y,z,' sq sum: ',x*x+y*y+z*z
