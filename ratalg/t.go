
/* what happens if you treat a denominator of 0 like you would any
other integer?

and. you have a limited amount of space for numerator and denominator.
for example, imagine you can only store the numbers 0, 1, and 2.
*/

package main

import "fmt"

var maxint int

type Ratnum struct {
  num,denom int
}

func mul(a, b Ratnum) (c Ratnum) {
  c = Ratnum{ ( a.num * b.num ) , ( a.denom * b.denom ) }
  return c
}

func add(a, b Ratnum) (c Ratnum) {
  c = Ratnum{a.num*b.denom+b.num*a.denom,b.denom*a.denom}
  return c
}

func norm( a Ratnum ) (c Ratnum ) {
  c = Ratnum{a.num % (maxint+1), a.denom % (maxint+1)}
  return c
}

func printop_mul(nums []Ratnum) {
  fmt.Print("  *   | ")
  for j:=0;j<len(nums);j++ {
    fmt.Print(nums[j]," ")
  }
  fmt.Println("\n-------------------------------------------------------------")
  for i:=0;i<len(nums);i++ {
    fmt.Print(nums[i]," | ")
    for j:=0;j<len(nums);j++ {
      fmt.Print(norm(mul(nums[i],nums[j]))," ")
    }
    fmt.Println()
  }
}

func printop_add(nums []Ratnum) {
  fmt.Print("  +   | ")
  for j:=0;j<len(nums);j++ {
    fmt.Print(nums[j]," ")
  }
  fmt.Println("\n-------------------------------------------------------------")
  for i:=0;i<len(nums);i++ {
    fmt.Print(nums[i]," | ")
    for j:=0;j<len(nums);j++ {
      fmt.Print(norm(add(nums[i],nums[j]))," ")
    }
    fmt.Println()
  }
}

func main() {
  maxint = 2
  fmt.Println("Hello Go")
  nums := []Ratnum{{0,0},{0,1},{0,2},{1,0},{1,1},{1,2},{2,0},{2,1},{2,2}}
  printop_mul( nums )
  fmt.Println()
  printop_add( nums )
}
