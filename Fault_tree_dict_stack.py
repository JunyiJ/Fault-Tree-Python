# Using dictionary(dict) to realize the fault tree function
# For example dict['Root']=['AND','E1','E2']
# All leaf nodes' names are stored in a list called leaves, for example ['A1','A2']

# To mannually test the code
# Build_FT('tree.txt')  				tree.txt is the xml file
# MCS(n,k)
# It will print the k cut set after running n times
					
import xml.etree.ElementTree as ET
from random import choice
import time
import sys
import copy

dict = {}								# The dictionary to store all tree node information
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
				if n[i].text=="AND":
					dict[name].append(1)
				else:
					dict[name].append(0)
			else:
				dict[name].append(n[i].text)
				if i>=1:
					if n[i].text not in dict:	# Also create entry for kid node
						
						dict[n[i].text]=[]
					
	"""Test whether a node is leaf node, if yes add it to list leaves"""
	for i in dict:
		if not dict[i]:
			leaves.append(i)

def MCS(n,k):
	"""Using Monte Carlo algorith to find minimal cut set
	Run the code n times and print the first k cut set
	"""
	start_time = time.time()
	
	final = {}					    # Store all result with the count as key. For example final[1]=[[1,0,0],[0,1,1]]
	seq = []						# Store the count with no duplication
	for i in range(n):
		
		leaf={}						# leaf is the dictionary to store the random value of each leaf
		count=0
		for i in leaves:
			leaf[i] = choice([0,1])
			count += leaf[i]
		#result = Cal_FT('Root',leaf)
		result = Cal_FT2(leaf)
		if result:
			'''Rearrange the node value in a list (cutset) based on the order node in leaves
			to avoid duplicates. For example {"A1":0,"A2":1,"A3":0} and {"A3":0,"A1":0,"A2":1}
			should be treated as the same result.
			'''
			cutset = []
			for i in leaves:
				cutset.append(leaf[i])
			
			if count in final:
				if cutset not in final[count]:
					final[count].append(cutset)
			else:
				seq.append(count)
				final[count]=[cutset]
	
	seq.sort()
	"""Print the first k cut set based on their count"""
	#print "order of leaves", leaves
	i=0
	while i<k:
		for j in seq:
			if i>=k:
				break
			for m in final[j]:
				#print m
				r=[]
				for index in range(len(m)):
					if m[index]:
						r.append(leaves[index])
				print r
				i+=1
				if i>=k:
					break
	end_time=time.time()
	print "Running time is", end_time-start_time
		
def Cal_FT(node,leaf):
	"""Using recurssion to calculate the value of the fault tree with assigned value in leaf"""
	if node in leaf:
		return leaf[node]
	method=dict[node][0]
	if method==1:
		result=1
		for subnode in dict[node][1:]:
			result*=Cal_FT(subnode,leaf)
			if not result:
				break
	else:
		result=0
		for subnode in dict[node][1:]:
			result+= Cal_FT(subnode,leaf)
			if result>=1:
				break
	return result

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
			if sub_node not in leaves:
				nonleaves.append(sub_node)
				waitlist.append(sub_node)
		else:
			waitlist.pop()
		
	
	
def Cal_FT2(leaf):
	nonleaves_cp=copy.deepcopy(nonleaves)
	dict_cp=copy.deepcopy(dict)
	for i in leaf:
		dict_cp[i]=leaf[i]
	while nonleaves_cp:
		cur_node=nonleaves_cp.pop()
		if isinstance(dict_cp[cur_node],list):
			if dict_cp[cur_node][0]:
				result = dict_cp[cur_node][0]
				for i in dict_cp[cur_node][1:]:
					result*=dict_cp[i]
					if not result:
						break
			else:
				result = dict_cp[cur_node][0]
				for i in dict_cp[cur_node][1:]:
					result+=dict_cp[i]
					if result:
						break
			dict_cp[cur_node]=result
	return dict_cp["Root"]			
			
				

				
argv=sys.argv
filename=argv[1]
n=int(argv[2])
k=int(argv[3])		
Build_FT(filename)
DFS()
MCS(n,k)