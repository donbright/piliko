piliko
======

Piliko is a very, very, very rough implementation of some formulas from 
Rational Trigonmetry in the computer language called Python. 

Current status
==============

This code is 'alpha' level. It is highly experimental. It can do basic 
calculations, but the whole type system has not been thought out very 
carefully and many functions are partially or wholly unimplemented. 
Tests have not been created.

Disclaimer 
==========

Rational Trigonometry was discovered and developed by Norman J 
Wildberger. He is not affiliated with this package and the use of his 
terms here, like Rational Trigonometry, quadrance, spread, etc, doesn't 
imply that he endorses this package.

* https://www.youtube.com/user/njwildberger
* http://web.maths.unsw.edu.au/~norman/
* http://www.wildegg.com
* http://www.cut-the-knot.org/pythagoras/RationalTrig/CutTheKnot.shtml
* http://farside.ph.utexas.edu/euclid.html

The statements here are probably accurate, but of course I am not an 
expert so there you have it.

But I don't know the computer language Python
=============================================

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

Examples
========

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

	from piliko import *

	v1 = vector(3,0)
	v2 = vector(0,4)
	print v1, v2
	s = spread( v1, v2 )
	print s

Result:

	(3,0) (0,4)
	1

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

Even more examples are under the 'experiment' folder of this bundle. But 
you will need to install extra python libraries, like matlpotlib, to use 
some of them.

Basic principle
===============

The Rational numbers implemented with Big Integers, unlike finite 
floating point numbers, are closed under addition, subtraction, 
multiplication, and division. This makes them uniquely suited to 
geometry, as many geometry packages have proven (including CGAL and 
LEDA). Why? Because many of the basic geometry operations, including 
scale, translate, boolean, intersection, etc, are doable in algebra 
using only plus, minus, multiply, and divide.

Therefore no approximation is required to perform these basic 
operations, which means the issue of floating-point error disappears.

It might even be possible to develop a geometry that does not use 
transcendental functions at all. There are rational analogues for 
rotation. Any conic curve can be approximated very well by rational 
parameterization (rational points on the curve). Bezier curves can be 
approximated by rational points. And thus, truetype(TM) fonts. 
Bernoulli's leminscate has a rational paramterization. Also a large 
number of polynomial curves can be parameterized by rational points. 
There are even people working algorithms to create rational 
paramterizations automatically.

There are also rational parameterizations for many of our favorite 3 
dimensional objects, like spheres, toruses, hyperbolic sheets, 
non-circle based toruses, dumbbells, and there are even people who have 
worked out rational parameterizations of 3 dimensional 'knot' shapes.

It may be even possible to create anlogues of geometry algorithms (like 
catmull clark subdivision or Delaunay triangulation) using rational 
points and rational functions.

The downside is that you lose some old things, like the notion of 
distance in any situation (for example, the point 1,1 is sqrt(2) from 
the origin... a rational circle will not include any such point at 45 
degrees angle), or the intersection of any line with any circle (this is 
replaced by the notion of the intersection of a line with the polygon 
approximation of the circle). Even the length of the side of a 45-45-90 
or 30-60-90 triangle is lost.

Another huge loss is that you can't add two angles together with simple 
addition. You have to use 'spread polynomials' instead.

What is approximation
=====================

In the end, there is no 'exact' circle in a computer, so you are just 
choosing between methods of approximation. Rational approximation is 
just another approximation method. However it has some advantages in 
that, as described, it is closed under division, so you can scale 
objects without loss of information, inside of your 'engine', before you 
actually have to output them. And rational points on a circle form 
pythagorean triples, so they have an exact distance from the center, not 
an approximate distance. Like the point 3,4 is exactly 5 from the 
center.

The term 'approximate' here means that the curves that are usually 
approximated with floating point approximations of transcendental 
functions, are instead approximated by drawing line segments between 
rational coordinates. For example drawing lines between the rational 
points of the unit circle will result in a polygon approximation of the 
circle. Comparing this to the approximation of the circle generated by 
floating point functions like cosine and sine, it can be argued
that the floating point circle approximations are also polygons, 
because when you have to finally output the circle to some format, like 
a pixellated screen, or an STL or DXF file, you are going to output 
distinct points that represent points on the circle, and those points
are probably going to be either ASCII decimal points, which is simply a series of
powers of ten (3.125 = 3/10^0 + 1/10^1 + 2/10^2 + 5/10^1000) or some binary
format, which is just a series of powers of two (11010.1010 = 2^4+2^3+2^1+2^-1+2^-3)

Slowness
========

The big downside of any rational number system is that it can be slow. 
There is the ordinary problem, for example that adding two numbers actually
takes 3 multiplications and a subtraction.. but that is not the biggest issue.
The big problem is when you chain several computations together. Your
Rationals are probably using a form of integer called 'big integer' that cannot
'overflow'. This means if you have some long fraction like 

909039039020367846780390904/493903903938089890308298173897891821

and it cant be simplified, it will be stored as a special sequence of 
numbers in the machine. This can grow quite fast and slow the computer 
to a crawl, as you can imagine by just thinking about squaring one of 
these fractions a few times and adding some number such that there is no 
simplified form. A good example would be simulating a space ship and 
planet, with force=g*mass1*mass2/radius^2. Re-calculate that a few dozen 
times and you are looking at hundreds of digits for numbers. Where the old
'floating point' number takes 4 bytes to store, the Big Int rational might take
dozens of bytes, and be dozens of times slower to multiply.

But to maintain the beautiful 'no approximation' feature of Rationals, 
you have to store all these digits.

This is fundamentally different from how finite length floating point 
numbers worked. Or even ordinary finite length integer arithmetic in old 
2d graphics libraries. With each step in a finite approximation number 
system, you throw out vast numbers of digits, but with Big Integer 
rationals, you 'accumulate' digits.

Copyright License
=================

This code is free for use under a basic BSD-style Open Source Software 
license as described in the LICENSE file. You can freely copy and use it
per the terms in that LICENSE file.
