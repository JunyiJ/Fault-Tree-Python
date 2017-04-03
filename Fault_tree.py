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
import copy

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
	def __iter__(self):
		for k in self.kid:
			yield k,self.kid[k]

class FaultTree(object):
	def __init__(self):
		self.root=None
		self.size=0

	def Length(self):
		return self.size
		
	def DFS_search2(self,name):
		# Using non-recurrsion method, Return a list containing all node that has name as a kid
		result=[]
		if not self.root:
			return None
		result=[]
		waitlist=[self.root]
		while waitlist:
			subnode=waitlist.pop()
			if not subnode.is_leaf():
				for k,v in subnode:
					if k==name:
						result.append(subnode)
					else:
						if not v.is_leaf():
							waitlist.append(v)
		return result		

	def Add_node(self,new_node):
		if new_node.name=="Root":
			self.root=new_node
		else:
			to_node=self.DFS_search2(new_node.name)
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
		
	def Cal_FT(self,leaf_value):
		# Using non recursive method to calculate the value of root based on leaf_values
		value=copy.deepcopy(leaf_value)
		result=None
		if not self.root:
			return result
		DFS=[]
		DFS_waitlist=[self.root]
		while DFS_waitlist:
			node=DFS_waitlist.pop()
			DFS.append(node)
			if not node.is_leaf():
				for k,v in node:
					DFS_waitlist.append(v)
		while DFS:
			node=DFS.pop()
			if not node.is_leaf():
				method=node.gate
				if method.upper()=="AND":
					result=1
					for k,v in node:
						result*=value[k]
						if not result:
							break
				else:
					result=0
					for k,v in node:
						result+=value[k]
						if result:
							break
				value[node.name]=result
		return value["Root"]

	def Leaf(self):
		# Using non-recurrsion method to generate a list containing the leaf nodes' names
		if not self.root:
			return None
		result=[]
		waitlist=[self.root]
		while waitlist:
			subnode=waitlist.pop()
			if not subnode.is_leaf():
				for k,v in subnode:
					waitlist.append(v)
			else:
				result.append(subnode.name)
		#print set(result)
		return set(result)
				
	def MonteCarlo_mcs(self,n,k):
		""" 
		Using Monte Carlo algorith to find minimal cut set
		Run the code n times and print the first k cut set
		"""		
		#start_time=time.time()
		count_list=[]										#if result(root)=1, store the count in count_list
		cs_all={}											#All cut sets (as list) with count as their key
		leaf_seq=list(self.Leaf())							#The list that contains all leaf node in a certain order
		for i in range(n):
			leaf_value = {}
			count=0
			for j in leaf_seq:								#Generate random value for each leaf node and store them in leaf_value
				leaf_value[j]=choice([0,1])
				count += leaf_value[j]
			result = self.Cal_FT(leaf_value)	
			'''
			if result:										#If is a cut set, add to cs_all
				cutset=[]
				for L in leaf_seq:
					cutset.append(str(leaf_value[L]))
				cutset="".join(cutset)
				if cutset not in cs_all:
					cs_all[cutset]=count
		
		cs_all_sorted=sorted(zip(cs_all.values(),cs_all.keys())) #Order the cutset by its count
		for i in range(k):
			cutset=list(cs_all_sorted[i][1])
			result=[]
			for index in range(len(cutset)):
				if cutset[index] is "1":
					result.append(leaf_seq[index])
			print result
		#end_time=time.time()
		#print "Running time is", end_time-start_time
		'''
starttime=time.time()	
argv=sys.argv
filename=argv[1]
#print argv
n=int(argv[2])
k=int(argv[3])
			
FT_test=FaultTree()
FT_test.Build_xml(filename)
FT_test.MonteCarlo_mcs(n,k)
endtime=time.time()
timetxt="Script: Fault_tree. Running time for %s is %s seconds\n"%(filename,endtime-starttime)
with open("running_time.txt","a") as f:
		f.write(timetxt)
print timetxt
