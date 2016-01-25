
/* quaternion rotation */

package main

import "fmt"

type Pythangle struct {
	adjacentleg, oppositeleg, hypoteneuse int
}

type Rational struct {
	num, denom int
}

type Quaternion struct {
	a,b,c,d Rational
}

func sine( t Pythangle ) ( r Rational ) {
	r.num = t.oppositeleg
	r.denom = t.hypoteneuse
	return
}

func cosine( t Pythangle ) ( r Rational ) {
	r.num = t.adjacentleg
	r.denom = t.hypoteneuse
	return
}

func halfPythangle( t Pythangle ) ( r Pythangle ) {
	r.oppositeleg
	r.adjacentleg
	r.hypoteneuse
	return
}

func neg( a Rational ) ( r Rational ) {
	r.num = -a.num
	r.denom = a.denom
	return
}

func div( a,b Rational ) ( r Rational ) {
	r.num = a.num * b.denom
	r.denom = a.denom * b.num
	return
}

/*
1/3 + 2/5 + 7/9
3*(1/3 + 2/5 + 7/9)
5*(1/3 + 2/5 + 7/9)
9*(1/3 + 2/5 + 7/9)
5*1/3*5 + 2*3/5*3
*/

func add( args...Rational ) ( r Rational ) {
	supernum := 1
	superdenom := 1
	for _,v := range args {
		superdenom *= v.denom
	}
	for _,v := range args {
		v.num *= (superdenom / v.denom)
		supernum += v.num
	}
	r.num = supernum
	r.denom = superdenom
	return
}

func Hamilton_product( q1, q2 Quaternion ) ( r Quaternion ) {
	a1,b1,c1,d1,a2,b2,c2,d2 := q1.a,q1.b,q1.c,q1.d,q2.a,q2.b,q2.c,q2.d
	r.a = add(mul(a1,a2),neg(mul(b1,b2)),neg(mul(c1,c2)),neg(mul(d1,d2)))
	r.b = add(mul(a1,b2),    mul(b1,a2),     mul(c1,d2), neg(mul(d1,c2)))
	r.c = add(mul(a1,c2),neg(mul(b1,d2)),    mul(c1,a2),     mul(d1,b2))
	r.d = add(mul(a1,d2),    mul(b1,c2), neg(mul(c1,b2)),    mul(d1,a2))
	return
}

func RotationQuaternions( x,y,z Rational, a Pythangle ) ( q, qn1 Quaternion ) {
	s := sine(halfPythangle( a ))
	q.a = cosine(halfPythangle( a ))
	q.b = mul(s,x)
	q.c = mul(s,y)
	q.d = mul(s,z)
	qn1.a = q.a
	qn1.b = neg(q.b)
	qn1.c = neg(q.c)
	qn1.d = neg(q.d)
	return
}

func mul(a, b Rational) (c Rational) {
	c.num = a.num * b.num
	c.denom = a.denom * b.denom
	return
}

func Rotate( rotatee Quaternion, x,y,z Rational, a Pythangle ) ( r Quaternion ) {
	q, qn1 := RotationQuaternions( x,y,z,a )
	tmp := Hamilton_product( q, rotatee )
	r = Hamilton_product( tmp, qn1 )
	return
}

func main() {
	fmt.Println("Hello Go")
	fmt.Println()
}
