/* ratalg.hpp Copyright (c) 2013, Don Bright ( http://github.com/donbright )
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

  Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

  Redistributions in binary form must reproduce the above copyright notice, this
  list of conditions and the following disclaimer in the documentation and/or
  other materials provided with the distribution.

  Neither the name of the organization nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

/* RatAlg.hpp Rational numbers algebra and geometry codes.

For certain algorithms rational numbers offer some good tradeoffs vs
floating point. For any algorithm that doesn't involve irrational or
transcendental functions or numbers, the results are exact, without
approximation issues or 'numerical instability'. The downside is that
Rationals are often slower in certain situations.

Care should be taken converting coordinates from non-rational to
Rationals. For example the conversion from double->rational is exact,
without any approximation, but rational->double is not exact. It is an
approximation. That is because doubles in the binary number system
cannot represent, exactly, a large set of numbers, for example 1/3. This
can destroy the topology of a shape, producing errors. See the general
literature for more info.

Code style is Go-ish, i.e. no templates, no exceptions, no inheritance.

Rationals are represented using the Free Software Foundation's GMP library,
which stores Rationals as a pair of Big Integers.
*/

#include <gmpxx.h>
#include <vector>
#include <algorithm>

/* orientation - do the vertices of a polygon go clockwise or
 counterclockwise? for example, if a ladybug was walking the vertices in order?
 It will appear to have a different orientation depending on which side
you look. If it appears CounterClockwise that is considered the
'outside' or 'front' of the polygon, while if it appears Clockwise then
you are looking at the 'inside' or 'back'. */
typedef enum {
	CLOCKWISE = -1,
	COUNTERCLOCKWISE = 1,
	ANTICLOCKWISE = 1,
	NONE = 0
} orientation_t;

// for projection info, see 'struct point' documentation below
typedef enum {
	XYPLANE, YZPLANE, XZPLANE,
	YXPLANE, ZYPLANE, ZXPLANE,
	XLINE, YLINE, ZLINE,
	AT_INFINITY, UNKNOWN, NULLITY
} projection_t;

/* struct point represents a point in 3d space.

how does projection work? each point carries a 'projection' value. the
algorithms can thus deal with 3d-points as though they were
2-dimensional points 'projected' on to one of the three simple planes,
xy, yz, or xz, but without actually doing any projection or switch of data
type from 3d to 2d.

Example. Let's take a quadrilateral and split it into 2 triangles. It's
3d coordinates are 0,0,0 0,0,1 0,1,1 0,1,0. Our algorithm expects x,y so
we can set 'projection' to the 'yz' plane. now accessing the point
coordinates throug projected_x() and projected_y() will make the points
appear as: 0,0 0,1 1,1 1,0 and we can apply 2-d algorithms to the polygon.

Now there is another layer to this. Consider the question of Polygon
Orientation, whether a Ladybug walking the polygon points would have to
turn mostly 'counter clockwise' or mostly 'clockwise'. If we do yet
another projection, of x->y and y->x, essentially 'flipping' the polygon
over the diagonal line x=y, we essentially 'flip' the orientation of
the polygon from clockwise to counterclockwise, or vice versa.

Since every single function depends on the use of 'side()', essentially
we can keep the algorithms themselves simple, as though they always were
being given a conter-clockwise 2 dimensional polygon with x,y coordinates.

Note this only works on algorithms that don't create new points, nor
change the existing points.

Also there is a projection reserved for points 'at infinity', which can be
also thought of as points that are the result of algorithms that have
divide-by-zero, for example the 'meet' of two paralell lines. */
struct rational_point {
        mpq_class x,y,z;
        rational_point( double x, double y, double z );
        rational_point( const rational_point &p );
	projection_t projection;
	mpq_class projectedx() const;
	mpq_class projectedy() const;
	void set_projectedz( mpq_class a );
};

struct rational_line { // 2d equation ax+by+c=0
	mpq_class a,b,c;
	rational_line( const rational_point &p1, const rational_point &p2 );
};

struct rational_plane { // plane equation ax+by+cd=0
        mpq_class a,b,c,d;
        rational_plane( const rational_point &p1, const rational_point &p2, const rational_point &p3 );
};

bool operator==( const rational_point &p1, const rational_point &p2 ) {
	return ( p1.x==p2.x && p1.y==p2.y && p1.z==p2.z );
}

bool operator!=( const rational_point &p1, const rational_point &p2 ) {
	return ( p1.x!=p2.x || p1.y!=p2.y || p1.z!=p2.z );
}

bool sign( mpq_class &a ) {
	if (a<0) return -1;
	else if (a==0) return 0;
	else return 1;
}

// build a rational 3 dimensional point from 3 double-float numbers
// mpq_class does implicit exact conversion from double to rational.
rational_point::rational_point( double x, double y, double z ) {
	this->x = x;
	this->y = y;
	this->z = z;
	this->projection = XYPLANE;
}

rational_point::rational_point( const rational_point &p ) {
	this->x=p.x; this->y=p.y; this->z=p.z; this->projection=p.projection;
}

/* return the 'projected' version of the point's x,y coordinate. see the
documentation of 'struct point' for more info about projection. */
mpq_class rational_point::projectedx() const {
	if (this->projection==XYPLANE ) return this->x;
	else if (this->projection==XZPLANE) return this->x;
	else if (this->projection==YZPLANE) return this->y;
	else if (this->projection==YXPLANE) return this->y;
	else if (this->projection==ZXPLANE) return this->z;
	else if (this->projection==ZYPLANE) return this->z;
	else return mpq_class(0);
}
mpq_class rational_point::projectedy() const {
	if (this->projection==XYPLANE) return this->y;
	else if (this->projection==XZPLANE) return this->z;
	else if (this->projection==YZPLANE) return this->z;
	else if (this->projection==YXPLANE) return this->x;
	else if (this->projection==ZXPLANE) return this->x;
	else if (this->projection==ZYPLANE) return this->y;
	else return mpq_class(0);
}
void rational_point::set_projectedz( mpq_class a ) {
	if (this->projection==XYPLANE ) this->z = a;
	else if (this->projection==XZPLANE) this->y = a;
	else if (this->projection==YZPLANE) this->x = a;
	else if (this->projection==YXPLANE) this->z = a;
	else if (this->projection==ZXPLANE) this->y = a;
	else if (this->projection==ZYPLANE) this->x = a;
	else this->x = this->y = this->z = mpq_class(0);
}



/* build a line equation from two points. Equation form is ax+by+c = 0.
Given two points, p1 and p2, consider a third point 'p'. Use the area of
a paralellogram formed by two vectors (p-p1) and (p2-p1), which is
wedge( p-p1, p2-p1 ), also called determinant, and many other names.  When
this area is zero, we can find the equation easily.

    | x-x1  y-y1|
det |x2-x1 y2-y1| = 0 -->  (x-x1)(y2-y1)-(y-y1)(x2-x1)=0
                          x(y2-y1)-y(x2-x1)-x1(y2-y1)+y1(x2-x1)=0
                          a=(y2-y1) b=-(x2-x1) c=-x1(y2-y1)+y1(x2-x1)
*/
rational_line::rational_line( const rational_point &p1, const rational_point &p2 )
{
	mpq_class x21,y21;
	x21 = p2.projectedx() - p1.projectedx();
	y21 = p2.projectedy() - p1.projectedy();
	this->a = y21;
	this->b = -x21;
	this->c = -p1.projectedx()*y21+p1.projectedy()*x21;
}

/* build a plane equation from three points. Equation form is
ax+by+cz+d=0 We use the a similar theory to the 'line' construction
above, but instead of the area of a parallelogram formed by 2 vectors,
we are using the volume of a parellellapiped formed by 3 vectors.

From Theory+Problems of Vector Analysis, Murray R Spiegel, 1959 Schaum
Publishing, New York. The volume of a parallellapiped v1,v2,v3 is
v1 dot v2 cross v3, or the 3x3 matrix Determinant of v1,v2,v3 as rows or
columns. So, if 3 vectors are coplanar, the volume of the piped will be 0.

Given 3 points, p1,p2,p3, consider the fourth point p. They form 3
vectors, (p-p1), (p2-p1) and (p3-p1). If p is coplanar to 3 points
p1,p2,p3, the area of paralellapiped formed by those three vectors is 0.
Thus v1 dot v2 cross v3 = 0. Expand this using Determinant math and
a,b,c,d become clear.

    | x-x1  y-y1  z-z1|
det |x2-x1 y2-y1 z2-z1| = 0 --> x[(y2-y1)(z3-z1)-(y3-y1)(z2-z1)] + y[ ... = 0
    |x3-x1 y3-y1 z3-z1|         a=(y2-y1)(z3-z1)-(y3-y1)(z2-z1) b=... c=...

On Orientation:

An interesting note. Given 3 points, M,N,P, if you feed them in the
reverse order, like P,N,M, then the resulting a,b,c,d will be 'flipped'
in sign. For example

M,N,P = [0,0,1],[1,0,1],[0,1,1]
plane(M,N,P) -> <0:0:1:-1>
plane(P,N,M) -> <0:0:-1:1>

*/
rational_plane::rational_plane( const rational_point &p1, const rational_point &p2, const rational_point &p3 )
{
	mpq_class x21,y21,z21,x31,y31,z31,dx,dy,dz;
	x21 = p2.x - p1.x;
	y21 = p2.y - p1.y;
	z21 = p2.z - p1.z;
	x31 = p3.x - p1.x;
	y31 = p3.y - p1.y;
	z31 = p3.z - p1.z;
	this->a = y21*z31 - z21*y31;
	this->b = z21*x31 - x21*z31;
	this->c = x21*y31 - y21*x31;
	dx = p1.x*( z21*y31 - y21*z31 );
	dy = p1.y*( x21*z31 - z21*x31 );
	dz = p1.z*( y21*x31 - x21*y31 );
	this->d = dx+dy+dz;
};

/* meet(line,line)
find the 2d intersection point of two lines. if they are paralell (or the same)
the return point will have a projection of 'AT_INFINITY'. The math is like so:
Start with two line equations.
  a1 x + b1 y + c1 = 0   << multiply by 1/b1
  a2 x + b2 y + c2 = 0   << multiply by 1/b2
  a1/b1 x + y + c1/b1 = 0
  a2/b2 x + y + c2/b2 = 0       ... now subtract eqn2 from eqn1
  (a1/b1-a2/b2)x + c1/b1-c2/b2 = 0 ... now mult by b1b2
  (a1*b2-a2*b1)x + c1*b2-c2*b1 = 0 ... now solve for x
  x = c2b1-b2c1 / a1b2-a2b1 ... now do the same process with y
  y = c2a1-c1a2 / a2b1-a1b2 ... notice denominators are inverses */
rational_point meet( const rational_line &l1, const rational_line &l2 ) {
	rational_point result(0,0,0);
	mpq_class x_denominator = l1.a*l2.b-l2.a*l1.b;
	result.x = l1.b*l2.c-l2.b*l1.c;
	result.y = l1.a*l2.c-l2.a*l1.c;
	if (x_denominator==0) {
		x_denominator = mpq_class(1,10000000);
		result.projection = AT_INFINITY;
	} else {
		result.projection = UNKNOWN;
	}
	result.x /= x_denominator;
	result.y /= -x_denominator;
	return result;
}

/* given point p0, project it back up into the given plane.
in other words, given x, and y, find z. the math goes like this:
ax+by+cz+d=0  -->  z=(-d-ax-by) / c  -->  if c==0, point=At_infinity
 */
void deproject( rational_point &p0, const rational_plane &pl ) {
	mpq_class z = -pl.d-pl.a*p0.projectedx()-pl.b*p0.projectedy();
	if (pl.c==0) {
		p0.projection=AT_INFINITY;
		z *= 1000000;
	} else {
		z /= pl.c;
	}
	p0.set_projectedz( z );
}

/* figure out which plane, xy, yz, or xz, will make a good plane on which to
project the given near-planar 3d polygon for 2d processing. 'good'
means points won't be projected onto each other. for example imagine a
triangle with 3 points 0,0,0 0,1,0 1,0,0. you dont want to project it
sideways to YZ because it will just be a line segment and we can't do
stuff, like get it's area.*/
projection_t find_good_projection( const std::vector<rational_point> &pgon ) {
	const rational_point &p1 = pgon[(0)%pgon.size()];
	const rational_point &p2 = pgon[(1)%pgon.size()];
	const rational_point &p3 = pgon[(2)%pgon.size()];
	rational_plane pl( p1, p2, p3 );
	mpq_class q1 = pl.a*pl.a+pl.b*pl.b;
	mpq_class q2 = pl.b*pl.b+pl.c*pl.c;
	mpq_class q3 = pl.c*pl.c+pl.a*pl.a;
	if (std::min(q1,std::min(q2,q3))==q1) return XYPLANE;
	else if (std::min(q1,std::min(q2,q3))==q2) return YZPLANE;
	return XZPLANE;
}

// figure out the best one-dimensional projection so that the coordinates
// wont be on top of each other. for info on projection please see the docs
// for 'struct rational_point'.
projection_t find_good_projection_1d( const rational_point &p1, const rational_point &p2 ) {
	mpq_class dx = p1.x-p2.x;
	mpq_class dy = p1.y-p2.y;
	mpq_class dz = p1.z-p2.z;
	mpq_class max = std::max(dx,std::max(dy,dz));
	if (max==dx) return XLINE;
	else if (max==dy) return YLINE;
	return ZLINE;
}

/* find the intersection of two one dimensional line segments. Some examples:
     Intersecting     Non-intersecting   Intersect=A1-A2   Non-intersection
    A1  B1  A2   B2    A1  A2  B1   B2   B1   A1 A2   B2   B1  B2  A1   A2
    .____.__.____.     .____.  .____.    .____.__.____.    .____.  .____.
*/
std::pair<rational_point,rational_point> meet_segments_1d(const rational_point &a1,const rational_point &a2,const rational_point &b1,const rational_point &b2 ){
/*	const rational_point alo = std::min(a1,a2);
	const rational_point ahi = std::max(a1,a2);
	const rational_point blo = std::min(b1,b2);
	const rational_point bhi = std::max(b1,b2);
	std::vector<rational_point> v;
	v.push_back( a1 );
	v.push_back( a2 );
	v.push_back( b1 );
	v.push_back( b2 );
//	std::sort( v.begin(), v.end(), getprojectedx );
	const rational_point *lo = &v[1];
	const rational_point *hi = &v[2];
	if (v[1]<blo && v[2]>ahi) {
		lo->projection=NULLITY;
		hi->projection=NULLITY;
	} else if (v[1]<alo && v[2]>bhi) {
		lo->projection=NULLITY;
		hi->projection=NULLITY;
	}
*/
	rational_point a(0,0,0),b(0,0,0);
	std::pair<rational_point,rational_point> m(a,b);
	return m;
}

// true if p lies on plane, false otherwise
bool meet( const rational_plane &pl, const rational_point &p ) {
	if (pl.a*p.x + pl.b*p.y + pl.c*p.z + pl.d == 0) return true;
	return false;
}

/* true if the given points are coplanar, false otherwise.
 for 0,1, or 2 given points, return true. */
bool coplanar( const std::vector<rational_point> &points ) {
	if (points.size()<3) return true;
	rational_plane plane(points[0],points[1],points[2]);
	for (size_t i =  3  ; i < points.size(); i++) {
		if (!meet( plane, points[i] )) return false;
	}
	return true;
}
bool coplanar(const rational_point &p1,const rational_point &p2,const rational_point &p3,const rational_point &p4 ) {
	rational_plane plane(p1,p2,p3);
	return meet(plane,p4);
}

/*
side()

Given 3 points, find whether p3 is a 'right turn' or 'left turn' from
the line from p1 to p2. if result is >0, turn is left. <0 right.
0=collinear this is similar to several concepts, including 'winding', or
'side', or the 'wedge' of the bivector( p3-p2, p2-p1 ), or the
'determinant' of (p3-p2, p2-p1). or the cross product of 3d vectors...
or the signed paralellogram area of (p3-p2)(p2-p1).

'projection' allows us to deal with 3d points as if they were 2d.
to understand the 'projection' concept please see the documentation of
'struct point'. */
mpq_class side( const rational_point &p1, const rational_point &p2, const rational_point &p3 ) {
	mpq_class x1 = p2.projectedx() - p1.projectedx();
	mpq_class y1 = p2.projectedy() - p1.projectedy();
	mpq_class x2 = p3.projectedx() - p2.projectedx();
	mpq_class y2 = p3.projectedy() - p2.projectedy();
	return x1*y2-x2*y1;
}

/* Find the intersection of two 3d line segments, assume coplanar.
Math: Consider two line segments

Non-intersecting:      Intersecting:        Intersecting paralell:
    A2   B1____B2              |B1             A1  B1  A2   B2
     /                         |               .____.__.____.
    /                  A1---------A2
   /                           |
  A1                           B2

For non-paralell, imagine running the 'side()' function, using A's
endpoints and one point of B. Now do it again with the other point of B.
The do the same with B, using the endpoints of A. If 'side' shows that
both segments endpoints lie on opposite sides of the other segment, you
have an intersection.

This will fail for paralell segments so we treat them differently (see meet_1d)

*/
std::pair<rational_point,rational_point> meet_segments_2d( const rational_point &a1,const rational_point &a2,const rational_point &b1,const rational_point &b2 ) {
	mpq_class s1 = side(a1,a2,b1);
	mpq_class s2 = side(a1,a2,b2);
	mpq_class s3 = side(b1,b2,a1);
	mpq_class s4 = side(b1,b2,a2);
	rational_point pm1(0,0,0),pm2(0,0,0);
	std::pair<rational_point,rational_point> m(pm1,pm2);
	if (s1==s2==s3==s4==0) {
		rational_point pa1(a1),pa2(a2),pb1(b1),pb2(b2);
		projection_t newp = find_good_projection_1d( a1, a2 );
		pa1.projection=pa2.projection=pb1.projection=pb2.projection=newp;
		m = meet_segments_1d( a1, a2, b1, b2 );
	} else if (sign(s1)==-1*sign(s2) && sign(s3)==-1*sign(s4)) {
		rational_line l1( a1, a2 );
		rational_line l2( b1, b2 );
		m.first = meet( l1, l2 );
		m.second = m.first;
	} else {
		m.first.projection = NULLITY;
		m.second.projection = NULLITY;
	}
	return m;
}

// same as side(), but with different human language idiom
orientation_t orientation( const rational_point &p1, const rational_point &p2, const rational_point &p3 )
{
	if (side(p1,p2,p3)>0) return COUNTERCLOCKWISE;
	else if (side(p1,p2,p3)<0) return CLOCKWISE;
	return NONE;
}

// 2d collinear test
bool collinear( const rational_point &p1, const rational_point &p2, const rational_point &p3 ) {
	return (side(p1,p2,p3)==0);
}

/* 'orientation' is the concept of the ordering of points in a polygon. if
 a ladybug ran around the pgon in the order the points are given, and she turned
 mostly right, thats clockwise. if she turned mostly left, thats
 counterclockwise. if she only turned 'about face' (180 degrees) its not
 really a polygon, its a bunch of collinear points.

 this is the '2d' version.

 FIX Me - some self intersecting polygons have orientation 0 but are not collinar
 */
orientation_t orientation( const std::vector<rational_point> &pgon )
{
	int orientation = 0;
	if (pgon.size()<3) return NONE;
	for (size_t i=0;i<pgon.size();i++) {
		const rational_point &p1 = pgon[(i+0)%pgon.size()];
		const rational_point &p2 = pgon[(i+1)%pgon.size()];
		const rational_point &p3 = pgon[(i+2)%pgon.size()];
		if (collinear(p1,p2,p3)) orientation += 0;
		else if (side(p1,p2,p3)>0) orientation += 1;
		else orientation -= 1;
	}
	if (orientation>0) return COUNTERCLOCKWISE;
	else if (orientation<0) return CLOCKWISE;
	else return NONE;
}

/* flip the orientation of the given polygon from counterclockwise to
clockwise or vice versa. we do this without modifying the polygon's
point coordinates. instead we switch the 'projection' of each point so that
projectedx() and projectedy() will be swapped with each other. this
essentially flips the polygon over the diagonal line x=y, which means
that side() and thus orientation() will also be flipped. please see the
documentation of 'struct rational_point' for more info on projection */
void flip_orientation( std::vector<rational_point> &pgon )
{
	for (size_t i=0;i<pgon.size();i++) {
		if (pgon[i].projection==XYPLANE) pgon[i].projection=YXPLANE;
		else if (pgon[i].projection==YZPLANE) pgon[i].projection=ZYPLANE;
		else if (pgon[i].projection==XZPLANE) pgon[i].projection=ZXPLANE;
		else if (pgon[i].projection==YXPLANE) pgon[i].projection=XYPLANE;
		else if (pgon[i].projection==ZYPLANE) pgon[i].projection=YZPLANE;
		else if (pgon[i].projection==ZXPLANE) pgon[i].projection=XZPLANE;
	}
}

// is the point p inside the triangle formed by t1,t2,t3?
bool inside( const rational_point &t1, const rational_point &t2, const rational_point &t3, const rational_point &p )
{
	if (side(t1,t2,p)>0 && side(t2,t3,p)>0 && side(t3,t1,p)>0) return true;
	return false;
}

// is the point on the line segments of the triangle formed by t1,t2,t3?
// or is it one of the corners?
bool meet( const rational_point &t1, const rational_point &t2, const rational_point &t3, const rational_point &p )
{
	if ( t1==p || t2==p || t3==p ) return true;
	if (side(t1,t2,p)==0 && side(t2,t3,p) >0 && side(t3,t1,p) >0) return true;
	if (side(t1,t2,p) >0 && side(t2,t3,p)==0 && side(t3,t1,p) >0) return true;
	if (side(t1,t2,p) >0 && side(t2,t3,p) >0 && side(t3,t1,p)==0) return true;
	return false;
}

/* returns true if the given polygon has any points inside of the given
triangle formed by t1,t2,t3.  also returns true if the given polygon has
any points lying directly on the lines of the given triangle. returns
false otherwise. note that polygon points that are the same as one of the 3
corners of the triangle are not considered encroaching */
bool encroaches( const rational_point &t1, const rational_point &t2, const rational_point &t3, const std::vector<rational_point> &pgon )
{
	for (size_t i=0;i<pgon.size();i++) {
		const rational_point &p = pgon[i];
		if (inside(t1,t2,t3,p)) return true;
		if (t1!=p && t2!=p && t3!=p && meet(t1,t2,t3,p)) return true;
	}
	return false;
}

/* clip a single ear triangle off of the given polygon, copying the ear points
 to 'triangle'. pgon will lose a single point. return 0 on success, 1 on error. */
int clip_ear( std::vector<rational_point> &triangle, std::vector<rational_point> &pgon )
{
	triangle.clear();
	if (pgon.size()<3) return 0;
	std::vector<rational_point>::iterator pi = pgon.begin();
	for (size_t i=0;i<pgon.size();i++,pi++) {
		rational_point &t1 = pgon[(i+0)%pgon.size()];
		rational_point &t2 = pgon[(i+1)%pgon.size()];
		rational_point &t3 = pgon[(i+2)%pgon.size()];
		if (orientation(t1,t2,t3)==COUNTERCLOCKWISE) {
			if (!encroaches(t1,t2,t3,pgon)) {
				triangle.push_back(t1);
				triangle.push_back(t2);
				triangle.push_back(t3);
				if (pi==pgon.end()) pi=pgon.begin();
				else pi++;
				pgon.erase( pi );
				break;
			}
		}
	}
	if (triangle.size()!=3) return 2;
	return 0;
}

/* convert a near-planar 3d polygon into a sequence of triangles. assume
 it is simple, non-self-intersecting, and no holes. return 0 on
 success, !0 on error; input polygon is destroyed and will have size() 0 */
int triangulate_near_planar_polygon( std::vector<rational_point> &pgon, std::vector< std::vector< rational_point > > &triangles ) {
	projection_t oldproj = pgon[0].projection;
	projection_t goodproj = find_good_projection( pgon );
	for (size_t i=0;i<pgon.size();i++) pgon[i].projection = goodproj;
	if (orientation(pgon)==CLOCKWISE) flip_orientation( pgon );
	while ( pgon.size()>2 ) {
		std::vector<rational_point> newtriangle;
		int err = clip_ear( newtriangle, pgon );
		if (err) return err;
		triangles.push_back( newtriangle );
	}
	for (size_t i=0;i<pgon.size();i++) pgon[i].projection = oldproj;
	return 0;
}





/* Testing of above code
To test compile an including c++ file with test_ratalg_hpp defined, like so:
echo '#include "ratalg.hpp"' >> t.cc; g++ t.cc -lgmpxx -lgmp -Dtest_ratalg_hpp*/
#ifdef test_ratalg_hpp

#include <assert.h>
#include <sstream>
#include <iostream>
#include <time.h>

std::ostream &operator<<(std::ostream &stream, const rational_point &p ) {
	stream << "["<<p.x<<","<< p.y << "," << p.z << ":"<< p.projection << "]";
	return stream;
}
std::ostream &operator<<(std::ostream &stream, const rational_line &l ) {
	stream << "<"<<l.a<<":"<< l.b << ":" << l.c << ">";
	return stream;
}

static int svg_xcursor = 100;
static int svg_ycursor = 100;
std::string dumpsvg( std::vector<rational_point> &pgon, std::string color ) {
	std::stringstream s;
	s << "<!--";
	for (size_t i=0;i<pgon.size();i++) { s << pgon[i]; }
	s << " orientation:" << orientation( pgon ) << "-->\n";
	s << "<polygon fill='none' stroke='" << color << "' points='";
	for (size_t i=0;i<pgon.size();i++) {
		pgon[i].projection=XYPLANE;
		s << pgon[i].projectedx().get_d()+svg_xcursor << ","
		  << pgon[i].projectedy().get_d()+svg_ycursor << " ";
	}
	s << "'/>\n";
	return s.str();
}

void test() {
	rational_point p1( 0, 0, 1 );
	rational_point p2( 1, 0, 1 );
	rational_point p3( 0, 1, 1 );
	rational_point p4( 0, 1, 1 );
	rational_point p5( 1, 2, 3 );
	rational_point p6( -1, -2, 1 );
	rational_point p7( -1, 2, 1 );
	rational_point p8( 0, 0, 0 );
	rational_point p9( 1, 0, 0.6 );
	rational_point p10( 0, 1, 0.6 );
	rational_point p11( 1, 1, 1.2 );
	rational_point p12( 1, 2, 1 );
	rational_point p13( 3, 6, 1 );
	assert( p3 == p4 );
	assert( p1 != p2 && p2 != p3 && p3 != p1 );
	assert( p5.projection == XYPLANE );
	assert( p5.projectedx()==1 && p5.projectedy()==2 );
	p5.projection = YZPLANE;
	assert( p5.projectedx()==2 && p5.projectedy()==3 );
	p5.projection = XZPLANE;
	assert( p5.projectedx()==1 && p5.projectedy()==3 );
	p5.projection = XYPLANE;
	assert( p5.projectedx()==1 && p5.projectedy()==2 );
	rational_plane pl( p1, p1, p1 );
	assert( pl.a==0 && pl.b==0 && pl.c==0 );
	rational_plane pl2( p1, p2, p3 );
	assert( meet(pl2, p1) );
	assert( meet(pl2, p2) );
	assert( meet(pl2, p3) );
	assert( meet(pl2, p7) );
	assert( !meet(pl2, p11) );
	rational_plane pl3( p8, p9, p10 );
	assert( meet(pl3, p8) );
	assert( meet(pl3, p9) );
	assert( meet(pl3, p11) );
	assert( meet(pl3, p10) );
	assert( meet(pl3, p10) );
	assert( !meet(pl3, p1) );
	assert( !meet(pl3, p2) );
	assert( !meet(pl3, p3) );
	assert( !meet(pl3, p4) );
	//rational_point p1( 0, 0, 1 );
	//rational_point p2( 1, 0, 1 );
	//rational_point p3( 0, 1, 1 );
	assert( side(p1,p2,p3)>0 );
	assert( side(p3,p2,p1)<0 );
	assert( side(p1,p1,p1)==0 );
	assert( side(p1,p1,p2)==0 );
	assert( side(p2,p1,p2)==0 );
	assert( side(p1,p2,p1)==0 );
	assert( side(p1,p2,p2)==0 );
	//rational_point p8( 0, 0, 0 );
	//rational_point p9( 1, 0, 0.6 );
	//rational_point p10( 0, 1, 0.6 );
	assert( side(p8,p9,p10)>0 );
	assert( side(p10,p9,p8)<0 );
	assert( side(p10,p10,p10)==0 );
	assert( orientation(p8,p9,p10)==COUNTERCLOCKWISE );
	assert( orientation(p8,p9,p10)==ANTICLOCKWISE );
	assert( orientation(p10,p9,p8)==CLOCKWISE );
	assert( orientation(p10,p10,p10)==NONE );
	assert( collinear(p1,p1,p1) );
	assert( collinear(p1,p2,p1) );
	assert( collinear(p6,p12,p13) );
	std::vector<rational_point> pgon;
	pgon.push_back( p1 );
	pgon.push_back( p2 );
	pgon.push_back( p12 );
	pgon.push_back( p3 );
	assert( orientation( pgon ) == COUNTERCLOCKWISE );
	pgon.clear();
	pgon.push_back( p3 );
	pgon.push_back( p12 );
	pgon.push_back( p2 );
	pgon.push_back( p1 );
	assert( orientation( pgon ) == CLOCKWISE );
	pgon.clear();
	pgon.push_back( p6 );
	pgon.push_back( p12 );
	pgon.push_back( p13 );
	assert( orientation( pgon ) == NONE );
	rational_point p14( 0,0,0 );
	rational_point p15( -1,0,1 );
	rational_point p16( 0,-1,2 );
	rational_point p17( -0.2,-0.2,3 );
	rational_point p18( 0,-0.5,4 );
	rational_point p19( 1,0,0 );
	assert( inside( p14,p15,p16, p17 ) );
	assert( !inside( p14,p15,p16, p19 ) );
	assert( meet( p14,p15,p16, p14 ) );
	assert( meet( p14,p15,p16, p15 ) );
	assert( meet( p14,p15,p16, p16 ) );
	assert( meet( p14,p15,p16, p18 ) );
	assert( !meet( p14,p15,p16, p19 ) );

	std::vector<rational_point> pgon0;
	pgon0.clear(); pgon0.push_back( p18 );
	assert( encroaches( p14,p15,p16,pgon0 ) );
	pgon0.clear(); pgon0.push_back( p16 );
	assert( !encroaches( p14,p15,p16,pgon0 ) );
	pgon0.clear();
	pgon0.push_back( p14 ); pgon0.push_back( p15 ); pgon0.push_back( p16 );
	assert( !encroaches( p14,p15,p16,pgon0 ) );
	pgon0.clear(); pgon0.push_back( p14 );
	assert( !encroaches( p14,p15,p16,pgon0 ) );
	pgon0.clear(); pgon0.push_back( p14 );
	assert( !encroaches( p14,p15,p16,pgon0 ) );

	pgon0.clear();
	pgon0.push_back( p18 );
	pgon0.push_back( p16 );
	assert( encroaches( p14,p15,p16,pgon0 ) );

	rational_point p20( 0,0,0 );
	rational_point p21( 1,0,1 );
	rational_point p22( 1,1,2 );
	rational_point p23( 0,1,2 );
	pgon.clear();
	pgon.push_back( p20 );
	pgon.push_back( p21 );
	pgon.push_back( p22 );
	pgon.push_back( p23 );
	assert( orientation(pgon)==COUNTERCLOCKWISE );
	std::vector<rational_point> ear;

	assert( clip_ear( ear, pgon ) == 0 );
	assert( ear.size()==3 );
	assert( pgon.size()==3 );
	assert( orientation(ear)==COUNTERCLOCKWISE );
	assert( orientation(pgon)==COUNTERCLOCKWISE );
	assert( !encroaches(ear[0],ear[1],ear[2],pgon) );
	assert( !encroaches(pgon[0],pgon[1],pgon[2],ear) );

	std::vector<rational_point> ear2;
	assert( clip_ear( ear2, pgon ) == 0 );
	assert( ear2.size()==3 );
	assert( pgon.size()==2 );
	assert( orientation(ear2)==COUNTERCLOCKWISE );
	assert( orientation(pgon)==NONE );
	assert( !encroaches(ear2[0],ear2[1],ear2[2],pgon) );
	assert( !encroaches(pgon[0],pgon[1],pgon[2],pgon) );

	assert( !encroaches(ear2[0],ear2[1],ear2[2],ear) );
	assert( !encroaches(ear[0],ear[1],ear[2],ear2) );

	rational_point p30( 0,0,0 );
	rational_point p31( 1,0,0 );
	rational_point p32( 1,1,0 );
	rational_point p33( 0,1,0 );
	pgon.clear();
	pgon.push_back( p30 );
	pgon.push_back( p31 );
	pgon.push_back( p32 );
	pgon.push_back( p33 );
	assert( find_good_projection( pgon ) == XYPLANE );

	rational_point p34( 0,0,0 );
	rational_point p35( 0,1,0 );
	rational_point p36( 0,1,1 );
	rational_point p37( 0,0,1 );
	pgon.clear();
	pgon.push_back( p34 );
	pgon.push_back( p35 );
	pgon.push_back( p36 );
	pgon.push_back( p37 );
	assert( find_good_projection( pgon ) == YZPLANE );

	rational_point p38( 0,0,0 );
	rational_point p39( 1,0,0 );
	rational_point p40( 1,0,1 );
	rational_point p41( 0,0,1 );
	pgon.clear();
	pgon.push_back( p38 );
	pgon.push_back( p39 );
	pgon.push_back( p40 );
	pgon.push_back( p41 );
	assert( find_good_projection( pgon ) == XZPLANE );

	rational_point p50( -1,-1,0 );
	rational_point p51( 1,0,0 );
	rational_point p52( 1,1,0 );
	rational_point p53( 0,1,0 );
	pgon.clear();
	pgon.push_back( p50 );
	pgon.push_back( p51 );
	pgon.push_back( p52 );
	pgon.push_back( p53 );
	std::vector<std::vector< rational_point > > triangles;
	assert( orientation(pgon) == COUNTERCLOCKWISE );
	assert( triangulate_near_planar_polygon( pgon, triangles ) == 0 );
	assert( pgon.size()==2 );
	assert( triangles.size()==2 );
	std::vector<rational_point> t0 = triangles[0];
	std::vector<rational_point> t1 = triangles[1];
	assert( !encroaches( t0[0],t0[1],t0[2], t1 ) );
	assert( !encroaches( t1[0],t1[1],t1[2], t0 ) );
	assert( orientation(t0) == COUNTERCLOCKWISE );
	assert( orientation(t1) == COUNTERCLOCKWISE );

	// orientation flipping
	flip_orientation(t1);
	flip_orientation(t0);
	assert( orientation(t0) == CLOCKWISE );
	assert( orientation(t1) == CLOCKWISE );

	// 2d lines
	rational_point pa(0,0,0);
	rational_point pb(1,0,0);
	rational_point pc(1,1,0);
	rational_point pd(0,1,0);
	rational_line l1( pa, pb );
	rational_line l2( pb, pc );
	rational_line l3( pc, pd );
	rational_line l4( pd, pa );
	rational_point m1 = meet(l1, l2);
	rational_point m2 = meet(l2, l3);
	rational_point m3 = meet(l3, l4);
	rational_point m4 = meet(l4, l1);
	assert( m1 == pb &&  m2 == pc && m3 == pd && m4 == pa );
	rational_line l5( pa, pc );
	rational_line l6( pb, pd );
	rational_point m5 = meet(l5, l6);
	rational_point m6 = meet(l1, l6);
	assert( m5 == rational_point(0.5,0.5,0) );
	assert( m6 == pb );
	rational_point m7 = meet(l1,l3);
	rational_point m8 = meet(l2,l4);
	assert( m7.projection = AT_INFINITY );
	assert( m8.projection = AT_INFINITY );
}

// fibonacci type sequence, modulo hi-lo = pseudorandom number generator
static unsigned int r1 = 1, r2 = 1;
int rand(int lo,int hi) { r2 = r1+r2; r1 = r2-r1; return (r2 % (hi-lo))+lo; }

void fuzztest() {
	r2 = time(NULL);
	for (size_t i=0;i<10000;i++) {
		int x = rand(-10000,10000);
		int y = rand(-10000,1000000);
		int z = rand(-10000,10000);
		int x2 = rand(-10000,10000);
		int y2 = rand(-10000,10000);
		int z2 = rand(-10000,10000);
		int x3 = rand(-10000,10000);
		int y3 = rand(-10000,10000);
		int z3 = rand(-10000,10000);
		rational_point p1(x,y,z);
		rational_point p2(x2,y2,z2);
		rational_point p3(x3,y3,z3);
		rational_line l1( p1, p2 );
		rational_line l2( p2, p3 );
		rational_point pm = meet( l1, l2 );
		pm.projection = p1.projection;
		deproject( pm, rational_plane( p1, p2, p3 ) );
		//std::cout << "l1" << l1 << "l2" << l2 << p1 << p2 << p3 << "m:" << pm << "\n";
		assert( pm == p2 );
		assert( coplanar( pm, p1, p2, p3 ) );
		assert( meet( p1, p2, p3, pm ) );
	}
}

void fuzztest_pgon() {
	r2 = time(NULL);
	for(int i=0;i<100;i++) rand(0,10);
	//size_t numpts = int(rand(0,10000));
	//size_t numpts = int(rand(0,10));
	size_t numpts = 26;
	std::vector<rational_point> pgon;
	for (size_t i=0;i<numpts;i++) {
		int x = rand(-100,100);
		int y = rand(-100,100);
		int z = rand(-1,1);
		rational_point p(x,y,z);
		p.x=x; p.y=y; p.z=z;
		pgon.push_back( p );
	}
	std::vector<std::vector<rational_point> > triangles;
	std::stringstream s;
	s << "<svg width='480px' height='480px' xmlns='http://www.w3.org/2000/svg' version='1.1'>\n";
	s << "<!--pgon before:-->\n" << dumpsvg( pgon, "black" ) << "\n";
	int err = triangulate_near_planar_polygon( pgon, triangles );
	svg_xcursor += 2; svg_ycursor += 2;
	s << "<!--pgon after:-->\n" << dumpsvg( pgon, "blue" ) << "\n";
	svg_xcursor += 2; svg_ycursor += 2;
	for (size_t i=0;i<triangles.size();i++) {
		s << "<!--tri after-->\n" << dumpsvg( triangles[i], "green" ) << "\n";
	}
	s << "</svg>\n";
	//std::cout << s.str();
	//assert( err==0 );
}

int main() {
	test();
	fuzztest();
	fuzztest_pgon();
}
#endif


/*
On the Wedge / Determinant / Signed Parallelogram Area / Cross Product / etc

The concept of 'signed area of the parallelogram' is a simple way to
visualize how 'side()' works. Consider two vectors v1, v2: (your text
viewer must be using a fixed-width font for these diagrams to work):

yaxis
|
|
|    . v1
|   /
|  /        .v2
| /     .
|/  .
|-------------------------> x axis


Together, they define a paralellogram:

yaxis            .newcorner
|            .  /
|        .     /
|    . v1     /
|   /        /
|  /        .v2
| /     .
|/  .
|-------------------------> x axis

Now, consider the formula for the Area of the paralellogram. One formula is
as follows:

Area = Absolute Value( v1.x * v2.y - v2.x * v1.y )

It is fine. But what if we deal with 'signed area'?

Signed Area = (v1.x * v2.y - v2.c * v1y )

Note that now, it actually matters which vector we consider 'first'.
And, the resulting sign will tell us which vector is 'counter clockwise'
or 'clockwise' from the other, as if they were watch hands. Another way
to think about it is to look at the parallelogram point labelled 'newcorner'
in the above diagram. Then treat it like an addition of two vectors.

yaxis            .v1+v2=newcorner
|            .
|        .
|    . v1
|   /
|  /
| /
|/
|-------------------------> x axis

Note that if you were a Ladybug walking from 0,0 to v1, you'd have to 'turn right'
to get to 'new corner'. Again, the 'sign' of the signed area will correspond
to whether or not Ladybug has to turn left or right to get to newcorner.
When the area is negative, i.e. if you put v2 before v1, here's what Ladybug's
path looks like:

yaxis            .newcorner
|               /
|              /
|             /
|            /
|           .v2
|       .
|   .
|-------------------------> x axis


For number examples, consider the vectors:

  3,4

  5,12

The Area would be absolute_value( 3*12-5*4 ) = 16

The Signed Area, if you take 3,4 first, is (3*12-5*4) = 16.
But if you take 5,12 first, it is (5*4-3*12) = -16. And, as you can tell,
3,4 is 'clockwise' from 5,12, when the Signed Area was Positive.
5,12 is 'counterclockwise' from 3,4 because the Signed Area is negative.
And Ladybug will take a 'left turn' if we put 3,4 first, but a 'right turn'
if we put 5,12 first.

Lastly, this automatically gives us a way to detect if v1 and v2 are collinear:
the 'signed area' of the parallelogram will be 0! v2 wont be on either side
of v1, and vice versa.

The reason 'side' is so important is not only for finding orientation of
a point on a line in a 2-d space. You can use exactly the same principle
to find whether a point is on one side of a plane or another in 3d
space... consider 4 points and the 'signed volume' of the paralellapiped
that they form. If the paralellapiped is 'flat' then its 'volume' is 0.

But go farther, what about comparing two points in 1 dimensional space,
both of which have rational coordinates? say, 1/3, and 1/2. You have to
do a/b - c/d in fractions, which turns into a*d-b*c / b*d.. but you only
need a*d-b*c to tell whether one point is 'less' than the other.

In other words, the formula x1y2-x2y1 (also called the 'determinant') of
point coordinates is some kind fundamental underlying pattern that is
very cool to contemplate.

In fact it is so fundamental that it has several different names as it
has been used in so many different areas.

*/
