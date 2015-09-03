# example of where rationals fail. 
# this simple simulation of newton gravity slows to a crawl
# due to massive integer overflow
# after just a few iterations

from fractions import Fraction

grav=Fraction(5)

def sqr(x): return x*x
# blue quadrance
def bq3(x,y): return sqr(x[0]-y[0])+sqr(x[1]-y[1])+sqr(x[2]-y[2])
def sign(x):
	if x==0: return 0
	if x>0: return 1
	return -1


class Body:
	def __init__(self):
		self.mass=0
		self.position=[0,0,0]
		self.velocity=[0,0,0]
		self.accel=[0,0,0]
	def update(self,b):
		dirx = -sign(self.position[0]-b.position[0])
		diry = -sign(self.position[1]-b.position[1])
		dirz = -sign(self.position[2]-b.position[2])
		q3x=sqr(self.position[0]-b.position[0])
		q3y=sqr(self.position[1]-b.position[1])
		q3z=sqr(self.position[2]-b.position[2])
		q3=q3x+q3y+q3z
		force = Fraction(grav*self.mass*b.mass,(q3))
		a = Fraction(force,self.mass)
		self.accel[0] = dirx * a * Fraction(q3x,q3)
		self.accel[1] = diry * a * Fraction(q3y,q3)
		self.accel[2] = dirz * a * Fraction(q3z,q3)
		for i in range(0,3): self.velocity[i] += self.accel[i]
		for i in range(0,3): self.position[i] += self.velocity[i]

planet = Body()
ship = Body()
grav=Fraction(1)
planet.mass=1
ship.mass=1
ship.position=[2,0,0]
for counter in range(0,20):
	oldship = ship
	ship.update(planet)
	planet.update(oldship)
#	planet.update(ship)
	print float(ship.position[0]),
	print float(ship.position[1]),
	print float(ship.position[2])
	print float(planet.position[0]),
	print float(planet.position[1]),
	print float(planet.position[2])
	print '-'
	#print planet.position


