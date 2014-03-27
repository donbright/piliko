# this demo shows that in a floating point math
# x+1 doesnt always mean what you think it means.
# (in this example, x+1 == x+2)

x=18014398509481982.0
print 'x=',type(x)
print 'x=',int(x)
print 'x=',x
print 'x+1:'
x+=1
print int(x)
print x



