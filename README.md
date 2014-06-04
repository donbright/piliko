piliko
======

Piliko is a very, very, experimenral mishmash of Rational Geometry computer 
codes in the computer language called Python. It follows, roughly,
Rational Trigonometry in that it avoids irrational and transcendental 
numbers and functions, and the concepts of angle and distance are 
avoided.

#Current status

This code is 'alpha' level. It is highly experimental. It may or may not 
work at any time, as I am constantly tinkering with it. It can do basic 
calculations, but the whole type system has not been thought out very 
carefully and many functions are partially or wholly unimplemented. 
Tests have not been created. There are no actual users at this time so 
debugging, as you might imagine, has been minimal.

#Disclaimer 

Rational Trigonometry was discovered and developed by Dr. Norman J 
Wildberger. His concepts and terminology are used here without 
permission and the use of these ideas/terms doesn't necessarily imply 
his endorsement. All apologies if I make mistakes. Please see these 
sites for more information:

* https://www.youtube.com/user/njwildberger
* http://web.maths.unsw.edu.au/~norman/
* http://www.wildegg.com
* http://www.cut-the-knot.org/pythagoras/RationalTrig/CutTheKnot.shtml
* http://farside.ph.utexas.edu/euclid.html

The statements below are probably somewhat accurate, but of course I am 
not an expert so there you have it.

#But I don't know the computer language Python

You don't need to know Python to do basic calculations. The syntax is
designed to be somewhat simple. Please see the examples. As long as you can
start up a python interpreter on your machine, you should be OK. See
http://www.python.org to download a python interpreter for your computer. 
Once you can get to the screen where you type 
	
	print 'hello world'

and get a 'hello world' to appear, then you will almost be ready to use 
piliko. The next step is to put the 'piliko.py' file in a folder where 
your python interpreter can find it. Then you can load piliko with this 
command in python:

	from piliko import *

#Examples

Example A:

	from piliko import *

	p1 = point(0,0)
	p2 = point(3,0)
	p3 = point(0,4)
	print p1,p2,p3

	print quadrance(p1, p2)

	L1 = line( p1, p2 )
	L2 = line( p1, p3 )
	s = spread( L1, L2 )
	print s

Result:

	[0,0] [3,0] [0,4]
	9
	1

Example B:

	t = triangle(point(0,0),point(4,3),point(2,5))
	oc,cc,nc = orthocenter(t),circumcenter(t),ninepointcenter(t)
	print oc,cc,nc
	print collinear( oc, cc, nc )
	
Result:

	[23/7,23/7] [19/14,33/14] [65/28,79/28]
	True

Example C:

	p1,p2,p3,p4 = point(0,0),point(3,0),point(2,0),point(6,0)
	print is_harmonic_range( p1, p2, p3, p4 )
	
Result:

	True

Example D:

	p=point(3,4)
	bq,rq,gq=blue_quadrance(p),red_quadrance(p),green_quadrance(p)
	print p,' ',bq,rq,gq,' ',sqr(bq),sqr(rq),sqr(gq)

Result:

	[3,4]   25 -7 24   625 49 576

More examples can be found in the files named example01.py, example02.py, etc
To run them:

	python example01.py
	python example02.py
	etc etc

Even more examples are under the 'experiment' folder of this bundle.

#Plotting pictures

When the add-on 'matplotlib' package is installed on your system, you can do
some basic plotting of pictures. For example:

	t = triangle(point(0,0),point(4,3),point(2,5))
	oc,cc,nc = orthocenter(t),circumcenter(t),ninepointcenter(t)
	circ = circle( oc, blueq( oc, point(0,0 ) )
	plot_circle( circ )
	plot_points( oc,cc,nc )
	plot_triangle( t )
	plotshow()

#Differences with real-number geometry

Geometry under rational numbers is different than 'ordinary' geometry using
the real numbers. Here are some key points.

```
Real                               Rational
----                               --------

The real number line is            The Rational line is fundamental
fundamental and used               and irrationals are avoided.
in calculations

Points can have any                Points can only have Rational
coordinates                        coordinates

Distances are fundamental          Quadratic Forms (Quadrance)
sqrt(x^2+y^2)                      are fundamental. x^2+y^2
                                   Distance = square root of Quadrance.

Circles are specified              Circles are specified by rational 
by radius & center                 center and by radius squared.

The point 1,1 is on                There is no circle centered at
a circle with center 0,0           0,0 containing the point 1,1

Any line with points inside        Some lines with points inside
the circle intersects the          the circle won't intersect it.
circle

Infinite series approximations     Only finite numbers are used.
are used in calculations.

e + pi might be rational           e and pi are both infinite 
or might not be                    series, so the question is moot.

Angles are used to measure         Spread is used (sin squared)
line separation

Angles can be simply added.        Spreaded lines are combined using
                                   spread polynomials.

The basic right triangles are      Basic right triangles are the Pythagorean
45-45-90, 30-60-90, 60-60-60       triple triangles, like 3,4,5  5,12,13, etc. 
(angle based) with irrational      Many angle-based triangles have irrational 
lengths.                           points.

Wedge between vectors can be       Wedge between vectors is 
expressed with 'sin'               x1*y2-x2*y1

Regular polygons are specified    Many regular polygons have irrational
by angles added.                  points and so are not representable.

Hyperbolic, Elliptical,           Hyperbolic, Elliptic, and Spherical
Spherical are special cases       geometry share many of the same formulas
with very different formulas      and ideas.

Circles are described with        Circles are described exactly using
sine and cosine approximations    rational paramterizations

Infinite series and sets are      Infinite series and sets are avoided
commonplace

Infinity is something we cant     Infinity can be dealt with using
deal with concretely              projective geometry (points-at-infinity map
                                  to finite points in 'ordinary' space, perhaps
                                  of a lower dimension)

Tangents can have any slope       Tangents have rational slope.

Tangents exist at every point     Tangents exist at rational points


```                               

Chromogeometry
==============

The package also contains several items of Chromogeometry, which is 
Wildberger's approach to changing the concept of 'square distance'
to include x^2-y^2 and 2*x*y in addition to the 'normal' x^2+y^2.

Red quadrance = x^2-y^2 and Green Quadrance = 2*x*y Red Circles are 
hyperboals and Green Circles are also hyperbolas but 'rotated' 45 
degrees. The concept of spread also has a 'red' and 'green' version, as 
well as perpendicularity.

Author and Copyright License
============================

Piliko is written by Don Bright, <hugh.m.bright at gmail.com>, 2013.

This code is free for use under a basic BSD-style Open Source Software 
license as described in the LICENSE file. You can freely copy and use it
per the terms in that LICENSE file.
