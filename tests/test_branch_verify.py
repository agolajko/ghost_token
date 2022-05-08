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


@pytest.fixture
async def starknet_ins() -> Starknet:
	print("Hello")
	return await Starknet.empty()

@pytest.fixture
async def branch_contract(starknet_ins : Starknet) -> StarknetContract:
    return await starknet_ins.deploy(source="../contracts/cairo/branch_verify.cairo", cairo_path=["contracts"])


@pytest.mark.asyncio
async def test_branch(starknet_ins: Starknet, branch_contract : StarknetContract):

    # Invoke test
    print("does this run?")
    res = await branch_contract.verify_branch().call()
    print("does this run?")

    assert res.res == 3 


    return()
