from piliko import *

print
print 'example 6'
print 'determinant, with vectors as input-rows'
det = determinant
va,vb = vector(3,1),vector(4,5)
print 'va, vb, determinant(va,vb), det(vb,va):',va,vb,det(va,vb),det(vb,va)	
v1,v2,v3=vector(3,0,0),vector(0,4,0),vector(0,0,5)
print 'v1,v2,v3:',v1,v2,v3
print 'determinant of ( v1,v2,v3 ):',det(v1,v2,v3)

v4,v5=vector(1,3),vector(-1,4)	
print 'v4,v5,det(v4,v5),det(v4,v4+v5)',v4,v5,det(v4,v5),det(v4,v5+v4*3)	

print 'solid spread of v1,v2,v3:',solid_spread(v1,v2,v3)
print 'solid spread of v1,v2,(3,2,-2):',solid_spread(v1,v2,vector(3,2,-2))
