from starkware.cairo.lang.vm.crypto import pedersen_hash
from collections import namedtuple
# store a node value as a named tuple

Node = namedtuple("Node", ["height", "position", "length", "path", "value"])

# test_node = Node(0, 0, 0, 0, 1)


def hash_orientation(node_one: Node, node_two: Node):
    # takes two nodes as defined above as input
    # checks which one is two the left and which one is on the right
    # hashes them accordingly

    # get last bit of each node positiion to get parity
    node_one_position_parity = int(bin(node_one.position)[-1])
    node_two_position_parity = int(bin(node_two.position)[-1])

    # check the two parities are not the same
    assert node_one_position_parity != node_two_position_parity
    # assert height is the same for the two nodes
    assert node_one.height == node_two.height

    # hash order depending on parity

    if node_one_position_parity:
        # if node_one is in odd position
        return mp_hash_named_tuple(node_two, node_one)
    else:
        return mp_hash_named_tuple(node_one, node_two)


def mp_hash_named_tuple(left_tuple: Node, right_tuple: Node):
    # takes two named tuples as an input
    # performs the MP hash on them as specified here https://docs.starknet.io/docs/State/starknet-state/

    # if both tuples are all zero return (0,0,0)
    left_zeros = all(v == 0 for v in left_tuple[2:])
    right_zeros = all(v == 0 for v in right_tuple[2:])

    # get the height and position of the new hashed node

    new_height = left_tuple.height - 1
    new_position = int(right_tuple.position / 2)

    if left_zeros and right_zeros:
        return(Node(new_height, new_position, 0, 0, 0))
    elif not left_zeros and right_zeros:
        return(Node(new_height, new_position, left_tuple.length+1, left_tuple.path, left_tuple.value))
    elif left_zeros and not right_zeros:
        return(Node(new_height, new_position, right_tuple.length+1, right_tuple.path + 2**right_tuple.length, right_tuple.value))
    else:
        return(Node(new_height, new_position, 0, 0, pedersen_hash(mp_inner_named_tuple(left_tuple[2:]), mp_inner_named_tuple(right_tuple[2:]))))


def mp_inner_named_tuple(inner_tuple):
    if inner_tuple[0] == 0:
        return(inner_tuple[2])
    else:
        return(pedersen_hash(inner_tuple[2], inner_tuple[1])+inner_tuple[0])


def hash_branch_named_tuple(branch_list):
    # takes a list of nodes represented as named tuples

    # hash first two together and add their hash to new hashes list
    # hash third element of branch list with first element of new_hashes
    # hash fourth element of branch_list with second of new_hashes

    # how will the hashing differ depending on the structure of the branch we are hashing

    new_hashes = []

    # hash first two together

    first_hash = hash_orientation(branch_list[0], branch_list[1])

    new_hashes.append(first_hash)

    # loop over the two lists
    # start hashing the last element of the

    for branch_node in branch_list[2:]:
        # joint_str = str(str(new_hashes[-1]) + str(node)).encode("ascii")
        # node_hash = sha256(joint_str).hexdigest()

        # how to load nodes into below hashing function so they are consistant with left, right policy
        node_hash = hash_orientation(branch_node, new_hashes[-1])

        new_hashes.append(node_hash)

    return(new_hashes)

# test the above with a few branches from the Starknet example here https://docs.starknet.io/docs/State/starknet-state/

# test_branch_list = [Node(3, 7, 0, 0, 0), Node(
#     3, 6, 0, 0, 0), Node(2, 2, 1, 1, 1), Node(1, 0, 2, 2, 1)]

# test_branch_list2 = [Node(3, 4, 0, 0, 0), Node(
#     3, 5, 0, 0, 1), Node(2, 3, 0, 0, 0), Node(1, 0, 2, 2, 1)]

# hash_branch_named_tuple(test_branch_list2)