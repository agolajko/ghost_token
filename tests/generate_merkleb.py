import sqlite3
from starkware.cairo.lang.vm.crypto import pedersen_hash
from starkware.starknet.public.abi import starknet_keccak, get_storage_var_address
from starkware.storage.names import generate_unique_key
import json


def generate_proof(block_num: int, contract_address: int, var_name: str, *args):
    con = sqlite3.connect("/home/ago/Downloads/goerli.sqlite")

    cur = con.cursor()
    print("hi run")
    print(f"cursor {cur}")
    # We prepare the Merkle branch
    merkleb_high = []
    merkleb_low = []

    # First get the address we want to find, this is the path we go down on.
    # Note: formatting: felts are 251 bit long. That should be 256/4=64 chars.Leftmost 5 bits are empty.
    b_address = str(bin(contract_address))[2:].rjust(251, "0")
    height = 0

    # Then find the correct block root:
    for row in cur.execute("SELECT quote(root) FROM starknet_blocks WHERE number IS "+str(block_num) + " ; "):
        # for row in cur.execute("SELECT root FROM starknet_blocks WHERE number IS "+str(block_num) + " ; "):
        next_hash = row[0][2:66]
        root_hash = next_hash
    print(f"root_hash from DB is {root_hash}")
    print("hi run 2")

    # Then go down the path of the global_trie

    for i in range(251):
        # if i % 50 == 0:
        print(f"global_trie path is {i}")

        for row in cur.execute("SELECT quote(data) FROM tree_global WHERE hash =CAST(X'"+next_hash+"' AS BLOB);"):
            # for row in cur.execute("SELECT data FROM tree_global WHERE hash =CAST(X'"+next_hash+"' AS BLOB);"):
            # we are using the fact that we only want the first row
            print(f"row is {row}")
            break
        if len(row[0]) == 131:
            # This means we are in a branch we include the opposite hash and location into the branch.We also increase height and path.
            # print (row[0][66:130])
            print(f"height is {height}")
            bit = b_address[height]
            op_bit = 1-int(bit)
            if int(bit) == 0:
                next_hash = row[0][2:66]
                other_hash = row[0][66:130]
            elif int(bit) == 1:
                other_hash = row[0][2:66]
                next_hash = row[0][66:130]
            else:
                assert 0 == 1

            height += 1

            # we put the other_hash's node into the branch
            for row in cur.execute("SELECT quote(data) FROM tree_global WHERE hash =CAST(X'"+other_hash+"' AS BLOB);"):
                # for row in cur.execute("SELECT data FROM tree_global WHERE hash =CAST(X'"+other_hash+"' AS BLOB);"):
                #    for row in cur.execute("SELECT quote(data) FROM tree_global WHERE quote(hash) LIKE '%" + other_hash+"%';"):
                print(f"row is {row}")
                break

            if len(row[0]) == 131:
                other_hash_path = 0
                other_hash_length = 0
            elif len(row[0]) == 133:
                # in this case the other_hash itself changes. In the others it does not.
                other_hash_length = int(row[0][130:132], 16)
                other_hash_path = int(row[0][66:130], 16)
                other_hash = row[0][2:66]
            else:
                other_hash_length = 0
                other_hash_path = 0
            # if other_hash == ():
                # in this case we are in a leaf, so nothing changes.
            merkleb_high.insert(0, [height, int(b_address[0: height-1]+str(op_bit), 2),
                                other_hash_length, other_hash_path,  int(str(other_hash), 16)])

        elif len(row[0]) == 133:
            # This means we are in an edge node, we have to increase height, but we don't change the merkle branch. We also check we are on the correct path.(we could return 0 instead of breaking)
            print(f"edge node len is {len(row[0])}")

            next_hash = row[0][2: 66]
            path_l = '0x' + row[0][130:132]
            assert int("0x"+row[0][66:130],
                       16) == int(b_address[height: height+int(path_l, 16)], 2)
            height += int(path_l, 16)

        else:
            # we are at the leaf. The leaf has no data, as the hash is the data itself.
            merkleb_high.insert(
                0, [height, int(b_address[0:height], 2), 0, 0, int(next_hash, 16)])
            break
    print("hi run 3")

    # We get the root of the contract
    for row in cur.execute("SELECT quote(root), quote(hash) FROM contract_states WHERE state_hash =CAST(X'"+next_hash+"' AS BLOB);"):
        # for row in cur.execute("SELECT  quote(root), quote(hash) FROM contract_states WHERE quote(state_hash) LIKE '%" + next_hash + "%';"):
        next_hash = row[0][2:66]
        storage_root = next_hash
        other_hash = row[1][2:66]

        break

    # we calculate the key
    # I think this part is correct, I just don't know the names of the storage variables. I will try again on goerli.

    key = get_storage_var_address(var_name, 1)
    b_key = str(bin(key))[2:].rjust(251, "0")
    height_cont = 0
    print("hi still run")

    # Then go down the path of the storage_trie
    for i in range(251):
        if i % 50 == 0:
            print(f"storage_trie path is {i}")
        for row in cur.execute("SELECT quote(data) FROM tree_contracts WHERE hash =CAST(X'"+next_hash+"' AS BLOB);"):
            # for row in cur.execute("SELECT data FROM tree_contracts WHERE hash =CAST(X'"+next_hash+"' AS BLOB);"):
            # for row in cur.execute("SELECT quote(data) FROM tree_contracts WHERE quote(hash) LIKE '%" + next_hash+"%';"):
            # we are using the fact that we only want the first row
            print(f"row is {row}")
            break
        if len(row[0]) == 131:
            # This means we are in a branch we include the opposite hash and location into the branch.We also increase height and path.
            bit = b_key[height_cont]
            op_bit = 1-int(bit)
            if int(bit) == 0:
                x = row[0][2:66]
                y = row[0][66:130]
            elif int(bit) == 1:
                y = row[0][2:66]
                x = row[0][66:130]
            else:
                assert 0 == 1

            height_cont += 1
 # we put the other_hash's node into the branch
            for row in cur.execute("SELECT quote(data) FROM tree_global WHERE hash =CAST(X'"+other_hash+"' AS BLOB);"):
                # for row in cur.execute("SELECT data FROM tree_global WHERE hash =CAST(X'"+other_hash+"' AS BLOB);"):
                #    for row in cur.execute("SELECT quote(data) FROM tree_global WHERE quote(hash) LIKE '%" + other_hash+"%';"):
                print(f"row is {row}")
                break

            if len(row[0]) == 131:
                other_hash_path = 0
                other_hash_length = 0
            elif len(row[0]) == 133:
                # in this case the other_hash itself changes. In the others it does not.
                other_hash_length = int(row[0][130:132], 16)
                other_hash_path = int(row[0][66:130], 16)
                other_hash = row[0][2:66]
            else:
                other_hash_length = 0
                other_hash_path = 0
            # if other_hash == ():
                # in this case we are in a leaf, so nothing changes.
            merkleb_low.insert(0, [height_cont, int(b_key[0: height_cont-1]+str(op_bit), 2),
                                   other_hash_length, other_hash_path,  int(str(other_hash), 16)])

        elif len(row[0]) == 133:
            # This means we are in an edge node, we have to increase height and traversedpath, but we don't change the merkle branch. We also check we are on the correct path.

            next_hash = row[0][2: 66]
            path_l = '0x' + row[0][130:132]

            # sanity check that we are on the correct path. (other option: if this breaks, return 0)
            assert int(
                "0x"+row[0][66:130], 16) == int(b_key[height_cont: height_cont+int(path_l, 16)], 2)
            height_cont += int(path_l, 16)
        else:

            merkleb_low.insert(
                0, [height_cont, int(b_key[0:height_cont], 2), 0, 0, int(next_hash, 16)])
            break

    con.close

    print(root_hash, storage_root,  merkleb_high, merkleb_low)
    return (root_hash, storage_root,  merkleb_high, merkleb_low)


def main():
    con = sqlite3.connect("/home/ago/Downloads/goerli.sqlite")

    cur = con.cursor()
    # Then find the latest block root:
    for row in cur.execute("SELECT number FROM starknet_blocks ORDER BY number DESC limit 1; "):
        # print("The root is:")
        # print(len(row[0]))
        block_number = row[0]
    con.close

    contract_address = int(
        "0x35572dec96ab362c35139675abc4f1c9d6b15ee29c98fbf3f0390a0f8500afa", 16)
    generate_proof(block_num=block_number,
                   contract_address=contract_address, var_name="l1GatewayAddress")


if __name__ == '__main__':
    main()
