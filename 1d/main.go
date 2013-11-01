package main
import "fmt"
type Point struct {
	a, b int
}
func avg(xs []int) (int,int) {
	tot := 0
	for _,val:= range(xs) {
		tot += val
	}
	return tot, tot/len(xs)
}
func ( p *Point ) decimal_approx() float64 {
	return float64(p.a)/float64(p.b)
}
func main() {
	n := []int{1*2,2*4,3*2,4*2,5/2}
	m := n[0:len(n)]
	for a:=0; a<10; a++ {
		fmt.Println("Hello " + "5", 1, a)
		if a%2==0 { fmt.Println("ok") } else { fmt.Println("nok") }
		if a<len(n) { fmt.Println("a:",a,"n[a]:",n[a]) }
		fmt.Println(m[0])
	}
	x := make(map[string]int)
	x["aloo"]=1
	x["aloo2"]=2
	x["aloo3"]=3
	fmt.Println(x)
	delete(x,"aloo")
	fmt.Println(x)
	if answer, status := x["tent"]; status {
		fmt.Println("lookup ok", answer,status)
	} else {
		fmt.Println("main lookup not ok. alt:", answer,status)
		answer, status = x["aloo3"]
	}
	color := map[string]int{
		"Red":0x110000,
		"Blue":0x000011,
		"Green":0x001100,
	}
	fmt.Println(color)
	for i, ni := range n { fmt.Println( i, ni ) }
	answer,answer2 := avg(n)
	fmt.Println( answer,answer2 )
	p1 := Point{0,1}
	p2 := Point{1,1}
	fmt.Println( p1, p2,p1.a,p1.b,p2.a,p2.b )	
	p1a:=p1.decimal_approx()
	p2a:=p2.decimal_approx()
	fmt.Println( p1a, p2a )
}
