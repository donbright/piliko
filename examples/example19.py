from piliko import *

l=line(12,2,3)
l2=line(3,2,-21)
l3=line(9,4,-1)
p=meet(l,l2)
p2=meet(l3,l2)
p3=meet(l3,l)
print l,l2,l3
print p,p2,p3
plot_points(p,p2,p3)
plot_line( l )
plot_line( l2 )
plot_line( l3 )
plot_show()
