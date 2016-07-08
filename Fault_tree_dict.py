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

dict = {}								# The dictionary to store all tree node information
leaves = []								# The list to store the names of leaf node

def Build_FT(filename):
	"""Store tree nodes in a dictionary dict and store leaf node names in list leaves"""
	tree = ET.parse(filename)
	root = tree.getroot()
	global dict
	global leaves
	for n in root:
		name=n.attrib['id']
		if name not in dict:
			dict[name]=[]
		for i in range(len(n)):
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
		result = Cal_FT('Root',leaf)
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
	i=0
	while i<k:
		for j in seq:
			if i>=k:
				break
			for m in final[j]:
				print m
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
	if method=='AND':
		result=1
		for subnode in dict[node][1:]:
			result*=Cal_FT(subnode,leaf)
			if not result:
				break
	elif method=='OR':
		result=0
		for subnode in dict[node][1:]:
			result+= Cal_FT(subnode,leaf)
			if result>=1:
				break
	return result
				
argv=sys.argv
filename=argv[1]
#print argv
n=int(argv[2])
k=int(argv[3])		
Build_FT(filename)
MCS(n,k)
