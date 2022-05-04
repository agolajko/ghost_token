# create new type for representing felts
# should only alow unsigned 251 bit numbers
# should be able to perform the usual set of arithmetic operations on it


# hash the felt together
# make a list from the felt (check that lenght is a power of 2)

# rules for hashing
# create a tuple from each number N of form (0,0,N), these are the leaves
# since we know the number of leaves we also know the height of the tree
# start hashing pairwise to get a new list of elements that form a new row of the tree
# continue until done
#
#

from hashlib import sha256
from math import log2
leaves = [12, 34, 33, 55]

n_leaves = len(leaves)
tree_height = int(log2(n_leaves))

# loop over all the leaves and generate a hash pairwise

# split list into pairs of two
split_leaves = [leaves[i:i + 2] for i in range(0, len(leaves), 2)]

all_nodes = []

for leaf in split_leaves:
    # encode as ascii

    bleaf = str(leaf).encode("ascii")
    # hash the string
    node_hash = sha256(bleaf).hexdigest()
    all_nodes.append(node_hash)


# function that takes a list of hashed leaves to be hashed as input
# returns a longer list with the hash tree elements layer by layer

# list for storing the full tree hash
tree_list = []


def make_tree(leaf_list, tree_list):

    # check if leaf_list is size power 2

    len_leaf = len(leaf_list)

    # bitwise check if the lenght of the list is a power of two
    len_2_power = (len_leaf & (len_leaf-1) == 0) and len_leaf != 0

    assert len_2_power

    # list for storing output of current hashing
    next_nodes_list = []

    # hash them pairwise, by appending one after the other

    paired_list = [leaf_list[i:i + 2] for i in range(0, len(leaf_list), 2)]
    print(paired_list)
    # append paired hash to tree list

    for leaf in paired_list:
        # encode as ascii

        bleaf = str(leaf).encode("ascii")
        # hash the string
        node_hash = sha256(bleaf).hexdigest()
        next_nodes_list.append(node_hash)
        print(leaf)
        print(node_hash)

    # append next_nodes_list to tree_list
    tree_list.append(next_nodes_list)

    # call the function recursively on next_nodes_list
    if len(next_nodes_list) != 1:
        make_tree(next_nodes_list, tree_list)


# flat_list = [item for sublist in t for item in sublist]

test_lists = [[1, 2, 3, 4, 5, 6, 7, 8]]

for tester in test_lists:
    new_list = []
    make_tree(tester, new_list)

    # flatten list

    # flat_list = [item for sublist in t for item in new_list]
    flat_list = [item for item in new_list]

    expected_len_pows = [2**k for k in range(log2(len(tester)))]
    expected_len = sum(expected_len_pows)
    assert len(flat_list) == expected_len
