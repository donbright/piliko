// with Eigen... 0.127 for n = 100
#include <eigen3/Eigen/Core> // FIXME for inclusion
#include <vector>
#include <iostream>
#include <map>
using Eigen::Vector3d;
using Eigen::Vector3i;
#define point Vector3d

// Treat a x,y,z point like a bit-string, then we can 'ROTL' (google it)
point rotl( point &p ) { return point(p.y(),p.z(),p.x()); }

struct mpoint {
	double px,py,pz;
	mpoint(point p){px=p.x();py=p.y();pz=p.z();}
	double x() const {return px;}
	double y() const {return py;}
	double z() const {return pz;}
};
bool operator!=( const mpoint &p1, const mpoint &p2 ) {
        return (p1.x()!=p2.x() || p1.y()!=p2.y() || p1.z()!=p2.z());
}
bool operator<( const mpoint &p1, const mpoint &p2 ) {
	return p1.x()<p2.x() && p1.y()<p2.y() && p1.z()<p2.z();
}
double sqr( double x ) { return x*x; }

double quadrance( const point &p1, const point &p2 ) { // aka squared distance
	return sqr(p1.x()-p2.x())+sqr(p1.y()-p2.y())+sqr(p1.z()-p2.z());
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
	p *= ratio;
	return p;
}

// given a sequence of triangles, project them onto a sphere centered at 0,0,0
// with sphere's radius^2 = sphere_quadrance
std::vector<triangle> project( std::vector<triangle> tris, double sphere_quadrance ) {
	std::vector<triangle> sphtris;
	for (int i=0;i<tris.size();i++) {
		point p1 = projectpt( tris[i].pts[0], sphere_quadrance );
		point p2 = projectpt( tris[i].pts[1], sphere_quadrance );
		point p3 = projectpt( tris[i].pts[2], sphere_quadrance );
		sphtris.push_back( triangle( p1, p2, p3 ) );
	}
	return sphtris;
}

int main() {
	int n = 100;
	std::vector<point> pts;
	pts.push_back( point(0,1,(std::sqrt(5)+1.0)/2.0) );
	pts.push_back( pts[0].cwiseProduct(Vector3d(1,1,-1)) );
	pts.push_back( pts[0].cwiseProduct(Vector3d(1,-1,1)) );
	pts.push_back( pts[0].cwiseProduct(Vector3d(1,-1,-1)) );
	for (int i=0;i<8;i++) pts.push_back( rotl( pts[i] ) );
	int initfaces[60] = { 1,3,11, 2,0,9, 2,5,8, 3,7,11, 4,1,6, 5,2,7, \
	  7,2,9, 6,0,4, 5,3,10, 7,3,5, 8,0,2, 8,4,0, 8,5,10, 10,1,4, 10,3,1, \
	  10,4,8, 9,0,6, 9,6,11, 11,6,1, 11,7,9 };
	double sphereq = quadrance( pts[0], point(0,0,0) );
	std::vector<triangle> sphtris;
	for (int i=0;i<60;i+=3) {
		triangle t(pts[initfaces[i]],pts[initfaces[i+1]],pts[initfaces[i+2]]);
		std::vector<triangle> subtris = splitn( t, n );
		std::vector<triangle> sphpatchtris = project(subtris, sphereq);
		for (int i=0;i<sphpatchtris.size();i++)
			sphtris.push_back( sphpatchtris[i] );
	}
	for (int i=0;i<sphtris.size();i++) std::cout << sphtris[i].pts[0].transpose() << "\n" << sphtris[i].pts[1].transpose() << "\n" << sphtris[i].pts[2].transpose() << "\n";
	return 0;
	std::map<mpoint,int> ptmap;
	std::vector<mpoint> ptlist;
	std::vector<Vector3i> faces;
	for (int i=0;i<sphtris.size();i++) {
		int indexes[3];
		for (int j=0;j<3;j++) {
			point &p = sphtris[i].pts[j];
			if (!ptmap.count( mpoint(p) )) {
				ptmap[ mpoint(p) ] = ptlist.size();
				ptlist.push_back( mpoint(p) );
			}
			indexes[j] = ptmap[mpoint(p)];
		}
		faces.push_back(Vector3i(indexes[0],indexes[1],indexes[2]));
	}
	std::cout << "OFF\n" << ptlist.size() << " " << faces.size() << "\n";
	for (int i=0;i<ptlist.size();i++) std::cout << ptlist[i].x() << " " << ptlist[i].y() << " " << ptlist[i].z() << "\n";
	for (int i=0;i<faces.size();i++) std::cout << "3 " << faces[i][0] << " " << faces[i][1] << " " << faces[i][2] << "\n";
}

