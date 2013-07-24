piliko
======

Piliko is a very, very, very basic implementation of some formulas from 
Rational Trigonmetry in a computer language. 

This package is not affiliated with, nor endorsed in any way by Norman J 
Wildberger, who developed Rational Trigonometry. For more info, check these
websites:

 *https://www.youtube.com/user/njwildberger
 *http://web.maths.unsw.edu.au/~norman/
 *http://www.wildegg.com
 *http://www.cut-the-knot.org/pythagoras/RationalTrig/CutTheKnot.shtml
 *http://farside.ph.utexas.edu/euclid.html

The computer language used is Python.

Current status
==============

alpha level, currently does very little and/or nothing. 

Examples
========

Example 1:

	from piliko import *

	# note ---> we use the line equation ax+by+c = 0
	L1 = line(1,-2,3) 
	L2 = line(4,-3,7)
	s = spread(L1,L2)
	print L1, L2, s

Result:

	<1:-2:3> <4:-3:7> 1/5

Example 2:

	v1 = vector(3,0)
	v2 = vector(0,4)
	q1 = quadrance( v1 )
	q2 = quadrance( v2 )
	s = spread( v1, v2 )
	print v1, v1, q1, q2, s

Result:

	(3,0) (3,0) 9 16 1

More examples can be found in test.py. To run it:

	python test.py

Copyright License
=================

This code is free for use under a basic BSD-style Open Source Software 
license as described in the LICENSE file.
