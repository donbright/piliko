piliko
======

Piliko is a very, very, very basic implementation of some formulas from 
Rational Trigonmetry in a computer language. 

Current status
==============

Alpha level, currently can do basic calculations, but types are not 
checked well and many functions are partially or wholly unimplemented.
Also design is messy currently and some bugs are undoubtedly present.


Disclaimer 
==========

This package is not affiliated with, nor endorsed in any way by Norman J 
Wildberger, who developed Rational Trigonometry. For more info, check these
websites:

* https://www.youtube.com/user/njwildberger
* http://web.maths.unsw.edu.au/~norman/
* http://www.wildegg.com
* http://www.cut-the-knot.org/pythagoras/RationalTrig/CutTheKnot.shtml
* http://farside.ph.utexas.edu/euclid.html

The computer language used is Python.


But I don't know the computer language Python
=============================================

You don't need to know Python to do basic calculations. The syntax is
designed to be somewhat simple. Please see the examples. As long as you can
start up a python interpreter on your machine, you should be OK. See
http://www.python.org to download a python interpreter for your computer. 
Once you can get to the screen where you type 
	
	print 'hello world'

then you will be ready to use piliko. Just put piliko.py in the proper
folder and you can load it with this command:

	from piliko import *

Examples
========

Example 1:

	from piliko import *

	p1 = point(0,0)
	p2 = point(3,0)
	p3 = point(0,4)
	print p1,p2,p3

	L1 = line( p1, p2 )
	L2 = line( p1, p3 )
	s = spread( L1, L2 )
	print s

Result:

	[0,0] [3,0] [0,4]
	1

Example 2:

	from piliko import *

	v1 = vector(3,0)
	v2 = vector(0,4)
	print v1, v2

	q1 = quadrance( v1 )
	q2 = quadrance( v2 )
	print q1, q2

	s = spread( v1, v2 )
	print s

Result:

	(3,0) (0,4)
	9 16
	1

Example 3:

	p1,p2,p3,p4 = point(0,0),point(25,0),point(50,0),point(100,0)
	print is_harmonic_range( p1, p2, p3, p4 )

More examples can be found in test.py. To run it:

	python test.py

Copyright License
=================

This code is free for use under a basic BSD-style Open Source Software 
license as described in the LICENSE file.
