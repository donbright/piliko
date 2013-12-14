/*
ratalg.hpp Copyright (c) 2013, Don Bright ( http://github.com/donbright )
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
floating point. The downside is they can be slow in certain situations.

Care should be taken converting coordinates. For example exact
conversion double->rational is possible, but rational->double is not
exact. This can destroy the topology of a shape, producing errors.See
the general literature for more info.

Code style is 'Effective Go'.
*/

#include <gmpxx.h>
#include <vector>
#include <assert.h>

/* orientation - you can imagine in 3d space a polygon will appear to 
have a different orientation depending on which side you look. If it 
appears CounterClockwise that is considered the 'outside' of the 
polygon, while if it appears Clockwise then you are looking at the 
'inside'. */
typedef enum {
	CLOCKWISE = -1,
	COUNTERCLOCKWISE = 1,
	ANTICLOCKWISE = 1,
	NONE = 0
} orientation_t;

typedef enum {
	XYPLANE, YZPLANE, XZPLANE
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

Note this only works on algorithms that don't create new points, nor
change the existing points. */
struct rational_point {
        mpq_class x,y,z;
        rational_point( double x, double y, double z );
	projection_t projection;
	mpq_class projectedx() const;
	mpq_class projectedy() const;
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

// build a rational 3 dimensional point from 3 double-float numbers
// mpq_class does implicit exact conversion from double to rational.
rational_point::rational_point( double x, double y, double z ) {
	this->x = x;
	this->y = y;
	this->z = z;
	this->projection = XYPLANE;
}

/* return the 'projected' version of the point's x coordinate. see the
documentation of 'struct point' for more info about projection. */
mpq_class rational_point::projectedx() const {
	if (this->projection==XYPLANE) return this->x;
	else if (this->projection==XZPLANE) return this->x;
	else if (this->projection==YZPLANE) return this->y;
	else return mpq_class(0);
}
mpq_class rational_point::projectedy() const {
	if (this->projection==XYPLANE) return this->y;
	else if (this->projection==XZPLANE) return this->z;
	else if (this->projection==YZPLANE) return this->z;
	else return mpq_class(0);
}

/* build a plane equation from three points. Equation form is ax+by+cz+d = 0.
From Theory+Problems of Vector Analysis, Murray R Spiegel, 1959 Schaum
Publishing, New York. For any point p coplanar to 3 points p1,p2,p3, the
area of paralellapiped formed by vector (p1-p), vector (p2-p), and
vector(p3-p) = 0. Thus v1 dot v2 cross v3 = 0. Expand this using
Determinant math and a,b,c,d become clear.

    | x-x1  y-y1  z-z1|
det |x2-x1 y2-y1 z2-z1| = 0 --> x[(y2-y1)(z3-z1)-(y3-y1)(z2-z1)]+ . . . = 0
    |x3-x1 y3-y1 z3-z1|         a=(y2-y1)(z3-z1)-(y3-y1)(z2-z1) b=... c=...
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

// true if p lies on plane, false otherwise
bool meet( const rational_plane &pl, const rational_point &p ) {
	if (pl.a*p.x + pl.b*p.y + pl.c*p.z + pl.d == 0) return true;
	return false;
}

// true if the given points are coplanar, false otherwise.
// for 0,1, or 2 given points, return true.
bool coplanar( const std::vector<rational_point> &points ) {
	if (points.size()<3) return true;
	rational_plane plane(points[0],points[1],points[2]);
	for (size_t i =  3  ; i < points.size(); i++) {
		if (!meet( plane, points[i] )) return false;
	}
	return true;
}

/* side: given 3 points, find whether p3 is a 'right turn' or 'left turn'
 from the line p1->p2. if result is >0, turn is left. <0 right. 0=collinear
 this is similar to several concepts, including 'winding', or 'side', or
 the 'wedge' of the bivector( p3-p2, p2-p1 ), or the 'determinant'
 of (p3-p2, p2-p1). or the signed paralellogram area of (p3-p2)(p2-p1), or
 the cross product of 3d vectors.

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

// same as side(), but with different human language idiom
orientation_t orientation( const rational_point &p1, const rational_point &p2, const rational_point &p3 )
{
	if (side(p1,p2,p3)>0) return COUNTERCLOCKWISE;
	else if (side(p1,p2,p3)<0) return CLOCKWISE;
	return NONE;
}

// 2d collinear test
bool collinear( const rational_point &p1, const rational_point &p2, const rational_point &p3 )
{
	if (side(p1,p2,p3)!=0) return false;
	return true;
}

/* 'orientation' is the concept of the ordering of points in a polygon. if
 you ran around the pgon in the order the points are given, and you turned
 mostly right, thats clockwise. if you turn mostly left, thats
 counterclockwise. if you only turn 'about face' (180 degrees) its not
 really a polygon, its a bunch of collinear points.

 this is the '2d' version.
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

// is the point p inside the triangle formed by t1,t2,t3?
bool inside( const rational_point &t1, const rational_point &t2, const rational_point &t3, const rational_point &p )
{
	if (side(t1,t2,p)>0 && side(t2,t3,p)>0 && side(t3,t1,p)>0) return true;
	return false;
}

// is the point on the line segments of the triangle formed by t1,t2,t3?
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

/* convert a near-planar 3d polygon into a sequence of triangles. assume
 it is simple, non-self-intersecting, and no holes. return 0 on
 success, !0 on error; input polygon is destroyed and will have size() 0 */
int triangulate_near_planar_polygon( std::vector<rational_point> &pgon, std::vector< std::vector< rational_point > > &triangles ) {
	projection_t goodproj = find_good_projection( pgon );
	for (size_t i=0;i<pgon.size();i++) {
		pgon[i].projection = goodproj;
	}
	while ( pgon.size()>2 ) {
		std::vector<rational_point> newtriangle;
		int err = clip_ear( newtriangle, pgon );
		if (err) return err;
		triangles.push_back( newtriangle );
	}
	return 0;
}





/* Testing of above code
To test. uncomment main() and compile like so:
echo '#include "ratalg.hpp"' >> t.cc; g++ t.cc -lgmpxx -lgmp -Dtest_ratalg_hpp*/
#ifdef test_ratalg_hpp

#include <sstream>
#include <iostream>
#include <time.h>

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
}



static int svg_xcursor = 100;
static int svg_ycursor = 100;
std::string dumpsvg( std::vector<rational_point> &pgon, std::string color ) {
	std::stringstream s;
	s << "<!--";
	for (size_t i=0;i<pgon.size();i++) {
		s << "["<<pgon[i].x<<","<< pgon[i].y << ","
		  << pgon[i].z << ":"<< pgon[i].projection << "]";
	}
	s << " orientation:" << orientation( pgon ) << "-->\n";
	s << "<polygon fill='none' stroke='" << color << "' points='";
	for (size_t i=0;i<pgon.size();i++) {
		s << pgon[i].projectedx()+svg_xcursor << ","
		  << pgon[i].projectedy()+svg_ycursor << " ";
	}
	s << "'/>\n";
	return s.str();
}

static unsigned int r1 = 1, r2 = 1;
int rand(int lo,int hi) { r2 = r1+r2; r1 = r2-r1; return (r2 % (hi-lo))+lo; }

void fuzztest() {
	r2 = time(NULL);
	for(int i=0;i<100;i++) rand(0,10);
	//size_t numpts = int(rand(0,10000));
	//size_t numpts = int(rand(0,10));
	size_t numpts = 4;
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
	std::cout << s.str();
	//assert( err==0 );
}

int main() {
	test();
	fuzztest();
}
#endif
