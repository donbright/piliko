from piliko import *
from random import randint

# perpendicularity
# defined as 'the line which is tangent to the given line, with respect
# to a given circle'. 

bcircs=[circle(0,0,Fraction(1,1))]
rcircs=[circle(0,0,Fraction(1,1))]
gcircs=[circle(0,0,Fraction(1,1))]
v1=line(4,3,0)
lbp=blue_find_perpendicular_line(v1)
lrp=red_find_perpendicular_line(v1)
lgp=green_find_perpendicular_line(v1)

plot_blue_circles(bcircs)
plot_red_circles(rcircs)
plot_green_circles(gcircs)
plot_lines([v1,lbp,lrp,lgp])
plotshow()
