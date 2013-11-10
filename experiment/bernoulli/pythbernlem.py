from fractions import Fraction
import sys

# rational paramterization / approximation of bernoulli's lemniscate
# traditional form: ( x^2 + y^2 ) ^2 = 2*a*( x^2 - y^2 )

# (note - this uses terms from Norman Wildberger's rational 
# trigonometry/chromogeometry. briefly for a vector from 0,0 to x,y:
#
# blue quadrance (x,y) = x^2 + y^2
# red quadrance (x,y) = x^2 - y^2
# green quadrance (x,y) = 2*x*y
# )

# theory:
#
# to summarize: we have a rational paramterization of the hypebrola, x,y 
# as x = blueq/redq and y = greenq/redq , with quadrances to rational 
# point m,n. now, Bernoulli's lemniscate is an inverse of the hyperbola 
# through the origin, so just find rational x,y for hyperbola, then do
#   
#   lamda = constant = 1/blueq(x,y)
#   x_lemniscate = x_hyperbola*lambda
#   y_lemniscate = y_hyperbola*lambda
#


# in more detail::::
#
# first, we have a rational paramterization of the hyperbola.
# for this, see the 'pythhyp' series of .py files.
#
# basically, we just use the rational paramterization of a circle: 
#
# x,y = redq/blueq, greenq/blueq     for rational points m,n
#
# written in ordinary algebra:
#
# x,y = m^2-n^2 / m^2+n^2 , 2mn / m^2+n^2
#
# Now we modify it a bit as though the hyperbola is a 'red circle' from 
# Norman Wildberger's Chromogeometry
#
# x = blueq/redq, y = greenq/redq     for rational points m,n
#
# written with ordinary algebra:
#
#  x = (m^2 + n^2) / (m^2 - n^2 )    y = 2mn / (m^2 - n^2)
#
# where m,n are rationals (usually, integers,,, but you can use any rational)
#
# So there is your rational paramterization of the hyperbola


#
# Next, following Wildberger's youtube lecture on the Bernoulli 
# Lemniscate, we note that the lemniscate curve is the inverse of the 
# hyperbola through the origin... meaning that you can draw a line from 
# the origin that intersects both the hyperbola and the lemniscate...
# and there is a special relationaship between those intersection points.
# Their distances from origin, when multiplied, produce a constant! Wow, cool!
# Now since we are following Dr Wildberger here, lets just use Blue Quadrance
# instead of distance, and save ourselves the trouble of square roots.
# So lets square our constant too.

# How does this help us? imagine we draw a line from the origin, and 
# call the hyperbola intersection x,y and the lemniscate intersection 
# x2,y2. we can imagine two similar right triangles:
#
# points [0,0] [x,0] [x,y] -> for hyperbola
# points [0,0] [x2,0] [x2,y2] -> for lemniscate
#
# Call the hypoteneuse for the hyperbola point by the name 'oh', and for the 
# leminscate point use the name 'ol'. Call the blue quadrances of the 
# hypotenueuses as OH and OL.
#
# Now, these triangles are similar... so we can use this fact. If we 
# know x and y, we can find x2,y2 using the proportionality between the 
# similar triangles.

# So since the triangles are similar, OL = some-constant^2 * OH. Lets call 
# this constant lambda.
#
# so we have some facts about OL and OH now, so how does it fit together?
#
# OH * OL = k^2        <- from the fact of inversion
# OL = OH * lambda^2   <- from the fact of similar triangles being proportional
#
# solve for lambda... 
# lambda^2=OL/OH, OL <= k^2/OH
# lambda^2=(k^2/OH)/OH 
# lambda^2 = k^2/OH^2
# lambda = k/OH

# now our goal is to find x2,y2 using the proportionality of 2 similar 
# triangles. now we found our proportionality, lambda, so we can find x2,y2.
#
# x2 = x * lambda
# y2 = y * lambda
# 
# Now, note that x2 and y2 are both rational, as long as x,y are 
# rational and lambda is rational.
#
# But wait, we know how to generate rational x,y... they are rational 
# points on the hyperbola, and we have a rational paramterization for 
# that! And obviously lambda will be rational b/c its the result of 
# rational math
#
# Thus, we have a rational paramterization for Bernoulli's Lemniscate. 
#
# for a bunch of integers or rationals m,n:
#
# x = blueq(m,n)/redq(m,n)       <-- rational hyperbola
# y = greenq(m,n)/redq(m,n)
# lambda = k/blueq(x,y)
# x2 = x * lambda                <-- rational lemniscate
# y2 = y * lambda


#### wait, couldn't you just use a simple version of the hyperbola?
#### x = sequence of rationals
#### y = 1/x 
####
#### yes. but i like the aesthetics of chromogeometry
####

def sqr(x): return x*x
def greenq_pts(x,y,x2,y2): return 2*(x2-x)*(y2-y)
def redq_pts(x,y,x2,y2): return sqr(x2-x)-sqr(y2-y)
def blueq_pts(x,y,x2,y2): return sqr(x2-x)+sqr(y2-y)

def greenq(m,n): return greenq_pts(0,0,m,n)
def redq(m,n): return redq_pts(0,0,m,n)
def blueq(m,n): return blueq_pts(0,0,m,n)

xs,ys=[],[]
depth = 13
for m in range(-depth,depth):
	for n in range(-depth,depth):
		if redq(m,n)==0: continue
		x = Fraction(blueq(m,n),redq(m,n))
		y = Fraction(greenq(m,n),redq(m,n))
		oh = blueq(x,y)
		lambd = Fraction( 1, oh )
		x = x * lambd
		y = y * lambd
		xs += [x]
		ys += [y]

max=max(xs+ys)
for i in range(0,2):
	print xs[i],',',ys[i],
print '....'
for i in range(0,len(xs)):
	xs[i] = Fraction( xs[i], max )
	ys[i] = Fraction( ys[i], max )

print len(xs), 'points'
import numpy as np
import matplotlib.pylab as plt
fig,ax = plt.subplots(figsize=(8,8))

ax.set_ylim([-1.2,1.2])
ax.set_xlim([-1.2,1.2])
for i in range(0,len(xs)):
	xs[i]=xs[i]#+zs[i]/4
	ys[i]=ys[i]#+zs[i]/4
ax.scatter(xs,ys)
plt.show()
