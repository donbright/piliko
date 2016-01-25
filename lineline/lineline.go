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
  vx is the x-distance between points w and s. vy is the y-distance.
  Consider W a vector from 0,0 to point w
  Consider U a vector from 0,0 to point u

  Now consider the wedge operator, '^', as defined by Geometric Algebra.
  It operates on two vectors with tails at origin, the result describing the
  "signed area" of a paralellogram formed by them if added.

  wedge A,B = A ^ B = ax*by - bx*ay

  Now, through various algebraic manipulations, it can be shown that the point
  q of intersection an be described as follows:

  qx = ux * ( V ^ W ) / ( V ^ U )
  qy = uy * ( V ^ W ) / ( V ^ U )

  Output is svg graphics file (text based graphics format)

Fun Fact
 If you only need to 'scale' the vector u so that it's head rests on the
 intersection point, then you can just do this

  scale factor = V^W / V^U

 Why? because Intersection vector = scale factor * u vector
 This is interesting to me... the simplicity of the scale factor could be
 useful in some situations.

 In this method, if modified for the situation where one is given 4 general
 points, two lying on line1 and two on line2... in such case as one needs
 to subtract the highest from lowest points and find wx,wy,ux,uy relative
 to the 'lowest' point which will become the origin, translated as such,
 it is interesting that you don't need to do this translation for the 'higher'
 point on line1, the "head" of v. You only need v's head as it relates
 to it's tail, not as it relates to origin.

 Computation

 wedge between two vectors described by rational-number coordinates are
 intesting.

 V ^ W

 becomes

 Vx Wy - Wx Vy

 which becomes, splitting numerator and denominator,

 Vxa   Wyc     Wxa   Vyc
 --- * ---  -  --- * ---
 Vxb   Wyd     Wxb   Vyd

 This in turn becomes

 Wxb * Vyd * Vxa * Wyc  -  Vxb * Wyd * Wxa * Vyc
 -----------------------------------------------
             Vxb * Wyd * Wxb * Vyd

 And the other wedge, V^U is similar

 Vx Uy - Ux Vy

 Uxb * Vyd * Vxa * Uyc - Vxb * Uyd * Uxa * Vyc
 ---------------------------------------------
             Vxb * Uyd * Uxb * Vyd

 But this second is divded from the first, which is the same thing
 as to multiply it by it's inverse. So.

 (Wxb*Vyd*Vxa*Wyc - Vxb*Wyd*Wxa*Vyc)              Vxb*Uyd*Uxb*Vyd
 ----------------------------------- * -------------------------------------
             Vxb*Wyd*Wxb*Vyd           ( Uxb*Vyd*Vxa*Uyc - Vxb*Uyd*Uxa*Vyc )

 Already there is something to cancel

 (Wxb*Vyd*Vxa*Wyc - Vxb*Wyd*Wxa*Vyc)                  Uyd*Uxb
 ----------------------------------- * -------------------------------------
                 Wyd*Wxb               ( Uxb*Vyd*Vxa*Uyc - Vxb*Uyd*Uxa*Vyc )

 And to regroup

 [ (Vyd*Vxa)(Wxb*Vyd) - (Vxb*Vyc)(Wyd*Wxa) ]   Uyd*Uxb
 -----------------------------------------------------
 [ (Vyd*Vxa)(Uxb*Uyc) - (Vxb*Vyc)(Uyd*Uxa) ]   Wyd*Wxb

 Notice anything strange? Yes!

 Vyd*Vxa - appears twice
 Vxb*Vyc - appears twice

 This means we have boiled the transactio down to the following operations
 integer multiplication: 8 initial, all paralellizable
 integer subtraction: 2
 integer multiplication: 2 final

 Now, I know in Traditional Rational Number implementations, like GNU
 gmp, they run a greatest common divisor algorithm to reduce the fraction
 after every calculation. But we don't need to do that.

 We don't necessarily need to do anything. We could, if we wanted to draw
 a point, do a division... then again... didn't Bresenham prove that
 division is overrated when drawing stuff on a pixel screen? Not saying
 I have an algorithm here... I'm just saying. What if?

 What this program actually does is just do a conversion to Floating Point
 and then does a division, without any of these above optimizations.

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
	r = add( a, neg(b) )
	return
}

func mul(a, b Rational) (c Rational) {
	c.num = a.num * b.num
	c.denom = a.denom * b.denom
	return
}

func subpts( p2, p1 Point ) ( v Vector ) {
	v.x = sub( p2.x, p1.x )
	v.y = sub( p2.y, p1.y )
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

func find_intersect(w,v,u Vector) (q Point) {
	wedger := div(wedge(v,w),wedge(v,u))
	//fmt.Println("wedge vw", wedge(v,w), "wedge vu", wedge(v,u))
	qx := mul(u.x, wedger)
	qy := mul(u.y, wedger)
	return Point{qx,qy}
}

func raw_intersect( p1, p2, p3, p4 Point ) (q Point) {
	w := subpts(p1,p3)
	u := subpts(p4,p3)
	v := subpts(p2,p1)
	return find_intersect( w, u, v )
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

	q := find_intersect( w,v,u )

	fmt.Println("<!--",w,v,u,q,"-->")
	fmt.Println(svgpoint(q))
	fmt.Println(svgend())

}
