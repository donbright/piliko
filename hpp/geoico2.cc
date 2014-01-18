#include <vector>
#include <iostream>
#include <map>
#include <cmath>

struct vector3 {
	double x,y,z;
	vector3(double px,double py,double pz) {x=px;y=py;z=pz;}
	vector3() {x=y=z=0;}
	vector3 operator*( double s ) { return vector3(x*s,y*s,z*s); }
	vector3 operator/( double s ) { return vector3(x/s,y/s,z/s); }
	vector3 operator-( const vector3 &v ) const { return vector3(x-v.x,y-v.y,z-v.z); }
	vector3 operator+( const vector3 &v ) const { return vector3(x+v.x,y+v.y,z+v.z); }
	vector3 operator*( const vector3 &v ) const { return vector3(x*v.x,y*v.y,z*v.z); }
	vector3 operator-() { return vector3(-x,-y,-z); }
	vector3 &operator*=( double s ) { x*=s; y*=s; z*=s; return *this;}
};
#define point vector3

struct hedron {
	std::vector<point> ptlist;
	std::map<point,int> ptmap;
	std::vector< std::vector<int> > faces;
	void addpoint( point p ) {
		if (!ptmap.count(p)) {
			ptmap[p] = ptlist.size();
			ptlist.push_back(p);
		}
		int idx = ptmap[p];
		faces.back().push_back(idx);
	}
	void addface() {
		faces.push_back(std::vector<int>());
	}
	void merge( hedron &h ) {
		for (int i=0;i<h.faces.size();i++) {
			addface();
			for (int j=0;j<h.faces[i].size();j++) {
				point p = h.ptlist[h.faces[i][j]];
				addpoint(p);
			}
		}
	}
};

std::ostream &operator<<(std::ostream &stream, const point &p ) {
	stream << p.x << " " << p.y << " " << p.z; return stream;
}

std::ostream &operator<<(std::ostream &stream, const hedron &h ) {
	stream << "OFF\n" << h.ptlist.size() << " " << h.faces.size() << "\n";
	for (int i=0;i<h.ptlist.size();i++)
		stream << h.ptlist[i].x << " " << h.ptlist[i].y << " " << h.ptlist[i].z << "\n";
	for (int i=0;i<h.faces.size();i++) {
		stream << h.faces[i].size() << " ";
		for (int j=0;j<h.faces[i].size();j++)
			stream << h.faces[i][j] << " ";
		stream << "\n";
	} return stream;
}

vector3 operator*( const int &i, vector3 &v ) {
	return vector3(v.x*i,v.y*i,v.z*i);
}

// implemented so std::map will work.
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

// split a triangle (t1,t2,t3) into n^2 subtriangles
void splitn( hedron &h, point &t1, point &t2, point &t3, int n ) {
	if (n<1) n=1;
	vector3 v1 = -vector3( t1 - t3 ) / n;
	vector3 v2 = -vector3( t3 - t2 ) / n;
	double cx = (t1.x+t2.x+t3.x) / 3;
	double cy = (t1.y+t2.y+t3.y) / 3;
	double cz = (t1.z+t2.z+t3.z) / 3;
	vector3 centroid( cx, cy, cz );
	for (int idx = 0; idx < n+1; idx++) {
		for (int j = 0; j < idx; j++) {
			int i = idx - 1;
			point p1 = t1 + i*v1 + j*v2;
			point p2 = p1 + v1;
			point p3 = p1 + v1 + v2;
			if (j>0 && idx>0 && j<(idx-1) && idx<n) {
				p1 = p1 + (p1+centroid) / 10.0;
				p2 = p2 + (p2+centroid) / 10.0;
				p3 = p3 + (p3+centroid) / 10.0;
			}
			h.addface();
			h.addpoint(p1);
			h.addpoint(p3);
			h.addpoint(p2);
			if (j<i) {
				point p4 = p1 + v2;
				if (j>0 && idx>0 && j<(idx-1) && idx<n) {
					p4 = p4 + (p4-centroid) / 10.0;
				}
				h.addface();
				h.addpoint(p1);
				h.addpoint(p4);
				h.addpoint(p3);
			}
		}
	}
}

// true if point contains 'not a number' coordinate, false otherwise
bool hasnan( point &p ) { return (isnan(p.x) || isnan(p.y) || isnan(p.z)); }
bool hasinf( point &p ) { return (isinf(p.x) || isinf(p.y) || isinf(p.z)); }

void make_icosahedron(hedron &h) {
        h.ptlist.push_back( point( 0,1,(std::sqrt(5)+1.0)/2.0) );
	h.ptlist.push_back( point( h.ptlist[0] * vector3(1, 1,-1)) );
	h.ptlist.push_back( point( h.ptlist[0] * vector3(1,-1, 1)) );
	h.ptlist.push_back( point( h.ptlist[0] * vector3(1,-1,-1)) );
	for (int i=0;i<8;i++)
		h.ptlist.push_back( rotl( h.ptlist[i] ) );
	int initfaces[60] = { 1,3,11, 2,0,9, 2,5,8, 3,7,11, 4,1,6, 5,2,7, \
	  7,2,9, 6,0,4, 5,3,10, 7,3,5, 8,0,2, 8,4,0, 8,5,10, 10,1,4, 10,3,1, \
	  10,4,8, 9,0,6, 9,6,11, 11,6,1, 11,7,9 };
	for (int i=0;i<60;i+=3) {
		h.addface();
		h.addpoint( h.ptlist[initfaces[i+0]] );
		h.addpoint( h.ptlist[initfaces[i+1]] );
		h.addpoint( h.ptlist[initfaces[i+2]] );
	}
}

void make_tetrahedron(hedron &h) {
	h.ptlist.push_back( point( 1, 1, 1 ) );
	h.ptlist.push_back( point( 1,-1,-1 ) );
	h.ptlist.push_back( point(-1, 1,-1 ) );
	h.ptlist.push_back( point(-1,-1, 1 ) );
	int initfaces[3*4] = { 3,1,0, 2,0,1, 3,0,2, 2,1,3 };
	for (int i=0;i<3*4;i+=3) {
		h.addface();
		h.addpoint( h.ptlist[initfaces[i+0]] );
		h.addpoint( h.ptlist[initfaces[i+1]] );
		h.addpoint( h.ptlist[initfaces[i+2]] );
	}
}

void make_octahedron(hedron &h) {
	h.ptlist.push_back( point( 1, 0, 0 ) );
	h.ptlist.push_back( point( 0, 1, 0 ) );
	h.ptlist.push_back( point( 0, 0, 1 ) );
//	h.ptlist.push_back( point( 0,-1, 0 ) );
	h.addface();
	h.addpoint( h.ptlist[0] );
	h.addpoint( h.ptlist[1] );
	h.addpoint( h.ptlist[2] );
//	h.addface();
//	h.addpoint( h.ptlist[0] );
//	h.addpoint( h.ptlist[2] );
//	h.addpoint( h.ptlist[3] );
/*	h.ptlist.push_back( point( 1, 0, 0 ) );
	h.ptlist.push_back( point(-1, 0, 0 ) );
	h.ptlist.push_back( point( 0, 0, 1 ) );
	h.ptlist.push_back( point( 0, 0,-1 ) );
	h.ptlist.push_back( point( 0, 1, 0 ) );
	h.ptlist.push_back( point( 0,-1, 0 ) );
	int initfaces[3*8] = { 0,2,5, 0,4,2, 1,3,5, 1,4,3, 2,4,1, 3,4,0, \
	  5,2,1, 5,3,0 };
	for (int i=0;i<3*8;i+=3) {
		h.addface();
		h.addpoint( h.ptlist[initfaces[i+0]] );
		h.addpoint( h.ptlist[initfaces[i+1]] );
		h.addpoint( h.ptlist[initfaces[i+2]] );
	}
*/
}

point centroid( point &p1, point &p2, point &p3 ) {
	double x = (p1.x + p2.x + p3.x)/3;
	double y = (p1.y + p2.y + p3.y)/3;
	double z = (p1.z + p2.z + p3.z)/3;
	return point(x,y,z);
}

int main() {
	int n = 5;
	hedron h;
	//make_icosahedron( h );
	//make_tetrahedron( h );
	make_octahedron( h );
	hedron geo;
	double sphere_quadrance = quadrance( h.ptlist[0], point(0,0,0) );
	for (int i=0;i<h.faces.size();i++) {
		point &p1 = h.ptlist[h.faces[i][0]];
		point &p2 = h.ptlist[h.faces[i][1]];
		point &p3 = h.ptlist[h.faces[i][2]];
		hedron tmp;
		splitn( tmp, p1, p2, p3, n );
		geo.merge( tmp );
	}
	for (int i=0;i<geo.ptlist.size();i++) {
		double point_quadrance = quadrance(point(0,0,0),geo.ptlist[i]);
		double ratio = std::sqrt( sphere_quadrance/point_quadrance );
		if (isnan(ratio)) continue;
		geo.ptlist[i] *= ratio;
	}
	std::cout << geo;
}




/*


  ...................
  | /| /| /| /| /| /
  |/ |/ |/ |/ |/ |/
  ................
  | /| /| /| /| /
  |/ |/ |/ |/ |/
  .............
  | /| /| /| /
  |/ |/ |/ |/
  ..........
  | /| /| /
  |/ |/ |/
  .......
  | /| /
  |/ |/
  ....
  | /
  |/
  .

  5 012345
  4 01234
  3 0,123
  2 012
  1 01
  0 0

0-2  2-1
*/
