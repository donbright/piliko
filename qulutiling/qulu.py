# -*- coding: utf-8 -*-

# Qu Lu Tiling
#
# In essence, each "trail" of a circle in Ford's Circles has a fun
# corresponding Tiling of Squares. This program will show it in SVG format.
#
# You only need to input the X coordinate of the Ford Circle in question.


# This is a tiling of squares that is linked directly to the
# Triple Quad Formula from Rational Trigonemetry and...
# Descarte's Circle Formula as applied to Ford's Circles

# In this document Curvature (1/Radius) is written by Chinese character Qu, 曲
# Quadrance (distance squared) is written as capital Latin Q.

# Basically, pick any cirlce deep down in Ford's Circles. There is a
# "path" if circle-triples back up to the original triple,
# 0/1, 1/1, and 1/2

# Now, The relationship between these three curvatures is
# 2 * (曲^2+曲^2+曲^2) = (曲+曲+曲)^2
#
# This is a similar relationship between quadrances of three squares
# mutually tangent.
# 2 * (Q^2+Q^2+Q^2) = (Q+Q+Q)^2

# Why? Well, it might be because Quadrance is essentially the Ratio between
# Radius and Curvature. In other words, rewriting the definitions shows it.
#
# 曲 = 1/R
# Q = R/曲,
# Q = R/(1/R)
# Q = R^2
#
# Therefore Quadrance is the Ratio of Radius to Curvature.
#
# https://chinese.yabla.com/chinese-english-pinyin-dictionary.php?define=%E6%9B%B2%E7%8E%87

from fractions import Fraction

square_roots={}

# assumes x is integer, does bad things if it's not
def sqrt(x):
	if not x in square_roots:
		for i in range(0,x/2+2):
			square_roots[i*i]=i
	return square_roots[x]

def squaresvg(lox,loy,hix,hiy):
	w,h=hix-lox,hiy-loy
	w,h=w*pixels_per_unit,h*pixels_per_unit
	x = border + lox * pixels_per_unit
	y = picsize - ( border + hiy * pixels_per_unit )
	x,y,w,h = str(x),str(y),str(w),str(h)
	style='fill:white;stroke:black'
	s=''
	s+='<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" style="'+style+'"/>\n'
	return s

# draw three squares w given quadrances assuming all three satisfy
# triple-quad-formula.
def triplesquare(q1,q2,q3):
	s1,s2,s3=sqrt(q1),sqrt(q2),sqrt(q3)
	s1=min(s1,min(s2,s3))
	s3=max(s1,max(s2,s3))
	s=''
	# order matters in svg. draw big first, small ones on top of it
	s+=squaresvg(0,0,s3,s3)
	s+=squaresvg(0,0,s1,s1)
	s+=squaresvg(s1,s1,s3,s3)
	return s


# find chain of Ford Circles back up from circle at given x coordinate.
# a / b  = la + ra / lb + rb
# b(la+ra) = a(lb+rb)
# ??? ok forget this
# assumes xcoord is Fraction, bad things happen otherwise
def findchain( xcoord ):
	a = xcoord.numerator
	b = xcoord.denominator
	print a,b
	radius = Fraction(1,2*b*b)
	curvature = Fraction(1, radius)
	print a,b,radius,curvature

picsize = 640
border = 5
maxside = 3
pixels_per_unit = ( picsize - 2 * border )  / maxside
borderstyle='fill:gray;stroke:black'

s= '<svg xmlns="http://www.w3.org/2000/svg" width="%i" height="%i">\n' % ( picsize, picsize )
s+= '<!-- pixels per unit %s -->' % ( pixels_per_unit )
s+= '<rect x="%i" y="%i" width="%i" height="%i" style="%s"/>\n' % ( 0,0,picsize,picsize,borderstyle )
s+= triplesquare(1*1,2*2,3*3)
s+= '\n </svg>\n'
print s

findchain(Fraction(1,3))
