#include <vector>
#include <iostream>
#include <map>
#include <cmath>

struct vector3 {
	double x,y,z;
	vector3(double px,double py,double pz) {x=px;y=py;z=pz;}
	vector3() {x=y=z=0;}
	vector3 operator*( double s ) const { return vector3(x*s,y*s,z*s); }
	vector3 operator/( double s ) const { return vector3(x/s,y/s,z/s); }
	vector3 operator-( vector3 v ) const { return vector3(x-v.x,y-v.y,z-v.z); }
	vector3 operator+( vector3 v ) const { return vector3(x+v.x,y+v.y,z+v.z); }
	vector3 operator*( vector3 v ) const { return vector3(x*v.x,y*v.y,z*v.z); }
	vector3 operator-() const { return vector3(-x,-y,-z); }
	vector3 &operator*=( double s ) { x*=s; y*=s; z*=s; return *this;}
};

double sqr( double x ) { return x*x; }

double quadrance( const vector3 &v1, const vector3 &v2 ) { // aka squared distance
	return sqr(v1.x-v2.x)+sqr(v1.y-v2.y)+sqr(v1.z-v2.z);
}

struct projection {
	const vector3 &sphere_center;
	double sphere_quadrance;
	projection() : sphere_center(vector3(0,0,0)), sphere_quadrance(1) {}
	vector3 project( const vector3 &p ) const {
		double pq = quadrance( p, sphere_center );
		double ratio = sqrt(pq/sphere_quadrance);
		return p * ratio;
	}
};

projection unitproj;

struct point : vector3 {
	projection *proj;
	point( double px,double py,double pz ) : proj(&unitproj) {}
	point( projection &pproj ) : proj(&pproj) {};
	point() : proj(&unitproj) {};
	point projected() { proj->project( vector3( x, y, z ) ); }
};

struct geodesic_icosahderon {
	std::vector< point > pointlist;
	std::vector< std::vector< int > > faces;
};

std::ostream &operator<<(std::ostream &stream, const point &p ) {
	stream << p.x << " " << p.y << " " << p.z; return stream;
}

vector3 operator*( const int &i, vector3 &v ) {
	return vector3(v.x*i,v.y*i,v.z*i);
}
bool operator!=( const point &p1, const point &p2 ) {
        return (p1.x!=p2.x || p1.y!=p2.y || p1.z!=p2.z);
}
bool operator<( const point &p1, const point &p2 ) {
	return p1.x<p2.x && p1.y<p2.y && p1.z<p2.z;
}
// Treat a x,y,z point like a bit-string, then we can 'ROTL' (google it)
point rotl( point &p ) { return point(p.y,p.z,p.x); }

struct triangle {
	point pts[3];
	triangle(point p1, point p2, point p3) {pts[0]=p1;pts[1]=p2;pts[2]=p3;}
};

// split a triangle into n^2 subtriangles
std::vector<triangle> splitn( triangle t, int n ) {
	if (n<1) n=1;
	std::vector<triangle> tris;
	vector3 v1 = -vector3( t.pts[0] - t.pts[2] ) / n;
	vector3 v2 = -vector3( t.pts[2] - t.pts[1] ) / n;
	for (int idx = 0; idx < n+1; idx++) {
		for (int j = 0; j < idx; j++) {
			int i = idx - 1;
			point p1 = t.pts[0] + i*v1 + j*v2;
			point p2 = p1 + v1;
			point p3 = p1 + v1 + v2;
			point p4 = p1 + v2;
			triangle nt1(p1,p3,p2);
			triangle nt2(p1,p4,p3);
			tris.push_back( nt1 );
			if (j<i) tris.push_back( nt2 );
		}
	}
	return tris;
}

int main() {
	int n = 10;
	std::vector<point> pts;

	// part 1 - create icosahedron
	pts.push_back( point(0,1,(std::sqrt(5)+1.0)/2.0) );
	pts.push_back( pts[0] * vector3(1, 1,-1) );
	pts.push_back( pts[0] * vector3(1,-1, 1) );
	pts.push_back( pts[0] * vector3(1,-1,-1) );
	for (int i=0;i<8;i++) pts.push_back( rotl( pts[i] ) );
	int initfaces[60] = { 1,3,11, 2,0,9, 2,5,8, 3,7,11, 4,1,6, 5,2,7, \
	  7,2,9, 6,0,4, 5,3,10, 7,3,5, 8,0,2, 8,4,0, 8,5,10, 10,1,4, 10,3,1, \
	  10,4,8, 9,0,6, 9,6,11, 11,6,1, 11,7,9 }; // icosahedron
	double sphereq = quadrance( pts[0], point(0,0,0) );
	std::vector<triangle> sphtris;
	// part 2 - split icosahedron faces into pieces
	for (int i=0;i<60;i+=3) {
		triangle t(pts[initfaces[i]],pts[initfaces[i+1]],pts[initfaces[i+2]]);
		std::vector<triangle> subtris = splitn( t, n );
		// todo
		// for each tri, add poly, add vertex.
		// set projection for each point as we create?
	}

	// todo - erase this part, equiv function in add_verex, add_poly
/*	std::map<point,int> ptmap;
	std::vector<point> ptlist;
	std::vector< std::vector<int> > faces;
	for (int i=0;i<sphtris.size();i++) {
		std::vector<int>indexes(3);
		for (int j=0;j<3;j++) {
			point &p = sphtris[i].pts[j];
			if (!ptmap.count( point(p) )) {
				ptmap[ point(p) ] = ptlist.size();
				ptlist.push_back( point(p) );
			}
			indexes[j] = ptmap[point(p)];
		}
		faces.push_back( indexes );
	}
	std::cout << "OFF\n" << ptlist.size() << " " << faces.size() << "\n";
	for (int i=0;i<ptlist.size();i++) std::cout << ptlist[i].x << " " << ptlist[i].y << " " << ptlist[i].z << "\n";
	for (int i=0;i<faces.size();i++) std::cout << "3 " << faces[i][0] << " " << faces[i][1] << " " << faces[i][2] << "\n";
*/
}


