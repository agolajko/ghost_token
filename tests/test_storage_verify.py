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
    branch_proofs_contract: StarknetContract


async def setup():
    starknet = await Starknet.empty()
    branch_proofs_contract = await starknet.deploy(source="contracts/cairo/branch_verify.cairo", cairo_path=["contracts"])
    return TestsDeps(
        starknet=starknet,
        branch_proofs_contract=branch_proofs_contract
    )


@pytest.fixture(scope='module')
async def factory():
    return await setup()


# 

@pytest.mark.asyncio
async def test_increase(factory):
    starknet, branch_proofs_contract = factory
	
	

