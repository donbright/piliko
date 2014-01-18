from piliko import *
print 'centers of triangles'

p1,p2,p3=point(0,0),point(4,0),point(4,3)
t = triangle(p1,p2,p3)
print 'triangle:',t
boc = blue_orthocenter(t)
roc = red_orthocenter(t)
goc = green_orthocenter(t)
bcc = blue_circumcenter(t)
rcc = red_circumcenter(t)
gcc = green_circumcenter(t)
print 'orthocenters. blue:',boc,'red:',roc,'green:',goc
print 'circumcenters. blue:',bcc,'red:',rcc,'green:',gcc
ot = omega_triangle( t )
print 'omega triangle:', ot

print
p1,p2,p3=point(0,0),point(12,2),point(4,6)
t = triangle(p1,p2,p3)
ot = omega_triangle( t )
print 'example13.2:'
print 'points:',p1,p2,p3
print 'triangle:',t
print 'omega triangle:',ot



print
p1,p2,p3=point(12+4,2+6),point(12,2),point(4,6)
t = triangle(p1,p2,p3)
ot = omega_triangle( t )
print 'example13.4:'
print 'points:',p1,p2,p3
print 'triangle:',t
print 'omega triangle:',ot

plot_triangles([t,ot])
plotshow()
