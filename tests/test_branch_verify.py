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


@pytest.fixture
async def starknet_ins() -> Starknet:
    print("Hello")
    return await Starknet.empty()


@pytest.fixture
async def branch_contract(starknet_ins: Starknet) -> StarknetContract:
    # return await starknet_ins.deploy(source="/home/ago/projects/ghost_token/contracts/cairo/branch_verify.cairo", cairo_path=["contracts"])
    return await starknet_ins.deploy(source="/home/proj/ghost_token/contracts/cairo/branch_verify.cairo")


@pytest.mark.asyncio
async def test_branch(starknet_ins: Starknet, branch_contract: StarknetContract):

    # Invoke test
    print("does this run?")
    leaf1 = (3, 5, 0, 0, 1)
    branch1 = ((1, 0, 2, 2, 1))
    total_len1 = 4
    root_hash1 = 1428519069806529925910806899344787140252006517057140074734361523088172087989
    res_hash = await branch_contract.verify_branch(leaf1, branch1, total_len1, root_hash1).call()
    print("does this run?")
    print(res_hash.result.res)
    # assert res.res == 3

    return()
