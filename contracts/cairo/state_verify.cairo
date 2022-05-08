%lang starknet

#%builtins pedersen range_check bitwise

from starkware.cairo.common.cairo_builtins import BitwiseBuiltin, HashBuiltin
from starkware.cairo.common.bitwise import bitwise_and, bitwise_xor
from starkware.cairo.common.hash import hash2
from starkware.cairo.common.math_cmp import is_le
#from starkware.cairo.common.math import div
from starkware.cairo.common.alloc import alloc


from branch_verify import verify_branch, tree_node

@storage_var
func variable() -> (res : felt):
end 

@storage_var
func state_root() -> (res : felt):
end 

@storage_var
func storage_root() -> (res : felt):
end 

@storage_var
func contract_hash() -> (res : felt):
end 



@external
func initialise{
    syscall_ptr : felt*,
    pedersen_ptr : HashBuiltin*,
    range_check_ptr,
}(contract_hash_ : felt):
    variable.write(10)
	contract_hash.write(contract_hash_)
    return ()
end

@external
func set_state_root{
    syscall_ptr : felt*,
    pedersen_ptr : HashBuiltin*,
    range_check_ptr}(
	state_root_ : felt):
   	
	alloc_locals
	state_root.write(state_root_)
	return ()
end	

@external
func verify_higher{
    syscall_ptr : felt*,
    pedersen_ptr : HashBuiltin*,
    range_check_ptr,
	bitwise_ptr : BitwiseBuiltin*}(
	leaf : tree_node, 
	branch_len : felt,
	branch : tree_node*, 
	total_len : felt,
	root_hash : felt):
   	alloc_locals
	
	verify_branch(leaf,  branch_len, branch,total_len, root_hash)
	
	#here we will check compared to the state root when we can read it. 
	let state_root_ver:felt = state_root.read()
	assert state_root_ver = root_hash
	
	storage_root.write( leaf.value)

    return ()
end

@external
func verify_lower{
    syscall_ptr : felt*,
    pedersen_ptr : HashBuiltin*,
    range_check_ptr,
	bitwise_ptr : BitwiseBuiltin*}(
	leaf : tree_node, 
	branch_len : felt,
	branch : tree_node*, 
	total_len : felt,
	root_hash : felt):
   	alloc_locals
	
	verify_branch(leaf,  branch_len, branch,total_len, root_hash)
	let contract_hash_ : felt = contract_hash.read()
	let (local storage_root_ : felt) = storage_root.read()
	let inter_hash1 : felt = hash2{hash_ptr=pedersen_ptr}(contract_hash_, storage_root_)
	let inter_hash2 : felt = hash2{hash_ptr=pedersen_ptr}(inter_hash1, 0)
	let final_hash : felt = hash2{hash_ptr=pedersen_ptr}(inter_hash2, 0)
	
	
	assert final_hash = storage_root_  
	let current_var : felt = variable.read()
	assert leaf.value = current_var
	
	variable.write(current_var+1)
    return ()
end
