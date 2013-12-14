/*
rational trigonometry for c++
*/

template <typename Number>
Number sqr( const Number &x ) { return x*x; }

template <typename Number, typename Point>
Number blue_quadrance( const Point &p1, const Point &p2 ) {
	return sqr(p1.x()-p2.x())+sqr(p1.y()-p2.y());
}

template <typename Number, typename Vector>
Number blue_quadrance( const Vector &v ) {
	return sqr(v.x())+sqr(v.y());
}
