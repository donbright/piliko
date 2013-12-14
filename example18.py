from piliko import *

pl1 = plane(1,2,3,-3)

pt1 = point(1,2,3)
pt2 = point(1,Fraction(1,2),Fraction(1,3))
pt3 = point(Fraction(1,2),Fraction(3,4),Fraction(1,3))
pt4 = point(1,Fraction(3,4),Fraction(1,6))

pl2 = plane(pt2,pt3,pt4)

print '\npart 1: basic planes\n'
print 'points:',pt1,pt2,pt3,pt4
print 'planes:',pl1,pl2
print 'pl1 meets:',meet(pt1,pl1),meet(pt2,pl1),meet(pt3,pl1),meet(pt4,pl1)
print 'pl2 meets:',meet(pt1,pl2),meet(pt2,pl2),meet(pt3,pl2),meet(pt4,pl2)

print '\npart 2: decimal->floating point vs decimal->rationals\n'
print '\npart 2a: decimal->floating point->rational\n'

decimal_o6 = '0.6' 
decimal_o7 = '0.7' 
decimal_o8 = '0.8' 
float_o6 = float(decimal_o6) 
float_o7 = float(decimal_o7) 
float_o8 = float(decimal_o8) 
p1=point(0,0, Fraction(float_o6) ) 
p2=point(1,0, Fraction(float_o7) )
p3=point(1,1, Fraction(float_o8) )
p4=point(0,1, Fraction(float_o7) ) 

print 'decimal heights:',decimal_o6,decimal_o7,decimal_o8,decimal_o7
print 'floating point heights:',float_o6, float_o7,float_o8
print 'points:',p1,p2,p3,p4
plupper = plane(p2,p3,p4)
pllower = plane(p1,p2,p4)
print 'lower plane:',pllower
print 'upper plane:',plupper
print 'intersection of each point with upper plane:'
print meet(p1,plupper),meet(p2,plupper),meet(p3,plupper),meet(p4,plupper)
print 'intersection of each point with lower plane:'
print meet(p1,pllower),meet(p2,pllower),meet(p3,pllower),meet(p4,pllower)


print '\npart 2b: decimal->rational\n'

rat_o6 = Fraction('6/10')
rat_o7 = Fraction('7/10')
rat_o8 = Fraction('8/10')
p1=point(0,0, rat_o6 ) 
p2=point(1,0, rat_o7 )
p3=point(1,1, rat_o8 )
p4=point(0,1, rat_o7 ) 

print 'rational heights:',rat_o6,rat_o7,rat_o8
print 'points:',p1,p2,p3,p4
plupper = plane(p2,p3,p4)
pllower = plane(p1,p2,p4)
print 'lower plane:',pllower
print 'upper plane:',plupper
print 'intersection of each point with upper plane:'
print meet(p1,plupper),meet(p2,plupper),meet(p3,plupper),meet(p4,plupper)
print 'intersection of each point with lower plane:'
print meet(p1,pllower),meet(p2,pllower),meet(p3,pllower),meet(p4,pllower)

print

