# how does the cairo testing look?
# Use code from Fossil


# make contract deployable
# deploy contract
# call contract on the test input
# call python code on test input
# verify contract gives same output as the python output


import pytest
import asyncio
# from typing import NamedTuple

from starkware.starknet.testing.contract import StarknetContract
from starkware.starknet.testing.starknet import Starknet
from python_hash_branch import hash_branch_named_tuple
from collections import namedtuple


@pytest.fixture
async def starknet_ins() -> Starknet:
    print("Hello")
    return await Starknet.empty()


@pytest.fixture
async def branch_contract(starknet_ins: Starknet) -> StarknetContract:
    # return await starknet_ins.deploy(source="/home/ago/projects/ghost_token/contracts/cairo/branch_verify.cairo", cairo_path=["contracts"])
    return await starknet_ins.deploy(source="../contracts/cairo/branch_verify.cairo", cairo_path=["contracts"])


# @pytest.mark.asyncio
# async def test_branch(starknet_ins: Starknet, branch_contract: StarknetContract):

#     # Invoke test
#     print("does this run?")
#     leaf1 = (3, 4, 0, 0, 1)
#     leaf2 = (3, 5, 0, 0, 1)
#     leaf3 = (3, 6, 2, 0, 1)
#     branch1 = [(1, 0, 2, 2, 1)]
#     total_len1 = 4
#     root_hash1 = 1428519069806529925910806899344787140252006517057140074734361523088172087989

#     # first we want to test the more low level hashes and functions

#     # res_hash0 = await branch_contract.decide_higher(leaf1, leaf2).call()
#     # res_hash1 = await branch_contract.decide_higher(leaf2, leaf3).call()

#     # print(res_hash0.result)
#     # print(res_hash1.result)

#     # test if join_nodes works
#     # res_hash1 = await branch_contract.hash_node(node=leaf3).call()
#     # # print(res_hash1.result)

#     # # test if join_nodes works
#     # res_hash1 = await branch_contract.join_nodes(node1=leaf1, node2=leaf2).call()
#     # print(res_hash1.result)

#     # test if empty_join_rec works
#     # res_hash1 = await branch_contract.empty_join_rec(leaf=leaf1, iter=2).call()
#     # print(res_hash1.result)

#     # test if hashing works
#     # res_hash1 = await branch_contract.hash_branch_rec(leaf=leaf2, branch=branch1, branch_iter=0).call()
#     # print(res_hash1.result)

#     res_hash = await branch_contract.verify_branch(leaf2, branch1, total_len1, root_hash1).call()
#     # print("does this run?")
#     # print(res_hash.result.res)
#     assert res_hash.result.res == root_hash1
#     return()


# @pytest.mark.asyncio
# async def test_branch(starknet_ins: Starknet, branch_contract: StarknetContract):

#     # Invoke test
#     print("does this run?")
#     # leaf2 = (3, 5, 0, 0, 1)
#     # branch1 = [(1, 0, 2, 2, 1)]
#     # total_len1 = 4
#     # root_hash1 = 1428519069806529925910806899344787140252006517057140074734361523088172087989
#     Node = namedtuple("Node", ["height", "position",
#                       "length", "path", "value"])

#     test_branch_list2 = [Node(3, 4, 0, 0, 0), Node(
#         3, 5, 0, 0, 1), Node(2, 3, 0, 0, 0), Node(1, 0, 2, 2, 1)]
#     # test_branch_list2 = [Node(3, 5, 0, 0, 1), Node( 3, 4, 0, 0, 0), Node(2, 3, 0, 0, 0), Node(1, 0, 2, 2, 1)]


#     python_root_hash = hash_branch_named_tuple(test_branch_list2)[-1].value

#     leaf = test_branch_list2[0]
#     total_len = len(test_branch_list2)

#     # remove and count zero nodes

#     non_zero_branch = []
#     for one_node in test_branch_list2:
#         if sum(one_node[2:]) != 0:
#             non_zero_branch.append(one_node)

#     print("non_zero_branch")
#     print(non_zero_branch)
#     print("total_len")
#     print(total_len)
#     print("leaf")
#     print(leaf)
#     print("python_root_hash")
#     print(python_root_hash)

#     # takes as input the list of nodes to hash (where the first node is the leaf)
#     # hashes the list with the python code
#     # tranforms list so can be fed to cairo
#     # compares output of cairo and python

#     res_hash = await branch_contract.verify_branch(leaf, non_zero_branch, total_len, python_root_hash).call()
#     # print("does this run?")
#     # print(res_hash.result.res)
#     assert res_hash.res == python_root_hash
#     return()


@pytest.mark.asyncio
async def test_branch(starknet_ins: Starknet, branch_contract: StarknetContract):

    # Invoke test
    print("does this run?")
    # leaf2 = (3, 5, 0, 0, 1)
    # branch1 = [(1, 0, 2, 2, 1)]
    # total_len1 = 4
    # root_hash1 = 1428519069806529925910806899344787140252006517057140074734361523088172087989

    # test_branch_list2 = [Node(3, 5, 0, 0, 1), Node( 3, 4, 0, 0, 0), Node(2, 3, 0, 0, 0), Node(1, 0, 2, 2, 1)]

    real_branch = [[251, 2087021424722619777119509474943472645767659996348769578120564519014510906823, 232, 101011100001101010011100100011011110100100011101001100101100111010010111101001111111100110010000100011001000100110111011101011010111001011011110111110001110100000110110001010101100010101110000010111110011110000000000100110111000111, '07AC195D7FAABDF3850B5E1A3DA6638A089C48358E35E845AAF0B929E404A658'], [19, 302390, 3, 110, '05DE1618F3168D1FB23939402A5C76DABC860209123B5550DB649E75E7C75022'], [15, 18899, 0, 0, '04EB420B27BA6E9BA401C9361325A5CF076CBC0CCA131B5E9C1F09F2301927F4'], [14, 9449, 0, 0, '05CE6E79A3D36383917EC2DCC9642B660323461B075FA1AA9B877DD9BB024910'], [13, 4724, 0, 0, '00408BB3208F66AD24235BFD3F1520A73B61ECEB21408124C74D1F1D67D27B04'], [12, 2362, 0, 0, '04452277C586D4B47FC85D903D311EB66F37C5C4792F3FC8C13D4521464C0073'], [
        11, 1181, 0, 0, '0349AE533EFDAD3CFA77CA6DA89BA94433831B999DD766C9E3AAFD396D3E4337'], [10, 590, 0, 0, '04E091F19C987A3D126E4E45AEA3EB65802F93C2FA8E68D49363C305814F6714'], [9, 295, 0, 0, '06D43325F12FFE11649AACB48F9DB4A9D4B311FE5481C091FB5D00B77E89FB6C'], [8, 147, 0, 0, '06589426562999F91DEDC0E4FF88ED130DE1D38A08AFA47050D5C36A5ABA7FBB'], [7, 73, 0, 0, '04E73B45C73DE014C705705DCE19E5F5B44A532407A6E3E722FCEAFD4E941297'], [6, 36, 0, 0, '0622643ABA807D4529126F5BE4A0454619830656337E26670E59F27657220C47'], [5, 18, 0, 0, '031F49CEA53CE98896D2A53F88A5F25D4BB91D7E9599560CF6677E4C473C57F9'], [4, 9, 0, 0, '01FAC8F046B07F218726FCB49E24C3C24A311B0423C66E4CFD6255674810998A'], [3, 4, 0, 0, '034B7B8D69067CADFB49C76BB8EAF667A67B07DB5E31B0BF5AC76F97CE259042'], [2, 2, 0, 0, '02DC00D7A73927E0CA4590E4ADB89D8CDF14964B2715735C476AFFDC11007EAD'], [1, 1, 0, 0, '000BA33DFAA6F87BE0911EE67C4BF56F74826833035C2596A39391F90D7C511E']]

    real_branch_tuple = [tuple(i) for i in real_branch]
    real_branch_int = [tuple((i[0], i[1], i[2], int(
        str(i[3]), 2), int(i[4], 16))) for i in real_branch]
    print("real_branch_int")
    print(real_branch_int[:10])
    real_leaf = real_branch_int[0]
    real_branch_rest = real_branch_int[1:]
    total_len = 251
    root_hash = int(
        "0577A755E6869DDE6B474567A1953C2CF1CAE4BD5956E33AD357C156BD38EEC4", 16)

    res_hash = await branch_contract.verify_branch(real_leaf, real_branch_rest, total_len, root_hash).call()
