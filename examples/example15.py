from piliko import *

# this example shows the plotting of red and green circles with
# negative radial quadrances.
c1=circle((0,0),4)
c2=circle((0,0),-4)

plot_red_circles([c1,c2])
plot_blue_circles(c1)
plot_green_circles(c1,c2)
plotshow()
