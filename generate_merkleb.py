import sqlite3
from starkware.cairo.lang.vm.crypto import pedersen_hash
from starkware.starknet.public.abi import starknet_keccak, get_storage_var_address
from starkware.storage.names import generate_unique_key
import json

def generate_proof(block_num : int, contract_address: int, var_name : str, *args):
		con = sqlite3.connect("./mainnet.sqlite")

		cur = con.cursor()


		#We prepare the Merkle branch
		merkleb_high=[]
		merkleb_low=[]

		# First get the address we want to find, this is the path we go down on.
		#Note: formatting: felts are 251 bit long. That should be 256/4=64 chars.Leftmost 5 bits are empty. 
		b_address= str(bin(contract_address))[2:].rjust(251, "0")
		height = 0

		# Then find the correct block root:
		for row in cur.execute("SELECT quote(root) FROM starknet_blocks WHERE number IS "+str(block_num) +" ; "):
			next_hash=row[0][2:66]
			root_hash=next_hash

		# Then go down the path of the global_trie
		for i in range(251):
			for row in cur.execute("SELECT quote(data) FROM tree_global WHERE quote(hash) LIKE '%"+ next_hash +"%';"):
				#we are using the fact that we only want the first row
				break		
			if len(row[0])==131: 
				#This means we are in a branch we include the opposite hash and location into the branch.We also increase height and path. 
				#print (row[0][66:130])
				bit = b_address[height]
				op_bit = 1-int(bit)
				if int(bit)==0:
					next_hash= row[0][2:66]
					other_hash= row[0][66:130]
				elif int(bit)==1:
					other_hash= row[0][2:66]
					next_hash= row[0][66:130]
				else:
					assert 0==1

				height+=1
			
				#we put the other_hash's node into the branch
				for row in cur.execute("SELECT quote(data) FROM tree_global WHERE quote(hash) LIKE '%"+ other_hash+"%';"):
					break
						
				if len(row[0])==131:
					other_hash_path= 0
					other_hash_length= 0
				elif len(row[0])==133:
					other_hash_length = int(row[0][130:132], 16)
					other_hash_path = int(row[0][66:130], 16) 
					other_hash=row[0][2:66]
					#in this case the other_hash itself changes. In the others it does not.
				else:
					other_hash_length=0
					other_hash_path=0
				if other_hash == ():

				merkleb_high.insert(0, [height, int(b_address[0: height-1]+str(op_bit), 2),other_hash_length , other_hash_path ,  int(str(other_hash), 16)])

			elif len(row[0])== 133:
				#This means we are in an edge node, we have to increase height, but we don't change the merkle branch. We also check we are on the correct path.(we could return 0 instead of breaking) 
					
				next_hash=row[0][2: 66]
				path_l ='0x'+ row[0][130:132]
				assert int("0x"+row[0][66:130], 16)==int(b_address[height: height+int(path_l, 16)], 2)
				height += int(path_l, 16)

			else:
				#we are at the leaf. The leaf has no data, as the hash is the data itself. 
				merkleb_high.insert(0, [height, int(b_address[0:height], 2), 0, 0, int(next_hash, 16)])
				break


		#We get the root of the contract
		for row in cur.execute("SELECT  quote(root), quote(hash) FROM contract_states WHERE quote(state_hash) LIKE '%" + next_hash +"%';"):
			next_hash = row[0][2:66]
			other_hash = row[1][2:66]
			
			break

		#we calculate the key
		# I think this part is correct, I just don't know the names of the storage variables. I will try again on goerli. 

		key= get_storage_var_address(var_name, args)
		b_key = str(bin(key))[2:].rjust(251, "0")
		height_cont=0

		# Then go down the path of the storage_trie
		for i in range(251):
			for row in cur.execute("SELECT quote(data) FROM tree_contracts WHERE quote(hash) LIKE '%"+ next_hash+"%';"):
				#we are using the fact that we only want the first row
				break	
			if len(row[0])==131: 
				#This means we are in a branch we include the opposite hash and location into the branch.We also increase height and path. 
				bit = b_key[height_cont]
				if int(bit)==0:
					x= row[0][2:66]
					y= row[0][66:130]
				elif int(bit)==1:
					y= row[0][2:66]
					x= row[0][66:130]
				else:
					assert 0==1

				height_cont+=1
				merkleb_low.insert(0, [height_cont, b_key[0: height_cont], y])

			elif len(row[0])== 133:
				#This means we are in an edge node, we have to increase height and traversedpath, but we don't change the merkle branch. We also check we are on the correct path. 
					
				x=row[0][2: 66]
				path_l ='0x'+ row[0][130:132]

				#sanity check that we are on the correct path. (other option: if this breaks, return 0)
				assert int("0x"+row[0][66:130], 16)==int(b_key[height_cont: height_cont+int(path_l, 16)], 2)
				height_cont += int(path_l, 16)
			else:
				print(row[0])
				break

		con.close

		return (root_hash, merkleb_high, merkleb_low)
