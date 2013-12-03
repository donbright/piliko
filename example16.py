from piliko import *

# Replicate a picture from one of NJ Wildberger's chromogeometry papers

t=triangle([2,7],[25,12],[9,20])
cb,cr,cg=blue_circumcenter(t),red_circumcenter(t),green_circumcenter(t)
nb,nr,ng=blue_ninepoint_center(t),red_ninepoint_center(t),green_ninepoint_center(t)
Ob,Or,Og=blue_orthocenter(t),red_orthocenter(t),green_orthocenter(t)
ct = triangle( cb, cr, cg )
ot = triangle( Ob, Or, Og )
circles  = [blue_circumcircle(t),red_circumcircle(t),green_circumcircle(t)]
circles += [blue_ninepointcircle(t),red_ninepointcircle(t),green_ninepointcircle(t)]
# different way to construct circles. center point + radial quadrance
bK,rK,gK = blueq( Ob, t[0] ), redq( Or, t[0] ), greenq( Og, t[0] )
circles += [circle( cb, bK ),circle( cr, rK), circle( cg, gK )]
g=centroid(t)

plot_points(g,cb,cr,cg,nb,nr,ng,Ob,Or,Og)
plot_triangles(t,ot,ct)
plot_blue_circles( circles[0],circles[3] )
plot_red_circles( circles[1],circles[4] )
plot_green_circles( circles[2],circles[5] )
plotshow()
