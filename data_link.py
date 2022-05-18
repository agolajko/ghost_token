import sqlite3
from starkware.cairo.lang.vm.crypto import pedersen_hash
from starkware.starknet.public.abi import starknet_keccak, get_storage_var_address
from starkware.storage.names import generate_unique_key

con = sqlite3.connect("./mainnet.sqlite")

cur = con.cursor()


#We prepare the Merkle branch
merkleb=[]
merkleb_cont=[]

# First get the address we want to find, this is the path we go down on.
#Note: formatting: felts are 251 bit long. That should be 256/4=64 chars.Leftmost 5 bits are empty. 
address= 0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7
b_address= str(bin(address))[2:].rjust(251, "0")


print("The address we are looking at:")
print(len(b_address))
print( b_address)
#sanity check

height = 0
distance_from_last_branch=0

# Then find the latest block root:
for row in cur.execute("SELECT quote(root) FROM starknet_blocks ORDER BY number DESC limit 1; "):
	print("The root is:")
	print(len(row[0]))
	x=row[0][2:66]
	print(x)

# Then go down the path of the global_trie
for i in range(251):
	for row in cur.execute("SELECT quote(data) FROM tree_global WHERE quote(hash) LIKE '%"+ x+"%';"):
		#we are using the fact that we only want the first row
		break		
	print("Next node:")
	print(len(row[0]))
	#print(row[0][2:66])
	if len(row[0])==131: 
		#This means we are in a branch we include the opposite hash and location into the branch.We also increase height and path. 
		#print (row[0][66:130])
		bit = b_address[height]
		if int(bit)==0:
			x= row[0][2:66]
			y= row[0][66:130]
		elif int(bit)==1:
			y= row[0][2:66]
			x= row[0][66:130]
			breakpoint()
		else:
			print(bit)
			assert 0==1

		height+=1
		if distance_from_last_branch==0:
			short_path=0
		else:	
			short_path=int(b_address[height-distance_from_last_branch: height])
		merkleb.insert(0, [height, int(b_address[0: height], 2), distance_from_last_branch, short_path,  y])
		distance_from_last_branch=0

	elif len(row[0])== 133:
		#This means we are in an edge node, we have to increase height and traversedpath, but we don't change the merkle branch. We also check we are on the correct path. 
			
		x=row[0][2: 66]
		path ='0x'+ row[0][130:132]
		assert int("0x"+row[0][66:130], 16)==int(b_address[height: height+int(path, 16)], 2)
		print("assert success")
		height += int(path, 16)
		distance_from_last_branch+=int(path, 16)

	else:
		#we are at the leaf. The leaf has no data, as the hash is the data itself. 
		short_path=int(b_address[height-distance_from_last_branch: height])

		merkleb.insert(0, [height, int(b_address[0:height], 2), distance_from_last_branch, short_path, x])
		print(row[0])
		break
	print(x)	


print(merkleb)
#We get the root of the contract
print("moving to contract level")
for row in cur.execute("SELECT  quote(root), quote(hash) FROM contract_states WHERE quote(state_hash) LIKE '%"+x+"%';"):
	z=row[0][2:66]
	y=row[1][2:66]
	
	assert int("0x"+x, 16)==pedersen_hash(pedersen_hash(pedersen_hash(int("0x"+y, 16),int("0x"+ z, 16)), 0), 0)
	x=z 
	break

#we calculate the key
# I think this part is correct, I just don't know the names of the storage variables. I will try again on goerli. 
var_name = "implementation"

inputs=[]
key= get_storage_var_address(var_name)
print(key)
b_key = str(bin(key))[2:].rjust(251, "0")

height_cont=0

# Then go down the path of the storage_trie
for i in range(251):
	for row in cur.execute("SELECT quote(data) FROM tree_contracts WHERE quote(hash) LIKE '%"+ x+"%';"):
		#we are using the fact that we only want the first row
		break	
	print("Next node:")
	print(len(row[0]))
	#print(row[0][2:66])
	if len(row[0])==131: 
		#This means we are in a branch we include the opposite hash and location into the branch.We also increase height and path. 
		#print (row[0][66:130])
		bit = b_key[height_cont]
		if int(bit)==0:
			x= row[0][2:66]
			y= row[0][66:130]
		elif int(bit)==1:
			y= row[0][2:66]
			x= row[0][66:130]

		else:
			print(bit)
			assert 0==1

		height_cont+=1
		merkleb_cont.insert(0, [height_cont, b_key[0: height_cont], y])

	elif len(row[0])== 133:
		#This means we are in an edge node, we have to increase height and traversedpath, but we don't change the merkle branch. We also check we are on the correct path. 
			
		x=row[0][2: 66]
		path ='0x'+ row[0][130:132]
		#breakpoint()
		print(int(path, 16))
		print( int("0x"+row[0][66:130], 16))
		print(int(b_key[height_cont: height_cont+int(path, 16)], 2))

		assert int("0x"+row[0][66:130], 16)==int(b_key[height_cont: height_cont+int(path, 16)], 2)
		print("assert success")
		height_cont += int(path, 16)
	else:
		print(row[0])
		break
	print(x)	



con.close
