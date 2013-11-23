from fractions import Fraction as Fract

##########
#
# rational parameterization of the 'dumbbell' p-orbital shape. sort of 
# like bernoulli's lemniscate, but in 3d. using four input variables, 
# m1,n1 m2,n2 all rational/integer
#

# chromogeometry notation is used here. 3 'quadrance' functions, input is 'a,b'
# blue quadrance from point (0,0) to point (a,b) = a^2+b^2
# red quadrance from point (0,0) to point (a,b) = a^2-b^2
# green quadrance from point (0,0) to point (a,b) = 2ab

# thus "blue/red" = m^2+n^2 / m^2-n^2

# basic equation of lemniscate for x,y:
#
# (x^2+y^2)^2 = 2*(x^2-y^2)
# 
# (blueq)^2 = 2*redq
#
# equation of lemniscate inverse (the hyperbola):
# 
# y=1/x
#
# paramterization of lemniscate inverse (hyperbola):
# 
# x=blue/red  y=green/red
#

# so then, using the paramterization of the hyperbola, from pythhyp*.py,
# and the 4-variable paramterization of the sphere, pythsphere*.py,
# we sort of 'combine' those techniques.

# step one is to say that 'x' and 'l' are going to be the 'distance' from
# origin and 'radius' of the 'dumbbell'. now, y and z will help us to make
# an actual rational x,y,z point on the surface of the dumbbell. 
#
# now. first we find rational paramterization of x and l. 
# we know (x^2+l^2)^2 = 2*(x^2-l^2) and some people can use that to find
# a rational parameterization. i am not that smart so i use the fact that
# hyperbola inverse = lemniscate. 

# 
# preliminaries
# xh = Fract(blue,red)
# yh = Fract(green,red)
# OH = blueq(xh,yh)
#
# we know OH*OL = k^2, because thats what inversion is. similar triangle 
# hypoteneuses. be rearranging, you find that (xh/xl)^2=oh/ol and thus
# xl^2 = xh^2*(ol/oh),   but ol/oh is k^1/(oh^2) and we can find oh. 
# so xl is k/oh * xh. 
# 
# so for x and l we can say
#
# x = k/oh * blue/red   and l = k/oh * green/red
# 



#
# the next step is noting that z^2+y^2 = l^2. using a similar technique 
# from paramterizing the sphere we go (z/l)^2 + (y/l)^2 = 1, therefore 
# z/l = red/blue and y/l = green/blue. thus z = l * red/blue, 
# and y = l * green/blue.
#
#
# x = Fract(k,OH) * blue1/red1
# l = Fract(k,OH) * green1/red1
# y = l * Fract( green2, blue2 ) 
# z = l * Fract( red2, blue2 )
#

xs,ys,zs=[],[],[]

depth=8
k=1
def blueq(a,b): return a*a+b*b
def redq(a,b): return a*a-b*b
def greenq(a,b): return 2*a*b
for m1 in range(-depth,depth):
	for n1 in range(-depth,depth):
		for m2 in range(-depth/2,depth/2):
			for n2 in range(-depth/2,depth/2):
				blue1,red1,green1 = blueq(m1,n1),redq(m1,n1),greenq(m1,n1)
				blue2,red2,green2 = blueq(m2,n2),redq(m2,n2),greenq(m2,n2)
				if red1==0: continue
				if blue2==0: continue
				xh = Fract(blue1,red1)
				yh = Fract(green1,red1)
				OH = blueq(xh,yh)
				x = Fract(k,OH) * xh
				l = Fract(k,OH) * yh
				y = l * Fract( green2, blue2 )
				z = l * Fract( red2, blue2 )
				#print x,y,z,' sq sum: ',x*x+y*y+z*z
				xs += [x]
				ys += [y]
				zs += [z]

max=max(xs+ys+zs)
for i in range(0,len(xs)):
        xs[i] = Fract( xs[i], max )
        ys[i] = Fract( ys[i], max )
        zs[i] = Fract( zs[i], max )


print len(xs)
import numpy as np
import matplotlib.pylab as plt
fig,ax = plt.subplots(figsize=(8,8))

ax.set_ylim([-1.2,1.2])
ax.set_xlim([-1.2,1.2])
for i in range(0,len(xs)):
	xs[i]=xs[i]+zs[i]/4
	ys[i]=ys[i]+zs[i]/4
ax.scatter(xs,ys)
plt.show()

