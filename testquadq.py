from piliko import *

# test quadruple-quad formulas

a,d=point(0,0),point(8,1)
b=midpoint(a,d)
c=midpoint(b,d)

print 'collinear?',collinear(a,b,c,d)

bqs,rqs,gqs = [],[],[]
bqs += [blueq(a,b)]
bqs += [blueq(b,c)]
bqs += [blueq(c,d)]
bqs += [blueq(d,a)]

rqs += [redq(a,b)]
rqs += [redq(b,c)]
rqs += [redq(c,d)]
rqs += [redq(d,a)]

gqs += [greenq(a,b)]
gqs += [greenq(b,c)]
gqs += [greenq(c,d)]
gqs += [greenq(d,a)]

print 'blueqs:', bqs
print 'redqs:', rqs
print 'greenqs:', gqs

bqq = quadruple_quad( bqs )
rqq = quadruple_quad( rqs )
gqq = quadruple_quad( gqs )
print bqq
print rqq
print gqq

plot_points(a,b,c,d)
plotshow()
