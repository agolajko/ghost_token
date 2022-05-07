# how does the cairo testing look?
# Use code from Fossil


# make contract deployable
# deploy contract
# call contract on the test input
# call python code on test input
# verify contract gives same output as the python output



import pytest
import asyncio
from typing import NamedTuple

from starkware.starknet.testing.contract import StarknetContract
from starkware.starknet.testing.starknet import Starknet


class TestsDeps(NamedTuple):
    starknet: Starknet
    trie_proofs_contract: StarknetContract

@pytest.fixture(scope='module')
def event_loop():
    return asyncio.new_event_loop()

async def setup():
    starknet = await Starknet.empty()
    branch_proofs_contract = await starknet.deploy(source="/home/projects/ghost_token/contracts/cairo/branch_verify.cairo", cairo_path=["contracts"])
    return TestsDeps(
        starknet=starknet,
        trie_proofs_contract=branch_proofs_contract
    )


@pytest.fixture(scope='module')
async def factory():
    return await setup()


# 

@pytest.mark.asyncio
async def test_count_shared_prefix_len(factory):
    starknet, branch_proofs_contract = factory

    # setup inputs
    # proof = trie_proofs[1]['accountProof']
    # element_rlp = Data.from_hex(proof[len(proof) - 1])

    # path = Data.from_hex(Web3.keccak(hexstr=trie_proofs[1]['address']).hex())
    # path_offset = 7

    # # Get expected values
    # node_path_items = to_list(element_rlp.to_ints())
    # node_path_items_extracted = extract_list_values(element_rlp.to_ints(), node_path_items)
    # node_path_nibbles = merkle_patricia_input_decode(node_path_items_extracted[0])
    # expected_shared_prefix = path_offset + count_shared_prefix_len(path_offset, path.to_nibbles(), node_path_nibbles)

    # Invoke test
    print("does this run?")
    count_shared_prefix_len_call = await branch_proofs_contract.verify_branch().call()
    print("does this run?")

    assert count_shared_prefix_len_call.result.res ==3 



    return()
