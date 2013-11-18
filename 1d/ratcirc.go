package main
import "fmt"
/* 
 calculate one hundred million points on the unit circle

 a simple example of paralell speedup in go

 run on a multi-core machine with GOMAXPROCS=1 then with GOMAXPROCS=2
 the second run will be fasyer than the first.
*/
const num_m = 10000
const num_n = 10000
const numpoints = num_m * num_m
var xs [numpoints]float64
var ys [numpoints]float64

func dohalf( lo_m int, hi_m int, c chan []int ) {
	for m:= lo_m ; m < hi_m; m++ {
		for n:= 0; n < num_n ; n++ {
			blueq := float64( m*m + n*n )
			redq := float64( m*m - n*n )
			greenq := float64( 2*m*n )
			xs[m*num_n+n] = redq/blueq
			ys[m*num_n+n] = greenq/blueq
		}
	}
	c <- []int{lo_m,hi_m}
} 

func main() {
	var c1 chan []int = make(chan []int)
	var c2 chan []int = make(chan []int)
	go dohalf(       0, num_m/2, c1 ) 
	go dohalf( num_m/2,   num_m, c2 ) 
	fmt.Println( "finis", <- c1, <- c2 )
}
