piliko
======

Piliko is a very, very, basic collection of Rational Geometry computer 
codes in the computer language called Python. It follows, roughly, the 
Rational Trigonometry in that it avoids irrational and transcendental 
numbers and functions, and the concepts of angle and distance are 
avoided.

Current status
==============

This code is 'alpha' level. It is highly experimental. It can do basic 
calculations, but the whole type system has not been thought out very 
carefully and many functions are partially or wholly unimplemented. 
Tests have not been created. There are no actual users at this time so
debugging, as you might imagine, has been minimal.

Plotting of pictures is only possible if your system has the 'matlpotlib'
python add-on packages installed.
 
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

Plotting pictures
=================

When the add-on 'matplotlib' package is installed on your system, you can do
some basic plotting of pictures. For example:

	t = triangle(point(0,0),point(4,3),point(2,5))
	oc,cc,nc = orthocenter(t),circumcenter(t),ninepointcenter(t)
	circ = circle( oc, blueq( oc, point(0,0 ) )
	plot_circle( circ )
	plot_points( oc,cc,nc )
	plot_triangle( t )
	plotshow()
        
Basic principle
===============

The program focuses on Rational Numbers as the basis for Geometry. This 
can be called a 'finitist' approach to geometry. There is a reason that 
many geometry packages use Rationals as opposed to floating point 
approximations and irrational and transcendental functions.

For many geometric operations, if you stick to Rationals and rational 
functions, the answers are exact, the issue of floating-point error 
disappears. Let's take a basic example.

Consider three points on a Cartesian plane:  

  Point1: 0 , 0.6
  Point2: 1 , 0.7
  Point3: 2 , 0.8

Now ask the question. Are they collinear? The obvious answer is 'yes'. I mean,
look at them! Draw them. It's pretty clear. What about algebra? Let's try it.
Look at the change in y vs the change in x. 

 Point1 to Point2: change in x = 1, change in y = 0.1
 Point2 to Point3: change in x = 1, change in y = 0.1

That's almost the definition of collinear points. They are on the same slope,
the same angle, whatever. If you were crawling up a mountain with those
elevations, you'd call it the same 'grade' of climb. If you drew triangles
between the points and the flat horizontal axis, they'd be identical. 

Now... lets do that again, but use 'floating point' numbers. 

First off, we need to realize the problem with place-value number 
systems. It's a bit of a mind-bender, because we have been using 
place-value systems since the beginning of civilization, even back to 
the Babylonians in ancient Mesopotamia, who used the base-60 place value 
system, to the Indians, who pioneered the use of '0' in the base-10 
system. But there is a fundamental issue when you are dealing with them 
that is a bit non-obvious, but highly important for questions of 
geometry.

For every place-value numebr system, there are numbers that can be represented
exactly in that system that cannot be represented exactly in another system. It
doesn't matter if you are using a computer or not, it's just impossible. It's
a limitation of the way that place-value number systems work with division. 

For example. 0.6 has no exact representation in binary numbers. Think about
it for a moment. It's so obvious but so profound and important. 

Lets take a simpler example. Consider that you want to divide a quantity into
3 parts. You want to take a 'third' of it. If your quantity is 'one', then 
you want the quantity 'one third'. 

How do you write that in decimals? You don't. You can't. Decimals cannot
express the concept of 'one third' exactly in a finite number of digits. Try it.

    0.3

OK. Good Try. But how can we test the 'quality' of our attempt to write one
third? Well, clearly, if you try to triple the answer, it should give you
the quantity that you were originally trying to divide. 

   0.3 multiplied by 3 gives 0.9. 

0.9 is not the same thing as one. 0.3 is not exactly 'one third'. Ok, 
what about 0.33?

   0.33 multiplied by 3 gives 0.99

Again. 0.99 is not 1. It's close, but it's 1 percent off. If you had a 
million people and you lost one percent of them, you lost 10,000 people! 
1 percent is not so good. Ok how about 0.33333333333?

  0.33333333333 multipled by 3 gives 0.9999999999

Ok. Thats still not one. Maybe you are thinking, but it's good enough! 
Surely! Well, it might be good enough for some things, but when we are 
dealing in geometry we have problems. And it doesn't change the fundamental
fact: You cannot represent the concept of 'one third' in a base-10 place
value number system. 

Now, if you had a 'trinary' number system, base 3, then you have no problem. 
In a trinary system, you only have 3 digits. 0,1,2. The first 'place' is
3 to the 0th power. The second place rperesents 3 to the first power, etc. 

   Decimal       Trinary
   0              0
   1              1
   2              2
   3             10
   4             11
   5             12
   6             20

Etc etc etc. A funny thing happens when you deal with fractional values, though.

   Decimal       Trinary
   0.1           ???? it's not 0.1
   0.2           ???? it's not 0.2
   
What, then, does 0.1 mean in Trinary? Why, in Decimal it means 10 to the 
minus-one power. In Trinary it means 3 to the minus one power. 

What is three to the minus one power?

   One Third.

   0.1

In other words, that number, 'one third', that we could not represent 
exactly in a decimal number system, even with an infinite number of 
digits, is exactly representable in the trinary number system with a 
single digit and a 'point'.

   Decimal                          Trinary 

   0.33333333333....infinity        0.1
   0.66666666666....infinity        0.2

Now. What does all this have to do with computers? There is no such 
thing as a trinary computer, after all. Actually there was. Some people 
built one, a long time ago, in a country that no longer exists, called 
the Soviet Union. But ok. Most modern computers are built with the 
binary number system, and most modern programming languages include a number
type called 'floating point' that uses that binary system. 

But just as there is no 'one third' in the decimal system, there is no 
'6 tenths' in the binary number system. Not if you wrote infinity digits
in binary. It just doesn't exist. You can get really close, but never exact.

Now lets go back to our original question. Consider these three points.

  Point1: 0 , 0.6
  Point2: 1 , 0.7
  Point3: 2 , 0.8

They have been given in Decimal format. That's what most human beings 
learn in school, the Decimal system. It's a great system. But let's look
what happens when we convert to floating point binary.

  Point1: 0 , 0.6
  Point2: 1 , 0.7
  Point3: 2 , 0.8

  Decimal         Binary
  0.6             
  0.7
  0.8  

What has happened? The computer has gone through a process called 
'approximation'. It has taken this decimal number 0.6, and found some 
binary floating point number that is really, really close to 0.6. How close?
Well, the floating point numbers in a computer usually have some set number
of 'bits' or 'binary digits' that they use. The 'double' type usually uses
about 53 bits. 

It's the same concept we dealt with when we used the Decimal number 
system to approximate 'one third'.

    Decimal
    0.3         < One digit of precision
    0.33        < Two digits of precision
    0.33333333  < Eight digits of precision

How many digits of precision do we use? If we use too many, we run out 
of paper to write with! And we run out of time to write. And we run out 
of pencil lead or ink or whatever. And our hands get tired. 

The computer has some of the same problems. It can't use a billion digits,
then it would take forever to do anything. It would grind to a halt. You 
could ask it what it was doing, and it would say "oh, I'm just trying to
get this One Third thing written out". So instead of that, the computer
builders have the computer use an Approximation using a certain number of 
digits of precision. 

So lets go back to our original question, again. Our three points, in Decimal:

  Decimal number system
  Point1: 0 , 0.6
  Point2: 1 , 0.7
  Point3: 2 , 0.8

And now their floating point, binary Approximations, generated by the computer:

  Binary number system
  Point1: 0 , 0.6
  Point2: 1 , 0.7
  Point3: 2 , 0.8

How did we figure out whether these three points were on a single line before?
We looked at the change in y vs the change in x. In the Decimal system, we had
this:

 Decimal system:
 Point1 to Point2: change in x = 1, change in y = 0.1
 Point2 to Point3: change in x = 1, change in y = 0.1

And we said, wow, OK, it's obvious they are all in a single line. But...let's
we aren't in decimal in anymore. Let's try the same thing using the binary
system approximations:

 Binary number system approximations:
 Point1 to Point2: change in x = 1, change in y =
 Point2 to Point3: change in x = 1, change in y = 

Notice the problem? The 'change in y' between these two points is no longer
identical! Sure, it's pretty close. But it's not the same. 

How then, can you know how close 'pretty close' is? Should it be one percent?
Oh wait, if you have 1 million people and you draw a line on a map that
is one percent off, you might have cut out 10,000 of those people. They might
complain to your office about being left out of the state or whatever.

How about one one millionth. That is pretty close, right? Well, what
if we aren't dealing with nice simple points like 1,0.6. What if we have
a problem like Point(0,0.0000000001) and Point(0.00000001,0.00000002)?
Points like that are often generated by algorithms that are full of repeated
chains of multiplications, divisions, scaling, rotation, and on and on. 

There are ways to deal with all of this, and make algorithms 'robust' for
floating point numbers.

However. That takes a lot of work. And it might not be portable between
systems because floating point works differently on different systems.
There are questions like Rounding Mode, precision, conversion to strings,
etc, that differ between systems. Then there are simply bugs in floating
point units. Then there are systems where the floating point is emulated
by software.

Compare this with using Rationals.

There is a funny thing about Rationals and their relationship to place value
number systems. 

Any number that can be expressed in any place-value system can be converted, 
exactly, to a Rational number. 

How is this possible you say? Think about it for a minute. Every 
place-value system, at it's heart, is just representing a sum of 
Rational numbers.

For example

  Decimal number system
  16.18 = 1 * 10 + 6 + 1/10 + 8/100
  
  Trinary number system
  1.21 = 1 + 2/3 + 1/9

  Binary number system
  10.1 = 1*2 + 0 + 1/2 

Now, any sum of rational numbers can, itself, be expressed as a single 
rational number.

  Decimal number system
  16.18 = 1 * 10 + 6 + 1/10 + 8/100  ---> 1618/100
  
  Trinary number system
  1.21 = 1 + 2/3 + 1/9  ----> 9/9+6/9+1/9 --> 16/9

  Binary number system
  10.1 = 1*2 + 0 + 1/2  ----> 2+1/2 --> 4/2+1/2 --> 5/2

That means that there is no number, anywhere, in any place-value system,
that can't be expressed exactly in Rationals. That includes the common
system used by Human Beings, the Decimal system, and the system used by
computers, the Binary System. 

Let's go back to the original question of three collinear points. Lets 
rewrite as Rationals.

  Decimals             Rationals
  Point1: 0 , 0.6   -> 0/1 , 6/10    
  Point2: 1 , 0.7   -> 1/1 , 7/10
  Point3: 2 , 0.8   -> 2/1 , 8/10 

What does our calculation of 'change in x vs change in y' look like now?

 Decimal system:
 Point1 to Point2: change in x = [1/1] change in y = [1/10]
 Point2 to Point3: change in x = [1/1] change in y = [1/10]

Now that is interesting. The differences are exact. Just like when we 
originally compared them using the decimal system. 

Now you might ask... why not just use some kind of Computerized form of 
Decimal arithemtic? Several systems have done that over the years for 
money. Imagine the budget of a modern country, which numbers in the 
trillions. You cannot afford to be 'off' by a floating-point issue 
there. You can't "approximate" currency amounts, they have to balance 
exactly in the books. So there are computerized decimal systems.

But we aren't doing currency. We are doing Geometry. Remember our old friend
"one third"? What if you wanted to divide a line segment into three equal
pieces? You can't do that in the Decimal system, not without Approximation. 

That's what makes Rationals so cool. You can divide by anything, and you 
get the exact answer, and that answer is a Rational. You don't have to 
approximate it. That is called the concept of being 'closed' under 
division. You stick a Rational in, you get a Rational out, and it's 
exact. No place-value system is closed under division. But Rationals 
are.

Another way to think about it is to compare it to some other type of 
data used in life. Imagine if you had a database that could look up the 
addresses of your customers, but not exact addresses, only 'approximate' 
addresses. Would that be good enough? What if you had a word processing 
program that could only 'approximately' print out what you had typed 
into the machine. This is what the situation is with Place-value number 
systems in regards to the operations of multiplication and division. You 
can perform operations on them, but get a result that is impossible to 
represent in that system exactly, so you have to approximate.

Why does this link so close to Geometry? Consider the activities of 
Geometry that involve multiplication and /or division. 

 Lets list a few:
   
   Assuming only points with rational coordinates:
   Determine if 3 points are on a single line
   Determine if 3 lines are concurrent in a single point
   Determine if two lines have the same 'slope'
   Find the intersection of two lines
   Find the intersection of a line with a polygon
   Find the intersection of two polygons
   Determine if a point is inside or outside a polygon
   Find the area of a polygon

You can do all of these operations in floating point, by approximation, 
but you have to insert special code to deal with the question of 
inexactness that is inherent to place-value systems and floating point. 
If you choose Rationals, then you don't need to worry about 
approximation for any of those algorithms.

So this is the basic philosophy behind why Rationals might be chosen for 
use in Geometry instead of floating point binary. However, it is not the 
whole story. Lets consider some other operations.

   Determine the intersection of a line with a circle.
   Determine the distance between two points.
   Determine the angle between two lines.
   Determine the area of a circle

None of those can be done with Rational Numbers alone. Rationals are not 'closed'
under any of those operations. In particular, the following concepts destroy
the concept of Rationals being exact:

   Pi
   Sine
   Cosine
   Square Root
   Tangent
   Arcsin
   Arctangent
   Cube Root

And on and on and on. Those operations cannot be performed alone with 
rationals, and therefore many Geometric operations are impossible if one 
is restricted to Rationals. An extremely simple example is as follows:

   Consider two points, 0,0 and 1,1
   Find the intersection of a line and a circle
   Find the distance between them
   Find the radius of a circle passing through that point
   Find the angle between that point and the horizontal axis
   Find the area of said circle
   Find the area under a curve

The answers, of course, are things like sqrt(2), 45 degrees, and Pi, 
none of which can be derived or expressed with Rational numbers. This is 
where the true genius of the place-value systems comes in. Their ability 
to approximate the infinite and to grasp hold of the cloudy ambiguous 
nature of numbers like Pi, is an amazing thing. But. It's still an 
approximation.

Does that mean there is no Geometry without irrationals and 
Transcendentals? No, remember all those things we Could Do with only 
Rationals? Intersections? Collinearity?

The question, then, becomes, how far can we go with Rationals alone? 
What all can we do, without having to resort to approximations? The
answer is, a large amount... larger than you might think. 

And the other part of the answer is.... that if we approximate certain 
items using rationals as a basis, then we can sort of 'translate' some 
of the items from the approximate world, into the rational world, and 
perform algorithms on these approximations but without worrying about 
the algorithm breaking down due to floating point.

For example. Any conic curve can be approximated very well by rational 
parameterization (finding rational points on the curve). Bezier curves 
can be approximated by rational points. And thus, truetype(TM) fonts. 
Bernoulli's leminscate has a rational paramterization. Also a large 
number of polynomial curves can be parameterized by rational points. 
There are even people working algorithms to create rational 
paramterizations automatically. There even are rational analogues for 
rotation.

There are also rational parameterizations for many of our favorite 3 
dimensional objects, like spheres, toruses, hyperbolic sheets, 
non-circle based toruses, dumbbells, and there are even people who have 
worked out rational parameterizations of 3 dimensional 'knot' shapes.

It may be even possible to create anlogues of geometry algorithms (like 
Catmull Clark subdivision or Delaunay triangulation) using rational 
points and rational functions.

Howevere there will always be things that Rationals are 'bad at'. For 
example, if you get rid of angles, you can't add two angles together 
with simple addition. You have to use 'spread polynomials' instead.

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
