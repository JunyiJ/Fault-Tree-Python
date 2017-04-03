# Using dictionary(dict) to realize the fault tree function
# For example dict['Root']=['AND','E1','E2']
# All leaf nodes' names are stored in a list called leaves, for example ['A1','A2']

# To mannually test the code
# Build_FT('tree.txt')  				tree.txt is the xml file
# MCS(n,k)
# It will print the k cut set after running n times
					
import xml.etree.ElementTree as ET
from random import choice
import sys
import copy
import time

dict = {}								# The dictionary to store all tree node information
dict_all={}
leaves = []								# The list to store the names of leaf node
nonleaves = []
def Build_FT(filename):
	"""Store tree nodes in a dictionary dict and store leaf node names in list leaves"""
	tree = ET.parse(filename)
	root = tree.getroot()
	global dict
	global leaves
	global nonleaves
	for n in root:
		name=n.attrib['id']
		#nonleaves.append(name)
		
		if name not in dict:
			dict[name]=[]
		for i in range(len(n)):
			if i==0:
				if n[i].text.upper()=="AND":
					dict[name].append(1)
				else:
					dict[name].append(0)
			else:
				dict[name].append(n[i].text)				
				if n[i].text not in dict:	# Also create entry for kid nodes						
					dict[n[i].text]=[]
					
	"""Test whether a node is leaf node, if yes add it to list leaves"""
	for i in dict:
		dict_all[i]=-1
		if not dict[i]:
			leaves.append(i)
def MCS(n,k):
	"""Using Monte Carlo algorith to find minimal cut set
	Run the code n times and print the first k cut set
	"""
	global dict_all
	dict_val=copy.deepcopy(dict_all)
	#start_time = time.time()
	final = {}					    # Store all result with the count as key. For example final[1]=[[1,0,0],[0,1,1]]
	seq = []						# Store the count with no duplication
	for i in range(n):
		leaf={}						# leaf is the dictionary to store the random value of each leaf
		#count=0
		for i in leaves:
			leaf[i] = choice([0,1])
			dict_val[i]=leaf[i]
			#count += leaf[i]
		result = Cal_FT(dict_val)	
		'''
		if result:
			cutset = []
			for i in leaves:
				cutset.append(str(leaf[i]))
			cutset="".join(cutset)
			if cutset not in final:
				final[cutset]=count
	final_sorted=sorted(zip(final.values(),final.keys())) 				#Order the cutset by its count
	for i in range(k):													#Print the first k result
		cutset=list(final_sorted[i][1])
		result=[]
		for index in range(len(cutset)):
			if cutset[index] is "1":
				result.append(leaves[index])
		print result
	#end_time=time.time()
	#print "Running time is", end_time-start_time
	'''

def DFS():
	"""
	Using depth first search to find out all non-leaf nodes
	Cal_FT2 will use this node list to calculate the root value without recurrion
	"""

	global nonleaves
	dict_cp=copy.deepcopy(dict)
	nonleaves=["Root"]
	waitlist=["Root"]
	while waitlist:
		peek=waitlist[-1]
		if len(dict_cp[peek])>=2:
			sub_node=dict_cp[peek].pop()
			if dict[sub_node]:
				nonleaves.append(sub_node)
				waitlist.append(sub_node)
		else:
			waitlist.pop()	
	
def Cal_FT(dict_val):
	
	global dict
	
	"""Using non recursion method to calculate the value in Root node"""
	
	nonleaves_cp=copy.deepcopy(nonleaves)
	

	
	while nonleaves_cp:
		cur_node=nonleaves_cp.pop()
		if dict_val[cur_node]==-1:
			result = dict[cur_node][0]
			if dict[cur_node][0]:				
				for i in dict[cur_node][1:]:
					result*=dict_val[i]
					if not result:
						break
			else:
				for i in dict[cur_node][1:]:
					result+=dict_val[i]
					if result:
						break
			dict_val[cur_node]=result		

	return dict_val["Root"]			
			
				

starttime=time.time()				
argv=sys.argv
filename=argv[1]
n=int(argv[2])
k=int(argv[3])		
Build_FT(filename)
DFS()
MCS(n,k)
endtime=time.time()
timetxt="Script: Fault_tree_dict. Running time for %s is %s seconds\n"%(filename,endtime-starttime)
with open("running_time.txt","a") as f:
		f.write(timetxt)
print(timetxt)
