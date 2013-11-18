import "fmt"

func main() {
/*	a := Rational{1,2}
	b := Rational{2,4}
	c := Rational{-2,1}
	d := Rational{3,1}
	e := Rational{2,-1}
*/
/*
	a := Rational{2,-1}
	b := Rational{-2,1}
	c := Rational{-2,-1}
	d := Rational{3,1}
	e := Rational{-3,1}
*/
/*
	a := Rational{2322,-1}
	b := Rational{-2122,1223}
	c := Rational{-23344,-1344}
	d := Rational{333,444441}
	e := Rational{-3300030,1333333}
*/
	a := Rational{1,0}
	b := Rational{5,12}
	c := Rational{1,0}
	d := Rational{2,3}
	e := Rational{-1,4}

	fmt.Println( "  a      b      c      d      e\n", a, b, c, d, e )
	fmt.Println( "blueq( 0,0,d,e )",blueq(rat(0),rat(0),d,e))
	fmt.Println()
	fmt.Println( "a+a a+b a+c a+d a+e", add(a,a), add(a,b), add(a,c), add(a,d), add(a,e) )
	fmt.Println( "b+a b+b b+c b+d b+e", add(b,a), add(b,b), add(b,c), add(b,d), add(b,e) )
	fmt.Println( "c+a c+b c+c c+d c+e", add(c,a), add(c,b), add(c,c), add(c,d), add(c,e) )
	fmt.Println( "d+a d+b d+c d+d d+e", add(d,a), add(d,b), add(d,c), add(d,d), add(d,e) )
	fmt.Println( "e+a e+b e+c e+d e+e", add(e,a), add(e,b), add(e,c), add(e,d), add(e,e) )
	fmt.Println()
	fmt.Println( "a-a a-b a-c a-d a-e", sub(a,a), sub(a,b), sub(a,c), sub(a,d), sub(a,e) )
	fmt.Println( "b-a b-b b-c b-d b-e", sub(b,a), sub(b,b), sub(b,c), sub(b,d), sub(b,e) )
	fmt.Println( "c-a c-b c-c c-d c-e", sub(c,a), sub(c,b), sub(c,c), sub(c,d), sub(c,e) )
	fmt.Println( "d-a d-b d-c d-d d-e", sub(d,a), sub(d,b), sub(d,c), sub(d,d), sub(d,e) )
	fmt.Println( "e-a e-b e-c e-d e-e", sub(e,a), sub(e,b), sub(e,c), sub(e,d), sub(e,e) )
	fmt.Println()
	fmt.Println( "a<a a<b a<c a<d a<e", lt(a,a), lt(a,b), lt(a,c), lt(a,d), lt(a,e) )
	fmt.Println( "b<a b<b b<c b<d b<e", lt(b,a), lt(b,b), lt(b,c), lt(b,d), lt(b,e) )
	fmt.Println( "c<a c<b c<c c<d c<e", lt(c,a), lt(c,b), lt(c,c), lt(c,d), lt(c,e) )
	fmt.Println( "d<a d<b d<c d<d d<e", lt(d,a), lt(d,b), lt(d,c), lt(d,d), lt(d,e) )
	fmt.Println( "e<a e<b e<c e<d e<e", lt(e,a), lt(e,b), lt(e,c), lt(e,d), lt(e,e) )
	fmt.Println()
	fmt.Println( "a>a a>b a>c a>d a>e", gt(a,a), gt(a,b), gt(a,c), gt(a,d), gt(a,e) )
	fmt.Println( "b>a b>b b>c b>d b>e", gt(b,a), gt(b,b), gt(b,c), gt(b,d), gt(b,e) )
	fmt.Println( "c>a c>b c>c c>d c>e", gt(c,a), gt(c,b), gt(c,c), gt(c,d), gt(c,e) )
	fmt.Println( "d>a d>b d>c d>d d>e", gt(d,a), gt(d,b), gt(d,c), gt(d,d), gt(d,e) )
	fmt.Println( "e>a e>b e>c e>d e>e", gt(e,a), gt(e,b), gt(e,c), gt(e,d), gt(e,e) )
	fmt.Println()
	fmt.Println( "a=a a=b a=c a=d a=e", eq(a,a), eq(a,b), eq(a,c), eq(a,d), eq(a,e) )
	fmt.Println( "b=a b=b b=c b=d b=e", eq(b,a), eq(b,b), eq(b,c), eq(b,d), eq(b,e) )
	fmt.Println( "c=a c=b c=c c=d c=e", eq(c,a), eq(c,b), eq(c,c), eq(c,d), eq(c,e) )
	fmt.Println( "d=a d=b d=c d=d d=e", eq(d,a), eq(d,b), eq(d,c), eq(d,d), eq(d,e) )
	fmt.Println( "e=a e=b e=c e=d e=e", eq(e,a), eq(e,b), eq(e,c), eq(e,d), eq(e,e) )
	fmt.Println()
	fmt.Println( "a*a a*b a*c a*d a*e", mul(a,a), mul(a,b), mul(a,c), mul(a,d), mul(a,e) )
	fmt.Println( "b*a b*b b*c b*d b*e", mul(b,a), mul(b,b), mul(b,c), mul(b,d), mul(b,e) )
	fmt.Println( "c*a c*b c*c c*d c*e", mul(c,a), mul(c,b), mul(c,c), mul(c,d), mul(c,e) )
	fmt.Println( "d*a d*b d*c d*d d*e", mul(d,a), mul(d,b), mul(d,c), mul(d,d), mul(d,e) )
	fmt.Println( "e*a e*b e*c e*d e*e", mul(e,a), mul(e,b), mul(e,c), mul(e,d), mul(e,e) )
	fmt.Println()
	fmt.Println( "a/a a/b a/c a/d a/e", div(a,a), div(a,b), div(a,c), div(a,d), div(a,e) )
	fmt.Println( "b/a b/b b/c b/d b/e", div(b,a), div(b,b), div(b,c), div(b,d), div(b,e) )
	fmt.Println( "c/a c/b c/c c/d c/e", div(c,a), div(c,b), div(c,c), div(c,d), div(c,e) )
	fmt.Println( "d/a d/b d/c d/d d/e", div(d,a), div(d,b), div(d,c), div(d,d), div(d,e) )
	fmt.Println( "e/a e/b e/c e/d e/e", div(e,a), div(e,b), div(e,c), div(e,d), div(e,e) )
	fmt.Println()
	fmt.Println( "mul(mul(mul(sub(add(mul(div(a,b),c),e),c),d),e),d) )",mul(mul(mul(sub(add(mul(div(a,b),c),e),c),d),e),d) )
	for i:=0; i<5; i++ { a = mul(a,a) }
	fmt.Println( "overflow?", a == Rational{0,1} )
}
