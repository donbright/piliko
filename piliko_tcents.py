from piliko_asymp import *
from piliko import *
############################### triangle centers


############## orthocenters

def blue_orthocenter_from_triangle( t ):
	if not checktype(triangle,t): raise Exception('need triangle')
	terma = eval_asympoly( 'x1*x2*y2', t )
	termb = eval_asympoly( 'y1*y2*y2', t )
	termc = eval_asympoly( 'x1*y2', t )
	termd = eval_asympoly( 'x1*y1*y2', t )
	terme = eval_asympoly( 'x1*x1*x2', t )
	termf = eval_asympoly( 'x1*y2', t )
	x = Fraction( terma + termb, termc )
	y = Fraction( termd + terme, termf )
	return point(x,y)

def red_orthocenter_from_triangle( t ):
	if not checktype(triangle,t): raise Exception('need triangle')
	terma = eval_asympoly( 'x1*x2*y2', t )
	termb = eval_asympoly( 'y1*y2*y2', t )
	termc = eval_asympoly( 'x1*y2', t )
	termd = eval_asympoly( 'x1*y1*y2', t )
	terme = eval_asympoly( 'x1*x1*x2', t )
	termf = eval_asympoly( 'x1*y2', t )
	x = Fraction( terma - termb, termc )
	y = Fraction( termd - terme, termf )
	return point(x,y)

def green_orthocenter_from_triangle( t ):
	if not checktype(triangle,t): raise Exception('need triangle')
	terma = eval_asympoly( 'x1*x1*y2', t )
	termb = eval_asympoly( 'x1*x2*y1', t )
	termc = eval_asympoly( 'x1*y2', t )
	termd = eval_asympoly( 'x1*y2*y2', t )
	terme = eval_asympoly( 'x1*y1*y2', t )
	termf = eval_asympoly( 'x1*y2', t )
	x = Fraction( terma + termb, termc )
	y = Fraction( termd - terme, termf )
	return point(x,y)

def blue_orthocenter_from_points( p1, p2, p3 ):
	t = triangle( p1, p2, p3 )
	blue_orthocenter_from_triangle( t )
def red_orthocenter_from_points( p1, p2, p3 ):
	t = triangle( p1, p2, p3 )
	red_orthocenter_from_triangle( t )
def green_orthocenter_from_points( p1, p2, p3 ):
	t = triangle( p1, p2, p3 )
	green_orthocenter_from_triangle( t )


def blue_orthocenter( *args ):
	if checktype(triangle, args[0]):
		return blue_orthocenter_from_triangle( args[0] )
	if checktype(point, args[0]) and checktype(point, args[1]):
		if checktype(point, args[2]):
			p1,p2,p3=args[0],args[1],args[2]
			return blue_orthocenter_from_points( p1, p2, p3 )
def red_orthocenter( *args ):
	if checktype(triangle, args[0]):
		return red_orthocenter_from_triangle( args[0] )
	if checktype(point, args[0]) and checktype(point, args[1]):
		if checktype(point, args[2]):
			p1,p2,p3=args[0],args[1],args[2]
			return red_orthocenter_from_points( p1, p2, p3 )
def green_orthocenter( *args ):
	if checktype(triangle, args[0]):
		return green_orthocenter_from_triangle( args[0] )
	if checktype(point, args[0]) and checktype(point, args[1]):
		if checktype(point, args[2]):
			p1,p2,p3=args[0],args[1],args[2]
			return green_orthocenter_from_points( p1, p2, p3 )

orthocenter=blue_orthocenter


def blue_centroid( t ):
	x = avg(t.p0.x,t.p1.x,t.p2.x)	
	y = avg(t.p0.y,t.p1.y,t.p2.y)	
	return point(x,y)
def red_centroid( t ):
	return blue_centroid(t)
def green_centroid( t ):
	return blue_centroid(t)
centroid=blue_centroid

############ circumcenters

def blue_circumcenter_from_triangle( t ):
	if not checktype(triangle,t): raise Exception('need triangle')
	terma = eval_asympoly( 'x1*x1*y2', t )
	termb = eval_asympoly( 'y1*y1*y2', t )
	termc = eval_asympoly( 'x1*y2', t )
	termd = eval_asympoly( 'x1*y2*y2', t )
	terme = eval_asympoly( 'x1*x2*x2', t )
	termf = eval_asympoly( 'x1*y2', t )
	x = Fraction( terma + termb, 2 * termc )
	y = Fraction( termd + terme, 2 * termf )
	return point(x,y)

def red_circumcenter_from_triangle( t ):
	if not checktype(triangle,t): raise Exception('need triangle')
	terma = eval_asympoly( 'x1*x1*y2', t )
	termb = eval_asympoly( 'y1*y1*y2', t )
	termc = eval_asympoly( 'x1*y2', t )
	termd = eval_asympoly( 'x1*y2*y2', t )
	terme = eval_asympoly( 'x1*x2*x2', t )
	termf = eval_asympoly( 'x1*y2', t )
	x = Fraction( terma - termb, 2 * termc )
	y = Fraction( termd - terme, 2 * termf )
	return point(x,y)

def green_circumcenter_from_triangle( t ):
	if not checktype(triangle,t): raise Exception('need triangle')
	terma = eval_asympoly( 'x1*x2*y2', t )
	termb = 0
	termc = eval_asympoly( 'x1*y2', t )
	termd = eval_asympoly( 'x1*y1*y2', t )
	terme = 0
	termf = eval_asympoly( 'x1*y2', t )
	x = Fraction( terma + termb, termc )
	y = Fraction( termd - terme, termf )
	return point(x,y)

def blue_circumcenter_from_points( p1, p2, p3 ):
	t = triangle( p1, p2, p3 )
	blue_circumcenter_from_triangle( t )
def red_circumcenter_from_points( p1, p2, p3 ):
	t = triangle( p1, p2, p3 )
	red_circumcenter_from_triangle( t )
def green_circumcenter_from_points( p1, p2, p3 ):
	t = triangle( p1, p2, p3 )
	green_circumcenter_from_triangle( t )


def blue_circumcenter( *args ):
	if checktype(triangle, args[0]):
		return blue_circumcenter_from_triangle( args[0] )
	if checktype(point, args[0]) and checktype(point, args[1]):
		if checktype(point, args[2]):
			p1,p2,p3=args[0],args[1],args[2]
			return blue_circumcenter_from_points( p1, p2, p3 )
def red_circumcenter( *args ):
	if checktype(triangle, args[0]):
		return red_circumcenter_from_triangle( args[0] )
	if checktype(point, args[0]) and checktype(point, args[1]):
		if checktype(point, args[2]):
			p1,p2,p3=args[0],args[1],args[2]
			return red_circumcenter_from_points( p1, p2, p3 )
def green_circumcenter( *args ):
	if checktype(triangle, args[0]):
		return green_circumcenter_from_triangle( args[0] )
	if checktype(point, args[0]) and checktype(point, args[1]):
		if checktype(point, args[2]):
			p1,p2,p3=args[0],args[1],args[2]
			return green_circumcenter_from_points( p1, p2, p3 )

circumcenter=blue_circumcenter


######################## nine point centers

def blue_ninepointcenter_from_triangle( t ):
	if not checktype(triangle,t): raise Exception('need triangle')
	p1 = red_circumcenter_from_triangle( t )
	p2 = green_circumcenter_from_triangle( t )
	return midpoint_from_points( p1, p2 )

def red_ninepointcenter_from_triangle( t ):
	if not checktype(triangle,t): raise Exception('need triangle')
	p1 = blue_circumcenter_from_triangle( t )
	p2 = green_circumcenter_from_triangle( t )
	return midpoint_from_points( p1, p2 )

def green_ninepointcenter_from_triangle( t ):
	if not checktype(triangle,t): raise Exception('need triangle')
	p1 = blue_circumcenter_from_triangle( t )
	p2 = red_circumcenter_from_triangle( t )
	return midpoint_from_points( p1, p2 )

def blue_ninepointcenter_from_points( p1, p2, p3 ):
	t = triangle( p1, p2, p3 )
	return blue_ninepointcenter_from_triangle( t )
def red_ninepointcenter_from_points( p1, p2, p3 ):
	t = triangle( p1, p2, p3 )
	return red_ninepointcenter_from_triangle( t )
def green_ninepointcenter_from_points( p1, p2, p3 ):
	t = triangle( p1, p2, p3 )
	return green_ninepointcenter_from_triangle( t )

def blue_ninepointcenter( *args ):
	if checktype(triangle, args[0]):
		return blue_ninepointcenter_from_triangle( args[0] )
	elif checktype(point, args[0]) and checktype(point, args[1]):
		if checktype(point, args[2]):
			p1,p2,p3=args[0],args[1],args[2]
			return blue_ninepointcenter_from_points( p1, p2, p3 )
	else: raise Exception('unknown input type')
def red_ninepointcenter( *args ):
	if checktype(triangle, args[0]):
		return red_ninepointcenter_from_triangle( args[0] )
	elif checktype(point, args[0]) and checktype(point, args[1]):
		if checktype(point, args[2]):
			p1,p2,p3=args[0],args[1],args[2]
			return red_ninepointcenter_from_points( p1, p2, p3 )
	else: raise Exception('unknown input type')
def green_ninepointcenter( *args ):
	if checktype(triangle, args[0]):
		return green_ninepointcenter_from_triangle( args[0] )
	elif checktype(point, args[0]) and checktype(point, args[1]):
		if checktype(point, args[2]):
			p1,p2,p3=args[0],args[1],args[2]
			return green_ninepointcenter_from_points( p1, p2, p3 )
	else: raise Exception('unknown input type')
ninepointcenter=blue_ninepointcenter



