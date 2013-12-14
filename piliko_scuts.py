from piliko_plot import *
from piliko_tcents import *
from piliko import *

####################################3 shortcuts and conveniene functions
############ for the spelling challenged, frogetful, and inebriated

def is_paralell( l1, l2):
	return is_parallel( l1, l2 )

def is_parallel( l1, l2):
	return spread( l1, l2 ) == 0

def intersection( l1, l2 ):
	return meet( l1, l2 )

# nice for doing paramterizations
def blueq( *args ):
	if checktypes(point,*args):
		if len(args)==1:
			return blue_quadrance(point(0,0),args[0])
		elif len(args)==2:
			return blue_quadrance(args[0],args[1])
		else: raise Exception('need 1 or 2 pts')
	elif checkrationals(*args):
		return blue_quadrance(point(0,0),point(args[0],args[1]))
	else: raise Exception('need point or x,y coords')
def redq( *args ):
	if checktypes(point,*args):
		if len(args)==1:
			return red_quadrance(point(0,0),args[0])
		elif len(args)==2:
			return red_quadrance(args[0],args[1])
		else: raise Exception('need 1 or 2 pts')
	elif checkrationals(*args):
		return red_quadrance(point(0,0),point(args[0],args[1]))
	else: raise Exception('need point or x,y coords')
def greenq( *args ):
	if checktypes(point,*args):
		if len(args)==1:
			return green_quadrance(point(0,0),args[0])
		elif len(args)==2:
			return green_quadrance(args[0],args[1])
		else: raise Exception('need 1 or 2 pts')
	elif checkrationals(*args):
		return green_quadrance(point(0,0),point(args[0],args[1]))
	else: raise Exception('need point or x,y coords')

def blue_quadrance_coordinates(x1,y1,x2,y2):
	return blue_quadrance_coords(x1,y1,x2,y2)
def red_quadrance_coordinates(x1,y1,x2,y2):
	return red_quadrance_coords(x1,y1,x2,y2)
def green_quadrance_coordinates(x1,y1,x2,y2):
	return green_quadrance_coords(x1,y1,x2,y2)

def blue_quadria(p1,p2,p3):
	return blue_quadrea(p1,p2,p3)
def red_quadria(p1,p2,p3):
	return red_quadrea(p1,p2,p3)
def green_quadria(p1,p2,p3):
	return green_quadrea(p1,p2,p3)

def Quadrea(x,y,z): return univ_quadrea(x,y,z)

def blue_circum_center( tri ):
	return blue_circumcenter( tri )
def red_circum_center( tri ):
	return red_circumcenter( tri )
def green_circum_center( tri ):
	return green_circumcenter( tri )


def blue_ninepoint_center( *args ): return blue_ninepointcenter(*args)
def red_ninepoint_center( *args ): return red_ninepointcenter(*args)
def green_ninepoint_center( *args ): return green_ninepointcenter(*args)
def nine_point_triangle( tri ): return ninepoint_triangle( tri )



