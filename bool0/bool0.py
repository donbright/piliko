# Boolean geometry in 0 dimensions

# stage 0
# binary operators
#
# and
# 0 & 0 => 0
# 0 & 1 => 0
# 1 & 0 => 0
# 1 & 1 => 1
#
# or
# 0 | 0 => 0
# 0 | 1 => 1
# 1 | 0 => 1
# 1 | 1 => 1
#
# xor
# 0 ^ 0 => 0
# 0 ^ 1 => 1
# 1 ^ 0 => 1
# 1 ^ 1 => 0
#
#
# language expressions are made from binary operators
# examples
#
# 1 ^ 1 | 0 => 1
#
# 1 | 0 | 1 => ?
# 1 & 0 | 1 => ?
# 1 | 0 & 1 => ?
# 1 & 0 & 1 => ?
#
# precedence
#
# left first
# 0 | 0 ^ 1 => 1
# 0 ^ 0 | 1 => 1
# 0 | 1 | 1 => 1
# 0 ^ 1 ^ 1 => 0
#
# right first
# 0 | 0 ^ 1 => 1
# 0 ^ 0 | 1 => 1
# 0 | 1 | 1 => 1
# 0 ^ 1 ^ 1 => 0

import uuid, sys, string, html

debugger=False

def debug(x):
	if debugger: print(x)

def debugToken(t):
	debug(token2str(t))

def token2str(t):
	s='token'
	s+=' data:'+t.data
	s+=' type:'+t.toktype
	s+=' origin:'+str(t.origin)
	return s

def debugTree(tree):
	debug('tree')
	debugTreenodes(tree.root)
	debug(' root:'+str(tree.root.id))
	debug(' numnodes:'+str(findnumnodes(tree.root)))
	debug(' numleaves:'+str(findnumleaves(tree.root)))
	debug(' maxdepth:'+str(findmaxdepth(tree.root)))
	debug(' name:'+str(tree.name))

def debugTreenode(node):
	debug(' treenode')
	debug('  id:'+str(node.id))
	debug('  data:'+token2str(node.data))
	ltext,rtext,utext = 'None','None','None'
	if node.left: ltext = str(node.left.id)
	if node.right: rtext = str(node.right.id)
	if node.up: utext = str(node.up.id)
	debug('  up:'+utext)
	debug('  left:'+ltext)
	debug('  right:'+rtext)

def svgTree(tree):
	maxdepth = findmaxdepth(tree.root)
	s='<?xml version="1.0" encoding="utf-8" standalone="no"?>\n'
	s+='<svg width="1024" height="1024" xmlns="http://www.w3.org/2000/svg"  xmlns:xlink="http://www.w3.org/1999/xlink">\n'
	s+='<title>bool0 tree</title>\n'
	s+='<rect x="{0}" y="{1}" width="{2}" height="{3}" fill="none" stroke="black"/>\n'.format(1,1,1023,1023)
	s+=svgTreenode(tree.root,512,10,0,maxdepth)+'\n'
	s+='</svg>'
	return s

def svgTreenode(node,x,y,depth,maxdepth):
	nwidth,nheight=1024/(2**(depth)),40
	boxw = 1024 / 2**maxdepth
	#label = '{0.data},{0.toktype},{0.origin}'.format(node.data)
	label = '{0}'.format(node.data.data)
	label = html.escape(label)
	s='<!-- {0} {1} {2} -->\n'.format(depth,nwidth,2**0)
	s+='<circle cx="{0}" cy="{1}" r="{2}" stroke="black" fill="none"'.format(x,y+boxw/2,boxw*3/4)
	s+=' style="fill:none;stroke:rgb(0,0,0)" />\n'
	s+='<text x="{0}" y="{1}">{2}</text>\n'.format(x-5,y+22,label)
	if node.left:
		s += '<line x1="{0}" y1="{1}" x2="{2}" y2="{3}" style="stroke:black;"/>\n'.format(x,y+nheight,x-nwidth/4,y+55)
		s += svgTreenode(node.left,x-nwidth/4,y+boxw*2,depth+1,maxdepth)
	if node.right:
		s += '<line x1="{0}" y1="{1}" x2="{2}" y2="{3}" style="stroke:black;"/>\n'.format(x,y+nheight,x+nwidth/4,y+55)
		s += svgTreenode(node.right,x+nwidth/4,y+boxw*2,depth+1,maxdepth)
	return s
	#debug('  id:'+str(node.id))
	#debug('  data:'+token2str(node.data))
	#ltext,rtext,utext = 'None','None','None'
	#if node.up: utext = str(node.up.id)
	#debug('  up:'+utext)
	#debug('  left:'+ltext)
	#debug('  right:'+rtext)

def debugTreenodes(node):
	if node.left: debugTreenodes(node.left)
	if node.right: debugTreenodes(node.right)
	debugTreenode(node)

class Treenode:
	left, right, up, data = None, None, None, None
	def __init__(self):
		self.id = uuid.uuid4()
class Tree:
	root = None
	name = None
	nodetable = {}
	def __init__(self,root):
		self.root = root
		self.name = uuid.uuid4()

class Token:
	data = ''
	toktype = ''
	origin = -1
	def __init__(self,data,toktype,origin):
		self.data = data
		self.toktype = toktype
		self.origin = origin

def findnumnodes(node):
	总=0
	if node.left: 总 += findnumnodes(node.left)
	if node.right: 总 += findnumnodes(node.right)
	return 总+1

def findnumleaves(node):
	总=0
	if node.left: 总 += findnumleaves(node.left)
	if node.right: 总 += findnumleaves(node.right)
	if node.left==node.right==None: 总+=1
	return 总

def findmaxdepth(node):
	右=左=1
	if node.left: 左 += findmaxdepth(node.left)
	if node.right: 右 += findmaxdepth(node.right)
	if node.left==node.right==None: return 1
	return max(右,左)

def findtoktype(data):
	if data in '012346789': return 'number'
	elif data in ' ': return 'whitespace'
	elif data in '|^&': return 'operator'
	else: return 'unknown'

def expression_to_tokens( expression ):
	tokens = []
	charcount = 0
	for char in expression:
		debug('tokenizing char \''+char+'\'')
		tokdata = char
		toktype = findtoktype(tokdata)
		tokens += [Token(tokdata,toktype,charcount)]
		charcount += 1
	return tokens

def token_to_node( token ):
	点 = Treenode()
	点.up = None
	点.data = token
	点.right = None
	点.left = None
	return 点

def tokens_to_tree( tokens ):
	currentnode = None
	leftmost = None
	for token in tokens:
		debugToken( token )
		newnode = token_to_node( token )
		if token.toktype == 'operator':
			if currentnode:
				currentnode.up = newnode
				newnode.left = currentnode
			else:
				leftmost = newnode
			currentnode = newnode
	inserter = leftmost
	for token in tokens:
		newnode = token_to_node( token )
		if token.toktype == 'number':
			done = False
			while not done:
				if not inserter.left:
					inserter.left = newnode
					done = True
				elif not inserter.right:
					inserter.right = newnode
					done = True
				else:
					inserter = inserter.up
	return Tree(currentnode)

def runtest(s):
	return [s,eval(s)]

def expression_to_tree(s):
	tokens = expression_to_tokens( s )
	tree = tokens_to_tree( tokens )
	return tree

def test1():
	expression = '0 | 0 | 1'
	tokens = expression_to_tokens( expression )
	tree = tokens_to_tree( tokens )
	tests = '''
len(tokens)==9
findnumnodes(tree.root)==5
findnumleaves(tree.root)==3
findmaxdepth(tree.root)==3
'''
	for line in tests.split('\n'):
		if line and not eval(line): print('test fail',line)

def test2():
	tree = expression_to_tree( '0 | 0 | 1 & 2 | 3' )
	tests='''
findnumnodes(tree.root)==9
findnumleaves(tree.root)==5
findmaxdepth(tree.root)==5
'''
	for line in tests.split('\n'):
		if line and not eval(line): print('test fail',line)

if __name__=='__main__':
	if '--debug' in str(sys.argv): debugger=True
	test1()
	test2()
	expression = '0 | 0 | 1 & 2 | 3'
	debug('input '+expression)
	tokens = expression_to_tokens( expression )
	tree = tokens_to_tree( tokens )
	debug('--- tree built')
	debugTree(tree)
	if '--svg' in str(sys.argv): print(svgTree(tree))
