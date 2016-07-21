from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree
import sys

# Given an input file, parse it into a xml file, named as the inputfilename_out.txt
# To test the script, type the following command:
# python .\parse.py 'input.txt'


def Parse2xml(infilename):
	# Given an input file, parse it into xml file
	list=Element('list')
	root=SubElement(list,'node')
	root.set('id','Root')
	root_gate=SubElement(root,'gate')
	root_gate.text='AND'
	nodes=[]
	nodes_child={}
	
	with open(infilename,'r') as f:
		for line in f.readlines():
			elements=line.strip("<\t />\n").split("=")
			if len(elements)>1:
				node_id=((elements[1].split(" "))[0]).strip('"\'')
				node_route=elements[3].strip('"').split(", ")
				#print node_id,node_route
				if node_id not in nodes:
					nodes.append(node_id)
					nodes_child[node_id]=[node_route]
				else:
					nodes_child[node_id].append(node_route)

	for node in nodes:
		n=SubElement(root,'dep')										#Add new child node under root
		n.text=node
		if len(nodes_child[node])==1:
			Add_Node(list,node,"OR",nodes_child[node][0])				#Add new node under list if no parellel path
		else:															#Add new node under list if exists parellel path
			new_pnode=SubElement(list,'node')
			new_pnode.set("id",node)
			g=SubElement(new_pnode,'gate')
			g.text="AND"
			for i in range(len(nodes_child[node])):
				count=i+1
				subnode_name="%s-path%d"%(node,count)
				subnode=SubElement(new_pnode,'dep')
				subnode.text=subnode_name
				Add_Node(list,subnode_name,"OR",nodes_child[node][i])
			
	outfilename=infilename[:(len(infilename)-4)]+"_out.txt"	
	with open(outfilename,"w") as f:
		ElementTree(list).write(f)

def Add_Node(parentnode,name,gate,child_node):
	#Create a new node by providing the following information:
	#parentnode, name of the new node,gate("AND","OR"),child_node list
	new_node=SubElement(parentnode,'node')
	new_node.set('id',name)
	g=SubElement(new_node,'gate')
	g.text=gate
	for c in child_node:
		child=SubElement(new_node,'dep')
		child.text=c
		
argv=sys.argv
infilename=argv[1]
Parse2xml(infilename)
	