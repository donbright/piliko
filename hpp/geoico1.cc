// with Eigen... 0.127 for n = 100
// without Eigen... basically the same. no speedup.
#include <vector>
#include <iostream>
#include <map>
#include <cmath>

struct Vector3d {
	double x,y,z;
	Vector3d(double px,double py,double pz) {x=px;y=py;z=pz;}
	Vector3d() {x=y=z=0;}
	Vector3d operator*( double s ) { return Vector3d(x*s,y*s,z*s); }
	Vector3d operator/( double s ) { return Vector3d(x/s,y/s,z/s); }
	Vector3d operator-( const Vector3d &v ) const { return Vector3d(x-v.x,y-v.y,z-v.z); }
	Vector3d operator+( const Vector3d &v ) const { return Vector3d(x+v.x,y+v.y,z+v.z); }
	Vector3d operator*( const Vector3d &v ) const { return Vector3d(x*v.x,y*v.y,z*v.z); }
	Vector3d operator-() { return Vector3d(-x,-y,-z); }
	Vector3d &operator*=( double s ) { x*=s; y*=s; z*=s; return *this;}
};
#define point Vector3d

std::ostream &operator<<(std::ostream &stream, const point &p ) {
	stream << p.x << " " << p.y << " " << p.z; return stream;
}

Vector3d operator*( const int &i, Vector3d &v ) {
	return Vector3d(v.x*i,v.y*i,v.z*i);
}

//< is implemented here so std::map will work.
bool operator<( const point &p1, const point &p2 ) {
	bool result = false;
	if (p1.x<p2.x) result = true;
	else if (p1.x>p2.x) result = false;
	else {
		if (p1.y<p2.y) result = true;
		else if (p1.y>p2.y) result = false;
		else {
			if (p1.z<p2.z) result = true;
			else if (p1.z>p2.z) result = false;
			else result = false; // all ==
		}
	}
	return result;
}

// Treat a x,y,z point like a bit-string, then we can 'ROTL' (google it)
point rotl( point &p ) { return point(p.y,p.z,p.x); }

double sqr( double x ) { return x*x; }

double blue_quadrance( const point &p1, const point &p2 ) {
	return sqr(p1.x-p2.x)+sqr(p1.y-p2.y)+sqr(p1.z-p2.z);
}

double redblue_quadrance( const point &p1, const point &p2 ) {
	return sqr(p1.x-p2.x)-sqr(p1.y-p2.y)+sqr(p1.z-p2.z);
}

double bluered_quadrance( const point &p1, const point &p2 ) {
	return sqr(p1.x-p2.x)+sqr(p1.y-p2.y)-sqr(p1.z-p2.z);
}

double quadrance( const point &p1, const point &p2 ) { // aka squared distance
	return blue_quadrance(p1,p2); // sphere
	//return redblue_quadrance(p1,p2); // hyperboloid of one sheet
	//return bluered_quadrance(p1,p2); // hyperboloid of two sheets
}

struct triangle {
	point pts[3];
	triangle(point p1, point p2, point p3) {pts[0]=p1;pts[1]=p2;pts[2]=p3;}
};

// split a triangle into n^2 subtriangles
std::vector<triangle> splitn( triangle t, int n ) {
	if (n<1) n=1;
	std::vector<triangle> tris;
	Vector3d v1 = -Vector3d( t.pts[0] - t.pts[2] ) / n;
	Vector3d v2 = -Vector3d( t.pts[2] - t.pts[1] ) / n;
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

// given a point, project it onto a sphere centered at 0,0,0 with
// sphere's radius^2 = sphere_quadrance
point projectpt( point p, double sphere_quadrance ) {
	double point_quadrance = quadrance( point(0,0,0), p );
	double ratio = std::sqrt( sphere_quadrance/point_quadrance );
//	double ratio = std::sqrt( point_quadrance/sphere_quadrance );
	p *= ratio;
	return p;
}

// true if point contains 'not a number' coordinate, false otherwise
bool hasnan( point &p ) { return (isnan(p.x) || isnan(p.y) || isnan(p.z)); }
bool hasinf( point &p ) { return (isinf(p.x) || isinf(p.y) || isinf(p.z)); }

// given a sequence of triangles, project them onto a sphere centered at 0,0,0
// with sphere's radius^2 = sphere_quadrance
std::vector<triangle> project( std::vector<triangle> tris, double sphere_quadrance ) {
	std::vector<triangle> sphtris;
	for (int i=0;i<tris.size();i++) {
		point p1 = projectpt( tris[i].pts[0], sphere_quadrance );
		point p2 = projectpt( tris[i].pts[1], sphere_quadrance );
		point p3 = projectpt( tris[i].pts[2], sphere_quadrance );
		if (hasnan(p1)||hasnan(p2)||hasnan(p3)) continue;
		if (hasinf(p1)||hasinf(p2)||hasinf(p3)) continue;
		sphtris.push_back( triangle( p1, p2, p3 ) );
	}
	return sphtris;
}

int main() {
	int n = 59;
	std::vector<point> pts;
	pts.push_back( point(0,1,(std::sqrt(5)+1.0)/2.0) );
	pts.push_back( pts[0] * Vector3d(1, 1,-1) );
	pts.push_back( pts[0] * Vector3d(1,-1, 1) );
	pts.push_back( pts[0] * Vector3d(1,-1,-1) );
	for (int i=0;i<8;i++) pts.push_back( rotl( pts[i] ) );
	int initfaces[60] = { 1,3,11, 2,0,9, 2,5,8, 3,7,11, 4,1,6, 5,2,7, \
	  7,2,9, 6,0,4, 5,3,10, 7,3,5, 8,0,2, 8,4,0, 8,5,10, 10,1,4, 10,3,1, \
	  10,4,8, 9,0,6, 9,6,11, 11,6,1, 11,7,9 }; // icosahedron
	double sphereq = quadrance( pts[0], point(0,0,0) );
	std::vector<triangle> sphtris;
	for (int i=0;i<60;i+=3) {
		triangle t(pts[initfaces[i]],pts[initfaces[i+1]],pts[initfaces[i+2]]);
		std::vector<triangle> subtris = splitn( t, n );
		std::vector<triangle> sphpatchtris = project(subtris, sphereq);
		for (int i=0;i<sphpatchtris.size();i++)
			sphtris.push_back( sphpatchtris[i] );
	}
	//for (int i=0;i<sphtris.size();i++) std::cout << sphtris[i].pts[0] << "\n" << sphtris[i].pts[1] << "\n" << sphtris[i].pts[2] << "\n";
	//return 0;
	std::map<point,int> ptmap;
	std::vector<point> ptlist;
	std::vector< std::vector<int> > faces;
	for (int i=0;i<sphtris.size();i++) {
		std::vector<int> indexes(3);
		for (int j=0;j<3;j++) {
			point p = sphtris[i].pts[j];
			if (!ptmap.count( p )) {
				ptmap[ p ] = ptlist.size();
				ptlist.push_back( p );
			}
			indexes[j] = ptmap[p];
		}
		faces.push_back( indexes );
	}
	std::cout << "OFF\n" << ptlist.size() << " " << faces.size() << "\n";
	for (int i=0;i<ptlist.size();i++) std::cout << ptlist[i].x << " " << ptlist[i].y << " " << ptlist[i].z << "\n";
	for (int i=0;i<faces.size();i++) std::cout << "3 " << faces[i][0] << " " << faces[i][1] << " " << faces[i][2] << "\n";
}


