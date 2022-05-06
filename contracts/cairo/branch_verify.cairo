%builtins output pedersen

from starkware.cairo.common.cairo_builtins import BitwiseBuiltin, HashBuiltin
from starkware.cairo.common.bitwise import bitwise_and, bitwise_xor
from starkware.cairo.common.hash import hash2
from starkware.cairo.common.math_cmp import is_le
from starkware.cairo.common.math import div
from starkware.cairo.common.alloc import alloc

const MAX_HEIGHT = 

#we store the path in felts, and as we are going to do division, in multiple felts. lenght gives us the maximal bit that (might) not be 0. path1<path2<...
struct tree_node:
	#we are locating nodes in the tree, it takes both height and position. Note for node at height h, position is < 2**(MAX_HEIGHT-H)
	member height : felt
	member position : felt
	#here we are looking at the values=(l, p, v) at the node.
	member length : felt
	member path : felt
	member value : felt
end

#we hash a single node, zero or not. 
func hash_node{range_check_ptr, pedersen_ptr : HashBuiltin*}(
	node : tree_node ) -> (res : felt):
	alloc_locals

	if node.length == 0:
		return (node.value)	
	end

	let (value) = (hash2{hash_ptr=pedersen_ptr}(node.value, node.path) + node.length)
	
	return (value)
end

#we join two nodes, and calculate their hash. We check that they are neighbours, and assume that they are non zero. 
func join_nodes{range_check_ptr, pedersen_ptr : HashBuiltin*}(
	node1 : tree_node,
	node2 : tree_node) -> (res_node : tree_node):
	alloc_locals
	
	assert node1.height=node2.height
	let (dif) = (node2.position-node1.position)
	assert dif=1

	let (new_pos) = (node1.position) / 2
	let (new_height) = node1.height + 1
	
	let (first_hash) = hash_node(node1)
	let (second_hash) = hash_node(node2)
	let (new_val) = (hash2{hash_ptr=pedersen_ptr}(first_hash, second_hash)

	return (tree_node(new_height, new_pos, 0, 0, new_val))
end
	
#we join a node with a number of zero nodes. We know the direction from the position of the node.
func empty_join_rec{range_check_ptr, pedersen_ptr : HashBuiltin*}(
	leaf : tree_node,
	iter : felt) -> ():
	alloc_locals
	
	if (iter==0):
		return (leaf)
	end

	let (res) = bitwise_and(leaf.position, 1)
	let (new_pos) = (leaf.position - res) /2
	
	let (new_leaf : tree_node) = tree_node(leaf.height+1, new_pos, leaf.length+1, leaf.path + res*pow(2, leaf.length), leaf.value )
	
	let (final_leaf : tree_node) = empty_join_rec(new_leaf, iter-1)
	return (final_leaf)
end

#we verify a branch. We do the outer checks here, and the recursive part in verify_branch_rec. 

func verify_branch{range_check_ptr, pedersen_ptr : HashBuiltin*}(
	leaf : tree_node,
	branch : tree_node*,
	branch_len : felt,
	root_hash : felt):
	
	assert leaf.height=0
	let (final_node : tree_node) = hash_branch_rec(leaf, branch, branch_len, branch_iter)
	let (res) = hash_node(final_node)
	assert (res==root_hash)
end

func hash_branch_rec{range_check_ptr, pedersen_ptr : HashBuiltin*}(
	leaf : tree_node,
	branch : tree_node*,
	branch_len : felt,
	branch_iter : felt) -> (res_node : tree_node):
	
	alloc_locals

	
	let (join_node : tree_node) = branch[branch_iter]
	let (zero_node_num : felt) = join_node.height-leaf.height
	let (zerod_leaf : tree_node) = empty_join_rec(leaf, zero_node_num) 
	
	let (new_leaf : tree_node) = hash_branch_rec(zerod_leaf, branch, branch_len, branch_iter+1)
end


