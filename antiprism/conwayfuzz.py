# generate random input for the 'conway' polyhedron generator from
# the 'antiprism' collection of polyhedron programs

seeds ='TOCIDPAY'

operators = 'abcdegjkmoprst'

interesting = { 
'blobball':'btD','flowerball':'bgbD','ovalishball':'ebmC','brickerball':'bpdO',
'paths':'tadbsP6','capsule':'atY6','nonsymmegg':'taotY6','bigsoccer':'cgsjC',
'dart':'cY7','snowhands':'bgksY5','speckles':'cgsY10','niceball':'ccccT',
'pillow':'kkkkkP13','spots':'tpmcI','interlock':'egbsD','soccerblue':'tpksI',
'squaredance':'dkseA9','snowfire':'pbstA10','danger':'jkjkjI','mushroom':'skskI',
'mostlyhexball':'dkdkdkdkdkD', 'tileball':'tstI', 'roads':'bactT', 
'roads2':'bactsT', 'flower':'tsbacT', 'splat':'bstcaT', 'eurodress':'abstcT',
'flowerdrumsong':'absY15'
}
from random import randint
ops=''
for i in range(0,randint(1,4)):
#for i in range(0,randint(1,3)):
	ops+=operators[randint(0,len(operators)-1)]

seed=seeds[randint(0,len(seeds)-1)]
if seed[-1] in 'PAY': seed += str(randint(3,10))
cmd = 'conway -f m '+ops+seed + ' | antiview -t no_triangulation'
print cmd
import os
os.popen( cmd )

