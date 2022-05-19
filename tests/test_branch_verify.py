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
    return await Starknet.empty()


@pytest.fixture
async def branch_contract(starknet_ins: Starknet) -> StarknetContract:
    # return await starknet_ins.deploy(source="/home/ago/projects/ghost_token/contracts/cairo/branch_verify.cairo", cairo_path=["contracts"])
    return await starknet_ins.deploy(source="../contracts/cairo/branch_verify.cairo", cairo_path=["contracts"])

# test whether the cairo contract internal functions work as intended


@pytest.mark.asyncio
async def test_core(starknet_ins: Starknet, branch_contract: StarknetContract):
    print("Testing core branch_verify.cairo functions")

    # Invoke test
    # print("does this run?")
    leaf1 = (3, 4, 0, 0, 1)
    leaf2 = (3, 5, 0, 0, 1)
    leaf3 = (3, 6, 2, 0, 1)
    branch1 = [(1, 0, 2, 2, 1)]
    total_len1 = 4
    root_hash1 = 1428519069806529925910806899344787140252006517057140074734361523088172087989

    # first we want to test the more low level hashes and functions

    res_hash0 = await branch_contract.decide_higher(leaf1, leaf2).call()
    res_hash1 = await branch_contract.decide_higher(leaf2, leaf3).call()

    print(res_hash0.result)
    print(res_hash1.result)

    # test if join_nodes works
    res_hash1 = await branch_contract.hash_node(node=leaf3).call()
    print(res_hash1.result)

    # # test if join_nodes works
    res_hash1 = await branch_contract.join_nodes(node1=leaf1, node2=leaf2).call()
    print(res_hash1.result)

    # test if empty_join_rec works
    res_hash1 = await branch_contract.empty_join_rec(leaf=leaf1, iter=2).call()
    print(res_hash1.result)

    # test if hashing works
    res_hash1 = await branch_contract.hash_branch_rec(leaf=leaf2, branch=branch1, branch_iter=0).call()
    print(res_hash1.result)

    return()


@pytest.mark.asyncio
async def test_branch(starknet_ins: Starknet, branch_contract: StarknetContract):
    # takes as input the list of nodes to hash (where the first node is the leaf)
    # hashes the list with the python code
    # tranforms list so can be fed to cairo
    # compares output of cairo and python
    print("Testing toy example branch")

    Node = namedtuple("Node", ["height", "position",
                      "length", "path", "value"])

    test_branch_list2 = [Node(3, 5, 0, 0, 1), Node(
        3, 4, 0, 0, 0), Node(2, 3, 0, 0, 0), Node(1, 0, 2, 2, 1)]

    python_root_hash = hash_branch_named_tuple(test_branch_list2)[-1].value

    leaf = test_branch_list2[0]
    total_len = len(test_branch_list2)

    # remove and count zero nodes
    # take the first node as a leaf node
    non_zero_branch = []
    for one_node in test_branch_list2[1:]:
        if sum(one_node[2:]) != 0:
            non_zero_branch.append(one_node)

    res_hash = await branch_contract.verify_branch(leaf, non_zero_branch, total_len-1, python_root_hash).call()
    assert res_hash.result.res == python_root_hash
    return()


@pytest.mark.asyncio
async def test_import_branch(starknet_ins: Starknet, branch_contract: StarknetContract):

    print("Testing imported branch")
    real_branch = [[251, 2087021424722619777119509474943472645767659996348769578120564519014510906823, 0, 0, 925923027743716088412580218759933356705924200491378477898922997267440127909], [19, 302391, 232, 804599282193126534729012206945677246823683991466037958900426319638155, 2845907075484037364340839605230938759614031545690464816023248203590004103890], [15, 18898, 1, 1, 2068999822834717155277431254277993556996921809430267328221339871988239691498], [14, 9448, 0, 0, 2626297209765236621112568054025023411157280018298857612198388327438765672720], [13, 4725, 0, 0, 114042384147459021247589628548989524378804968261581027693897228674841869060], [12, 2363, 0, 0, 363544692136358849593922891137150500414254016895051513683597360015525958644], [11, 1180, 0, 0, 1455217617578759071219323265713615622485361384186997712159947788454446006627], [
        10, 591, 0, 0, 2206032403902298161642980152874228407049484295795844662530069446718827489044], [9, 294, 0, 0, 2987505503067271205655009149904786789113847611235725839287179543737548254375], [8, 146, 0, 0, 888666846273684553742385526466199882452300571760042010132161258023056564811], [7, 72, 0, 0, 1628637071339699414739222192994669561688627612078636828121896912385471552952], [6, 37, 0, 0, 1345256175674707089191791658560608135523660778760243573736085934114218009965], [5, 19, 0, 0, 3398541956851574724602720438280143714473047022802377852322768518123275525521], [4, 8, 0, 0, 1622095540731265172145181973183423146174436422526103308238267871709620380432], [3, 5, 0, 0, 456614750810695172736454163323963431217958450263303308677873234045662684514], [2, 3, 0, 0, 312345566541817044255288812116449046262495767671064483232498601625367264889], [1, 0, 0, 0, 908782179392994200239506909464745281819857492057798832247104747873438968770]]
    real_branch_int = [tuple(i) for i in real_branch]
    real_leaf = real_branch_int[0]
    real_branch_rest = real_branch_int[1:]
    total_len = 251
    root_hash = 2100660188095084288620515079086904656261336581214533446535447348142332014717

    res_hash = await branch_contract.verify_branch(real_leaf, real_branch_rest, total_len, root_hash).call()
    return()
