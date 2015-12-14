
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
  var num,denom int
  x := a.num * b.denom
  y := b.num * a.denom
  z := b.denom * a.denom
  num,denom = x+y,z
  c = Ratnum{ num, denom }
  return c
}

func norm( a Ratnum, normstyle int ) (c Ratnum ) {
  if (normstyle==0) {
    c = a
  } else {
    c = Ratnum{ a.num % (maxint), a.denom % (maxint) }
  }
  return c
}

func printop_mul(nums []Ratnum, normstyle int) {
  fmt.Print("  *   | ")
  for j:=0;j<len(nums);j++ {
    fmt.Print(nums[j]," ")
  }
  fmt.Println("\n-------------------------------------------------------------")
  for i:=0;i<len(nums);i++ {
    fmt.Print(nums[i]," | ")
    for j:=0;j<len(nums);j++ {
      fmt.Print(norm(mul(nums[i],nums[j]),normstyle)," ")
    }
    fmt.Println()
  }
}

func printop_add(nums []Ratnum, normstyle int) {
  fmt.Print("  +   | ")
  for j:=0;j<len(nums);j++ {
    fmt.Print(nums[j]," ")
  }
  fmt.Println("\n-------------------------------------------------------------")
  for i:=0;i<len(nums);i++ {
    fmt.Print(nums[i]," | ")
    for j:=0;j<len(nums);j++ {
      fmt.Print(norm(add(nums[i],nums[j]),normstyle)," ")
    }
    fmt.Println()
  }
}

func max(l []Ratnum) (c int) {
  for _,v := range l {
    if v.num>c { c=v.num }
    if v.denom>c { c=v.denom }
  }
  return
}

func main() {
  fmt.Println("Hello Go")
  var nums []Ratnum
  //nums := []Ratnum{{0,0},{0,1},{0,2},{1,0},{1,1},{1,2},{2,0},{2,1},{2,2}}
  //maxint = max( nums )
  maxint = 4
  for i:=0;i<maxint;i++ {
    for j:=0;j<maxint;j++ {
      nums = append(nums,Ratnum{i,j})
    }
  }
  //nums := []Ratnum{{0,0},{0,1},{1,0},{1,1}}
  printop_mul( nums, 0 )
  fmt.Println()
  printop_mul( nums, 1 )
  fmt.Println()
  printop_add( nums, 0 )
  fmt.Println()
  printop_add( nums, 1 )
}
