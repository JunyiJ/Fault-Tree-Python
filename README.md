# Fault Tree (Python)

## Introduction

**Fault Tree** is a special tree structure used to test the weakness in a network (for example, web network or computer network). All inner nodes contains a logic gate ("AND" gate or "OR" gate) and the value of any inner node is determined by its logic gate and its children's values (either 1 or 0). 

A **cut set** of the fault tree is a set of leaf values causing the root value equal to 1. A **Minimal cut set** (MCS) is a cut set with as few 1s as possible in it. If we define broken part of a network as value 1, then minimal cut sets can be used to understand the structural vulnerability of a system. 

Finding a minimal cut set for a fault tree is a NP hard problem. However, we can use Monte Carlo algorithm to find a solution or close solution for the minimal cut set (MCS) problem for a fault tree.

## Usage
In this code, I used two different structure to represent the fault tree structure and realize its functions:
* A tree structure with node   (Fault tree)
To test the script, in command line type python "Fault tree.py" "tree.txt" 100000 5

* A dictionary storing nodes with their name as the key (Fault_tree_dict)
To test the script, in command line type python "Fault_tree_dict.py" "tree.txt" 100000 5
There is also a test case (text.txt) containing a fault tree represented in an xml format.


## Credit
Thanks Dr.Ennan Zhai for comments.

