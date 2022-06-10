
# from tkinter import W
import pytest
import asyncio
# from typing import NamedTuple

from starkware.starknet.testing.contract import StarknetContract
from starkware.starknet.testing.starknet import Starknet
# from python_hash_branch import hash_branch_named_tuple
from collections import namedtuple
# from generate_merkleb import generate_proof
# from starkware.starknet.cli.starknet_cli import get_state_update
from starkware.starknet.cli.starknet_cli import get_feeder_gateway_client
from starkware.starknet.services.api.feeder_gateway.feeder_gateway_client import FeederGatewayClient
from services.external_api.client import RetryConfig
import json
import requests


@pytest.fixture
async def starknet_ins() -> Starknet:
    return await Starknet.empty()


@pytest.fixture
async def branch_contract(starknet_ins: Starknet) -> StarknetContract:
    # return await starknet_ins.deploy(source="/home/ago/projects/ghost_token/contracts/cairo/branch_verify.cairo", cairo_path=["contracts"])
    return await starknet_ins.deploy(source="../contracts/cairo/branch_verify.cairo", cairo_path=["contracts"])

@pytest.fixture
async def state_contract(starknet_ins: Starknet) -> StarknetContract:
    # return await starknet_ins.deploy(source="/home/ago/projects/ghost_token/contracts/cairo/branch_verify.cairo", cairo_path=["contracts"])
    return await starknet_ins.deploy( source="../contracts/cairo/state_verify.cairo", cairo_path=["../contracts/cairo"])

@pytest.fixture
async def test_get_hash():

    # get the storage_contract info
    # storage_contract_address = "0x35572dec96ab362c35139675abc4f1c9d6b15ee29c98fbf3f0390a0f8500afa"
    # storage_tx_hash = "0x5750bd4870d80c7f58c3f2e443f54001fa5427f36e3dad4b66a95fcd30874aa"

    storage_contract_address = "0x126a13039b9122a2459f9b1053a8e0c25ad55a9096e7924b6d854cfc31ce8d7"
    storage_tx_hash = "0x7e187d8bedb3edb5c1557a0469efc77d9891e2142009a0a0684c8abf6b71960"

    # get feeder_gateway_client
    retry_config = RetryConfig(n_retries=1)
    feeder_gateway_client = FeederGatewayClient(
        url="https://alpha4.starknet.io/feeder_gateway", retry_config=retry_config)

    block_hash = None
    block_number = None
    acceptance_iterator = 0
    # while block_hash == None:
    #     acceptance_iterator += 1
    #     print(f"this is loop {acceptance_iterator}")
    #     tx_receipt = await feeder_gateway_client.get_transaction_receipt(tx_hash=storage_tx_hash)

    #     block_hash = tx_receipt.block_hash
    #     block_number = tx_receipt.block_number
    #     print(block_hash)
    #     print(block_number)
    #     time.sleep(15)

    block_hash = "0x4d893935543cc0a39d1ce1597695e0fc02f9512781e0b23f41bbb01b0c6b5f1"
    block_number = 234500

    block_state_updates = await feeder_gateway_client.get_state_update(
        block_hash=block_hash, block_number=block_number)

    dep_contract_list = block_state_updates["state_diff"]["deployed_contracts"]
    storage_contract_hash = 0
    for contract_iterator in dep_contract_list:
        if contract_iterator["address"] == storage_contract_address:
            storage_contract_hash = contract_iterator["class_hash"]

    assert storage_contract_hash != 0, "Contract not found on chain"

    return((block_number, storage_contract_address, storage_contract_hash))


# next call the api to get the merkle branch belonging to it
# call the contract

@pytest.mark.asyncio
async def test_core(starknet_ins: Starknet, branch_contract: StarknetContract,state_contract: StarknetContract,  test_get_hash: tuple):

    # make a post request for the branch needed
    (block_number, storage_contract_address, contract_hash) = test_get_hash

    url = "https://test.slush.dev/generate_proof"

    contract_address = storage_contract_address
    # contract_hash = ""

    # set the following by hand to sth we know will work
    json_object = {
        "block": 235000,
        "contract": contract_address,
        "variable": "variable"
    }
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.post(url, data=json.dumps(json_object), headers=headers)
    # print("response")
    # print(response.json)

    response_dict = json.loads(response.text)
    # print(response_dict.keys())
    # print(response_dict["storage_root"])

    # unpack the content of the request
    merkle_branch_high = response_dict["merkleb_high"]
    merkle_branch_low = response_dict["merkleb_low"]
    root_hash = response_dict["root_hash"]
    storage_root = response_dict["storage_root"]

    # format the merkle trees so it can be passed to the contract

    # merkle_branch_low_dicts = [{"height": i[0], "position": i[1],
    #                             "length": i[2], "path": i[3], "value": i[4]} for i in merkle_branch_low[1:]]
    # merkle_branch_high_dicts = [{"height": i[0], "position": i[1],
    #                             "length": i[2], "path": i[3], "value": i[4]} for i in merkle_branch_high]
    merkle_branch_low_tuple = [tuple(i) for i in merkle_branch_low]
    merkle_branch_high_tuple = [tuple(i) for i in merkle_branch_high]

    print(merkle_branch_low)
    leaf = tuple(merkle_branch_low[0])
    print(f"leaf elements {leaf}")

    contract_leaf=tuple(merkle_branch_high[0])

    # res_hash = await branch_contract.verify_branch( contract_leaf ,
    #                                                       branch=merkle_branch_high_tuple[1:],
    #                                                       root_hash=int("0x" + root_hash, 16)).call()

    # res_hash = await branch_contract.verify_branch(leaf=leaf, branch=merkle_branch_low_tuple[1:],
    #                                                       root_hash=int("0x" + storage_root, 16)).call()

    
    # res_hash = await branch_contract.verify_both_branches(leaf=leaf, branch_low=merkle_branch_low_tuple[1:],
    #                                                       root_low_hash=int("0x" + storage_root, 16), contract_address=int(contract_address, 16), contract_hash=int("0x" + contract_hash, 16),
    #                                                       branch_high=merkle_branch_high_tuple[1:],
    #                                                       root_high_hash=int("0x" + root_hash, 16)).call()

    res_hash=  state_contract.initialise(int("0x126a13039b9122a2459f9b1053a8e0c25ad55a9096e7924b6d854cfc31ce8d7", 16), int("0x"+"07c656556234b252fb3d67029d795bcda48ee9721f75c08619e164009cad1f0f", 16))
    res_hash =  state_contract.verify_increment(0, leaf, merkle_branch_low_tuple[1:], int("0x" + storage_root, 16), merkle_branch_high_tuple[1:], root_high_hash=int("0x" + root_hash, 16))
    print(res_hash)
    return()
