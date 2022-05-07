%builtins output pedersen

from starkware.cairo.common.cairo_builtins import BitwiseBuiltin, HashBuiltin
from starkware.cairo.common.bitwise import bitwise_and, bitwise_xor
from starkware.cairo.common.hash import hash2
from starkware.cairo.common.math_cmp import is_le
from starkware.cairo.common.math import div
from starkware.cairo.common.alloc import alloc


from branch_verify import verify_branch

@storage_var
func variable() -> (res : felt):
end 

@storage_var
func state_root() -> (res : felt):
end 

@storage_var
func contract_root() -> (res : felt):
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
end	

@external
func verify_higher{
    syscall_ptr : felt*,
    pedersen_ptr : HashBuiltin*,
    range_check_ptr}(
	leaf : tree_node, 
	branch : tree_node*, 
	branch_len : felt_node,
	total_len : felt,
	root_hash : felt):
   	alloc_locals
	
	verify_branch(leaf, branch, branch_len, total_len, root_hash)
	
	#here we will check compared to the state root when we can read it. 
	let state_root_ = state_root.read()	
	assert (state_root_ = root_hash)
	
	contract_root.write(res = leaf.value)

    return ()
end

@external
func verify_lower{
    syscall_ptr : felt*,
    pedersen_ptr : HashBuiltin*,
    range_check_ptr}(
	leaf : tree_node, 
	branch : tree_node*, 
	branch_len : felt_node,
	total_len : felt,
	root_hash : felt):
   	alloc_locals
	
	verify_branch(leaf, branch, branch_len, total_len, root_hash)
	
	let inter_hash1= hash2{hash_ptr=pedersen_ptr}(contract_hash.read(), root_hash.read())
	let inter_hash2= hash2{hash_ptr=pedersen_ptr}(inter_hash1, 0)
	let final_hash= hash2{hash_ptr=pedersen_ptr}(inter_hash2, 0)
	
	assert (final_hash = contract_root.read() ) 
	let current_var = variable.read()
	assert (leaf.value = current_var)
	
	variable.write(current_var+1)
    return ()
end
