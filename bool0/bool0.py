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

import uuid

def debug(x):
	print(x)

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
	debugTreenodes(tree.rootnode)
	debug(' numnodes:'+str(findnumnodes(tree.rootnode)))
	debug(' numleaves:'+str(findnumleaves(tree.rootnode)))
	debug(' maxdepth:'+str(findmaxdepth(tree.rootnode)))
	debug(' name:')

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

def debugTreenodes(node):
	if node.left: debugTreenodes(node.left)
	if node.right: debugTreenodes(node.right)
	debugTreenode(node)

class Treenode:
	left, right, up, data = None, None, None, None
	def __init__(self):
		self.id = uuid.uuid4()
class Tree:
	rootnode = None
	def __init__(self,rootnode):
		self.rootnode = rootnode
	name = ''

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
	if node.left:
		左 += findmaxdepth(node.left)
	if node.right:
		右 += findmaxdepth(node.right)
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
	for token in tokens:
		debugToken( token )
		newnode = token_to_node( token )
		if token.toktype == 'operator':
			if currentnode:
				currentnode.up = newnode
				newnode.left = currentnode
			currentnode = newnode
		elif token.toktype == 'number':
			if currentnode==None: currentnode = newnode
			elif currentnode.left==None: currentnode.left = newnode
			elif currentnode.right==None: currentnode.right = newnode
			else: print('unknown'+token2str(token))
		debug('current')
		debugTreenode(currentnode)
		debug('new')
		debugTreenode(newnode)
	return Tree(currentnode)

if __name__=='__main__':
	expression = '0 | 0 | 1'
	debug('input '+expression)
	tokens = expression_to_tokens( expression )
	tree = tokens_to_tree( tokens )
	debug('--- tree built')
	debugTree(tree)
