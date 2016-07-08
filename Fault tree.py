"""
This script build a real fault tree to store node information in it.
Each tree node contains node name, value(-1 as default),gate,kid(dictionary,using name as its key)
To test the script mannually, run the following function
FT_test=FaultTree()
FT_test.Build_xml('tree.txt')
FT_test.MonteCarlo_mcs(n,k)
"""
import xml.etree.ElementTree as ET
from random import choice
import time
import sys

class Node(object):
	def __init__(self,name):
		self.value=-1
		self.name=name
		self.gate=None
		self.kid={}
		self.size=0
	def num_kid(self):
		return self.size
	def is_leaf(self):
		# Return Trus if is leaf
		return self.size==0
	def add_kid(self,name):
		node=Node(name)
		self.kid[name]=node
		self.size+=1
	def def_gate(self,gate):
		self.gate=gate

class FaultTree(object):
	def __init__(self):
		self.root=None
		self.size=0

	def Length(self):
		return self.size

	def _search(self,cur_node,name):
		# BFS return the parent of "name"
		result=[]
		if not cur_node.is_leaf():
			if name in cur_node.kid:
				result.append(cur_node)
			else:
				for kid in cur_node.kid:
					result += self._search(cur_node.kid[kid],name)
		return result

	def BFS_search(self,name):
		# Return a list containing all node that has name as a kid
		if not self.root:
			return None
		return self._search(self.root,name)

	def Add_node(self,new_node):
		if new_node.name=="Root":
			self.root=new_node
		else:
			to_node=self.BFS_search(new_node.name)
			for n in to_node:
				n.kid[new_node.name]=new_node
		self.size += 1

	def Build_xml(self,filename):
		# Build a Fault Tree based on xml file
		tree=ET.parse(filename)
		root=tree.getroot()
		for n in root:
			name=n.attrib['id']
			gate=n[0].text
			New_Node=Node(name)
			New_Node.def_gate(gate)
			for kid in n[1:]:
				New_Node.add_kid(kid.text)
			#print New_Node.name,New_Node.gate
			self.Add_node(New_Node)

	def _print(self,node):
		print "(",node.name,node.gate,")"
		if not node.is_leaf():
			for kid in node.kid:
				self._print(node.kid[kid])

	def Print_FT(self):
	# Print the fault tree (preorder)
		if not self.root:
			print "blank tree"
		else:
			self._print(self.root)
		
	def _Cal_FT(self,node,leaf_value):
		# Using recurrsion to calculate the result at node given the leaf values stored in leaf_value
		if node.is_leaf():
			return leaf_value[node.name]
		method=node.gate
		if method=="AND":
			result=1
			for k in node.kid:
				result*=self._Cal_FT(node.kid[k],leaf_value)
				if not result:
					break
		else:
			result=0
			for k in node.kid:
				result+=self._Cal_FT(node.kid[k],leaf_value)
				if result:
					break
		return result
		
	def Cal_FT(self,leaf_value):
		# Calculate the result at root node given the values staored in leaf_value
		return self._Cal_FT(self.root,leaf_value)

	def _Leaf(self,node):
		result=[]
		if node.is_leaf():
			result = [node.name]
		else:
			for k in node.kid:
				result += self._Leaf(node.kid[k])
		return result
	
	def Leaf(self):
		# Generate a list containing the leaf nodes' names
		result=self._Leaf(self.root)
		return set(result)
				
	def MonteCarlo_mcs(self,n,k):
		""" 
		Using Monte Carlo algorith to find minimal cut set
		Run the code n times and print the first k cut set
		"""
		
		start_time=time.time()
		count_list=[]										#if result(root)=1, store the count in count_list
		cs_all={}											#All cut sets (as list) with count as their key
		leaf_seq=[]											#The list that contains all leaf node in a certain order
		leaf_seq=self.Leaf()
		for i in range(n):
			leaf_value = {}
			count=0
			for j in leaf_seq:								#Generate random value for each leaf node and store them in leaf
				leaf_value[j]=choice([0,1])
				count += leaf_value[j]
			result = self.Cal_FT(leaf_value)	
			if result:										#If is a cut set, add to cs_all
				cutset=[]
				for L in leaf_seq:
					#print "leaf", L
					cutset.append(leaf_value[L])
				if count not in count_list:
					count_list.append(count)
					cs_all[count]=[cutset]
				else:
					if cutset not in cs_all[count]:
						cs_all[count].append(cutset)
			
					
		count_list.sort()
		i=0
		while i<k:											# Print out the first k cut-set
			for j in count_list:
				if i>=k:
					break
				for m in cs_all[j]:
					print m
					i+=1
					if i>=k:
						break
		end_time=time.time()
		print "Running time is", end_time-start_time
			
		
argv=sys.argv
filename=argv[1]
print argv
n=int(argv[2])
k=int(argv[3])
			
FT_test=FaultTree()
FT_test.Build_xml(filename)
FT_test.MonteCarlo_mcs(n,k)
