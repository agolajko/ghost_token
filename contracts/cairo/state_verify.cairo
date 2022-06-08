%lang starknet

#%builtins pedersen range_check bitwise

from starkware.cairo.common.cairo_builtins import BitwiseBuiltin, HashBuiltin
from starkware.cairo.common.bitwise import bitwise_and, bitwise_xor
from starkware.cairo.common.hash import hash2
from starkware.cairo.common.math_cmp import is_le
#from starkware.cairo.common.math import div
from starkware.cairo.common.alloc import alloc


from branch_verify import verify_branch, tree_node, verify_both_branches 

@storage_var
func variable() -> (res : felt):
end 

@storage_var
func state_root() -> (res : felt):
end 

@storage_var
func contract_hash() -> (res : felt):
end 

@storage_var
func contract_address() -> (res : felt):
end 

@storage_var
func variable_key() -> (res : felt):
end 


@view
func get{
    syscall_ptr : felt*,
    pedersen_ptr : HashBuiltin*,
    range_check_ptr,
}()-> (res : felt):
    let res : felt = variable.read()
    return (res)
end

@external
func initialise{
    syscall_ptr : felt*,
    pedersen_ptr : HashBuiltin*,
    range_check_ptr,
}(contract_hash_ : felt, contract_address_: felt):
    variable.write(10)
	contract_hash.write(contract_hash_)
	contract_address.write(contract_address_)
	variable_key.write(778741677097751136629359488410499500026881115738990894538495916875030189956)
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
func verify_increment{
    
	syscall_ptr : felt*,
    pedersen_ptr : HashBuiltin*,
    range_check_ptr,
	bitwise_ptr : BitwiseBuiltin*}(
	state_root_ : felt, 	
	leaf : tree_node,
	branch_low_len : felt,
	branch_low : tree_node*,
	root_low_hash : felt, 
	branch_high_len : felt,
	branch_high : tree_node*,
	root_high_hash : felt):
   	alloc_locals

	#we do the checks. These variables never change
	let (contract_address_ : felt) = contract_address.read()
	let (contract_hash_ : felt) = contract_hash.read()

	#the main branch check
	verify_both_branches(leaf, branch_low_len, branch_low,  root_low_hash, contract_address_, contract_hash_, branch_high_len, branch_high, root_high_hash)

	#the secondary checks
	let (variable_key_ : felt) = variable_key.read()
	assert leaf.position = variable_key_
	let (variable_ : felt) = variable.read()
	assert leaf.value = variable_
	
	assert state_root_ = root_high_hash	
		
	

	variable.write(variable_+1)
	return ()
end


