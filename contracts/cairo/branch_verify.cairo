%lang starknet

%builtins pedersen range_check bitwise

from starkware.cairo.common.cairo_builtins import BitwiseBuiltin, HashBuiltin
from starkware.cairo.common.bitwise import bitwise_and, bitwise_xor
from starkware.cairo.common.hash import hash2
from starkware.cairo.common.math_cmp import is_le
from starkware.cairo.common.pow import pow
# from starkware.cairo.common.math import div
from starkware.cairo.common.alloc import alloc


#we store the path in felts, and as we are going to do division, in multiple felts. lenght gives us the maximal bit that (might) not be 0. path1<path2<...
struct tree_node:
	#we are locating nodes in the tree, it takes both height and position.  
	member height : felt
	member position : felt
	#here we are looking at the values=(l, p, v) at the node.
	member length : felt
	member path : felt
	member value : felt
end

#we hash a single node, zero or not. 
@external
func hash_node{range_check_ptr, pedersen_ptr : HashBuiltin*}(
	node : tree_node ) -> (res : felt):
	alloc_locals

	if node.length == 0:
		return (node.value)	
	end

	let (local hash_value) = hash2{hash_ptr=pedersen_ptr}(node.value, node.path)
	# %{print(ids.hash_value)%}
	let node_value= node.length
	let sum_value = hash_value  + node_value
	
	return (sum_value)
end

# we join two nodes, and calculate their hash. We check that they are neighbours, and assume neither of them are zero.
@external
func join_nodes{range_check_ptr, pedersen_ptr : HashBuiltin*}(
	node1 : tree_node,
	node2 : tree_node) -> (res_node : tree_node):
	alloc_locals
	
	assert node1.height=node2.height
	let node2_pos = node2.position
	let node1_pos = node1.position
	let dif = node2_pos-node1_pos
	assert dif=1

	let new_pos = node1.position / 2
	let new_height = node1.height - 1
	
	let (first_hash) = hash_node(node1)
	let (second_hash) = hash_node(node2)
	let (new_val) = hash2{hash_ptr=pedersen_ptr}(first_hash, second_hash)

	%{print("************************************************************")%}
	%{print(f"new joined node height: {ids.new_height} ")%}
	%{print(f"new joined node pos: {ids.new_pos} ")%}
	%{print(f"new joined node val: {ids.new_val} ")%}

	return (tree_node(new_height, new_pos, 0, 0, new_val))
end
	
#we join a node with a number of zero nodes. We know the direction from the position of the node.
@external
func empty_join_rec{range_check_ptr, pedersen_ptr : HashBuiltin*, bitwise_ptr : BitwiseBuiltin*}(
	leaf : tree_node,
	iter : felt) -> (final_leaf : tree_node):
	alloc_locals
	
	if iter==0:
		return (leaf)
	end

	#  check if the leaf is the first leaf in the row
	let (res: felt) = bitwise_and(leaf.position, 1)
	let new_pos = (leaf.position - res) /2
	let leaf_path = leaf.path
	let leaf_len= leaf.length
	let (pow_leaf_len: felt) = pow(2,leaf.length)
	# %{print(f"height of node {ids.leaf.height}")%}
	# %{print(f"position of node {ids.leaf.position}")%}
	# %{print(ids.iter)%}
	# %{print(ids.iter)%}
	# %{print(ids.leaf_len)%}
	# %{print(ids.leaf_path)%}
	# %{print("pow_leaf_len")%}
	# %{print(ids.pow_leaf_len)%}
	let new_path = leaf_path + res*pow_leaf_len
	
	let new_leaf = tree_node(leaf.height-1, new_pos, leaf.length+1,new_path , leaf.value )
	
	let (final_leaf : tree_node) = empty_join_rec(new_leaf, iter-1)

	return (final_leaf)
end

#we verify a branch. We do the outer checks here, and the recursive part in verify_branch_rec. 

@external
func verify_branch{range_check_ptr, pedersen_ptr : HashBuiltin*, bitwise_ptr : BitwiseBuiltin*}(
	leaf : tree_node,
	branch_len : felt,
	branch : tree_node*,
	total_len : felt,
	root_hash : felt)-> (res:felt):
 	alloc_locals
	
	%{print("start")%}
	
	assert leaf.height=total_len
	let (local final_node : tree_node) = hash_branch_rec(leaf,branch_len, branch, 0)
	
	%{print(ids.final_node.height)%}	
	%{print(ids.final_node.position)%}	
	%{print(ids.final_node.length)%}	
	%{print(ids.final_node.path)%}	
	%{print(ids.final_node.value)%}	
	%{print(ids.total_len - ids.final_node.height)%}	
	
	let (zeroed_node : tree_node) = empty_join_rec(final_node, final_node.height)
	
	%{print(ids.zeroed_node)%}	
	
	# let (res) = hash_node(final_node)
	let (res) = hash_node(zeroed_node)
	# %{print(ids.res)%}
	assert res=root_hash
	return (res)
	# return (3)
end

@external
func hash_branch_rec{range_check_ptr, pedersen_ptr : HashBuiltin*, bitwise_ptr : BitwiseBuiltin*}(
	leaf : tree_node,
	branch_len : felt,
	branch : tree_node*,
	branch_iter : felt) -> (res_node : tree_node):
	
	alloc_locals
	
	# %{print("branch_iter")%}
	# %{print(ids.branch_iter)%}
	# %{print("branch_len")%}
	# %{print(ids.branch_len)%}
	
	if branch_iter==branch_len:
		return (leaf)
	end	 
	local join_node : tree_node = branch[branch_iter]
	# subtract the height of the current node 
	let zero_node_num : felt = (leaf.height-join_node.height)
	let (zeroed_leaf : tree_node) = empty_join_rec(leaf, zero_node_num) 

	# %{print(f" leaf height {ids.leaf.height}")%}
	# %{print(f" leaf pos {ids.leaf.position}")%}
	# %{print(f" join_node height {ids.join_node.height}")%}
	# %{print(f" join_node pos {ids.join_node.position}")%}
	# %{print("zero_node_num")%}
	# %{print(ids.zero_node_num)%}
	# %{print("positions")%}
	# %{print(ids.zeroed_leaf)%}
	# %{print(ids.zeroed_leaf.height)%}
	# %{print(ids.zeroed_leaf.position)%}
	# %{print(ids.join_node.height)%}
	# %{print(ids.join_node.position)%}

	let (l_leaf : tree_node, r_leaf : tree_node) = decide_higher(zeroed_leaf, join_node)
	let (join_leaf : tree_node)= join_nodes(l_leaf, r_leaf)
	# %{print(ids.join_leaf)%}
	
	let (new_leaf : tree_node) = hash_branch_rec(join_leaf, branch_len, branch, branch_iter+1)
	return (new_leaf)
end


@external
func decide_higher{range_check_ptr, pedersen_ptr : HashBuiltin*, bitwise_ptr : BitwiseBuiltin*}(
	node1 : tree_node,
	node2 : tree_node) -> (l_node : tree_node, r_node : tree_node):
	
	alloc_locals
	# %{print("decide_higher")%}	
	# %{print(ids.node1.position)%}	
	# %{print(ids.node2.position)%}	
	if node1.position-node2.position==1:
		return (node2, node1)
	end

	if node1.position-node2.position==-1:
		return (node1, node2)
	end
	assert 0=1
	return (node1, node2)
end
