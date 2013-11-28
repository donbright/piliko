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
name and terms here, like Rational Trigonometry, quadrance, spread, etc, 
doesn't imply that he endorses this package. Please see these sites for
more information:

* https://www.youtube.com/user/njwildberger
* http://web.maths.unsw.edu.au/~norman/
* http://www.wildegg.com
* http://www.cut-the-knot.org/pythagoras/RationalTrig/CutTheKnot.shtml
* http://farside.ph.utexas.edu/euclid.html

The statements below are probably somewhat accurate, but of course I am 
not an expert so there you have it.

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

Some of the examples require extra python libraries, like matplotlib for 
plotting.

Basic principle
===============

The Rational numbers, as implemented in Python's Fraction module, with 
Big Integers, are closed under addition, subtraction, multiplication, 
and division. This makes them fundamentally different from floating 
point numbers. This also makes them uniquely suited to geometry, as many 
geometry packages have proven (including CGAL and LEDA). Why? Because 
many of the basic geometry operations, including scale, translate, 
boolean, intersection, etc, are doable in algebra using only plus, 
minus, multiply, and divide, without approximation in the results.

In other words, for many geometric operations, if you stick to Rationals 
and rational functions, the issue of floating-point error disappears.

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
universally applicable concept of distance. For example, the point '1,1'
has a distance of sqrt(2) from the origin. The point '1,0' has a distance
of 1 from the origin. The former is not expressable as a finite sequence
of numbers, but the latter is. 

Another thing you lose is the idea of curve intersections. A line may intersect
a circle at irrational points, which cannot be expressed in Rationals. Also
many curves have few or no rational points on them. 

Another huge loss is that you can't add two angles together with simple 
addition. You have to use 'spread polynomials' instead.

Slowness
========

The big downside of any rational number system is that it can be slow. 
There is the ordinary problem, for example that adding two numbers 
actually takes 3 multiplications and a subtraction.. but that is not the 
biggest issue. Besides, division is actually faster than under floating 
point - because with Rationals, division is just multiplying 
denomimnators.

The big problem is when you chain several computations together. Your
Rationals are probably using a form of integer called 'big integer' that cannot
'overflow'. This means if you have some long fraction like 

909039039020367846780390904/493903903938089890308298173897891821

To simplify it, you can use the Greatest Common Divisor code, but that slows
us down even more. If it cannot be simplified, then you are in a pickle. 
You are stuck with these enormous numbers. Multiplying them can be quite
slow compared to floating point. Storing them can take a lot of RAM as well.

Just imagine by just thinking about squaring one of these fractions a 
few times and adding some number such that there is no simplified form. 
A good example would be simulating a space ship and planet, with 
force=g*mass1*mass2/radius^2. Re-calculate that a few dozen times and 
you are looking at hundreds of digits for numbers. Where the old 
'floating point' number takes 4 bytes to store, the Big Int rational 
might take dozens of bytes, and be dozens of times slower to add or multiply.

But to maintain the beautiful 'no approximation' feature of Rationals, 
you have to store all these digits.

This is fundamentally different from how finite length floating point 
numbers worked. Or even ordinary finite length integer arithmetic in old 
2d graphics libraries. In those systems, you can 'throw out' large numbers
of digits with each calculation. With Big Integer Rationals, you carry these
digits with you.

Author and Copyright License
============================

Piliko is written by Don Bright, <hugh.m.bright at gmail.com>, 2013.

This code is free for use under a basic BSD-style Open Source Software 
license as described in the LICENSE file. You can freely copy and use it
per the terms in that LICENSE file.
