/* line line intersection given two lines as follows

consider w,s,and u as points, all with given coordinates
w and s lie on "l1", a line
consider the line l2 to be between the origin 0,0 and u

consider q as the intersection of lines one and two
find it's value!

                  l1
   |             /
   |            /s
   |           /
   |          /
   |         /w      ___----l2
   |        /  __---u
   |       /---
   |   __-/q
   |---  /
   ------------------------

How?

  First, consider V, a vector between w and s, or s minus w.
  vx is the x distance between points w and s. vy is the y distance.
  Consider W a vector from 0,0 to point w
  Consider U a vector from 0,0 to point u

  Now consider the wedge operator, '^', as defined by Geometric Algebra.
  It operates on two vectors with tails at origin, the result describing the
  "signed area" of a paralellogram formed by them if added.

  wedge A,B = A ^ B = ax*by - bx*ay

  Now, through various algebraic manipulations, it can be shown that the point
  q of intersection an be described as follows:

  qx = vx * ( V ^ W ) / ( V ^ U )
  qy = vy * ( V ^ W ) / ( V ^ U )


  Output is svg graphics file (text based graphics format)

Number Type

 This uses 'fake rationals'. The rational is a ratio of to ints, but
 they do not expand if either one, numerator or denominator, overflows 32 bits,
 64 bits, or whatever bit width is being used.

 */

package main

import "fmt"

type Rational struct {
	num, denom int
}

type Vector struct {
	x, y Rational
}

type Point Vector

func tofloat( r Rational ) ( f float32 ) {
	if r.denom==0 {
		f = 3.40282346638528859811704183484516925440e+38
	} else {
		f = float32(r.num)/float32(r.denom)
	}
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

func add( a,b Rational ) ( r Rational ) {
	r.denom = a.denom * b.denom
	r.num = a.denom * b.num + b.denom * a.num
	return
}

func sub(a, b Rational ) ( r Rational ) {
	fmt.Println("sub",a,b,neg(b),add(a,neg(b)))
	r = add( a, neg(b) )
	return
}

func mul(a, b Rational) (c Rational) {
	c.num = a.num * b.num
	c.denom = a.denom * b.denom
	return
}

func wedge(a,b Vector) (r Rational) {
	r = sub(mul(a.x,b.y),mul(b.x,a.y))
	return
}

func svgbegin( width, height int ) (s string) {
	ns := "http://www.w3.org/2000/svg"
	tmp := `
<svg width='%d' height='%d' xmlns='%s' version='%s'>
 <!-- border -->
 <path fill='none' stroke='black' d='M 0 0 L %d %d L %d %d L %d %d L %d %d'/>
`
	s = fmt.Sprintf(tmp,width,height,ns,"1.1",0,0,height,0,width,height,width,0)
	return
}

func svgpoint(p Point) (s string) {
	f:=`
  <circle cx='%f' cy='%f' r='2' stroke='black' fill='none' />
`
	return fmt.Sprintf(f,tofloat(p.x),tofloat(p.y))
}

func svgend() (s string) {
	return "</svg>"
}

func svglines() (s string) {
	s = "  <path fill='none' stroke='black' fill-opacity='0.45' d='"
	return
}


func main() {
	fmt.Println(svgbegin(400,400))

	wx := Rational{2,1}
	wy := Rational{1,1}
	vx := Rational{3,1}
	vy := Rational{4,1}
	ux := Rational{6,1}
	uy := Rational{2,1}
	w := Vector{wx,wy}
	v := Vector{vx,vy}
	u := Vector{ux,uy}
	wedger := div(wedge(v,w),wedge(v,u))
	fmt.Println("wedge vw", wedge(v,w), "wedge vu", wedge(v,u))
	qx := mul(ux, wedger)
	qy := mul(uy, wedger)
	q := Point{qx,qy}

	fmt.Println("<!--",w,v,u,q,"-->")
	fmt.Println(svgpoint(q))
	fmt.Println(svgend())

}
