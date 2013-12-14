from piliko import *
from random import randint

# given a circle, and the slope of a line, find the full equation of the line
# that is tangent to the circle.

# equation is generated as follows
#
# Eqn of cricle: x^2+y^2=r^2   = Quadrance
# 
# Eqn of tangent line: ax+by+c= 0     c is our unknown.
# We are given a and b, remember? a, and b make up the slope. 
# You can also think of y=mx+k, and say we are looking for k, given b
# and given the circle.
#
# Step 0. translate circle to origin to make life easier.
#
# Now, step 1, find line perpendicular to ax+by+??=0 that passes trhu circl
# center. No problem. flip the slope and make it negative. -bx+ay=0 and no
# 'c'. We pass thru circle center which is at 0,0.
# Step 2 find intersection of line from step 1 w circle. 
####   y=bx/a, plug into circ eqn, x^2+(bx/a)^2=Q, solve for x.
# x = sqrt(some mess )
# Step 2.b, solve for y, y=bx/a, and x from prev step.
#
# Step 3 now we have a point. traanslate it back to where the circle was.
# (newx=x+centerx)(newy=y+centery)
#
# Step 4. Find the 'c' for the line eq. Well, given a point, we can 
# solve ax+by+c=0 for c. plug in point.x, point.y, a, and b. c will be 
# the negative.

# Step 5 realize that we have two lines here... corresponding to plus or minus
# sqrt when solving the equation for x. so our result will be two lines!

depth=10

# we only deal with rationals, so sqrt has to have perfect squares as input.
# Therefore, the slope of the line, a, and b, must be legs of rational 
# Pythagorean triples. These three lines of code ensure that.
m,n=randint(1,depth),randint(1,depth)
a=Fraction(redq(m,n),blueq(m,n))
b=Fraction(greenq(m,n),blueq(m,n))

circ=circle(randint(1,depth),randint(1,depth),sqr(randint(1,depth)))
print circ
l=line(a,b,0)
l2=line(-b,a,0)
tmp=Fraction(circ.radial_quadrance,Fraction(sqr(b),sqr(a))+1)
meetx1=perfect_square_root(tmp)
meety1=Fraction(b,a)*meetx1
meetx2=-perfect_square_root(tmp)
meety2=Fraction(b,a)*meetx2
meetx3=meetx1+circ.center.x
meety3=meety1+circ.center.y
meetx4=meetx2+circ.center.x
meety4=meety2+circ.center.y
c3=-1*(a*meetx3+b*meety3)
c4=-1*(a*meetx4+b*meety4)
l3=line(a,b,c3)
l4=line(a,b,c4)
print l,l2,l3,l4
plot_lines(l,l2,l3,l4)
plot_circle(circ)
plotshow()
