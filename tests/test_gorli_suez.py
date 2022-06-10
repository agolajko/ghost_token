# how does the cairo testing look?
# Use code from Fossil


# make contract deployable
# deploy contract
# call contract on the test input
# call python code on test input
# verify contract gives same output as the python output
from api.generate_proof import generate_proof
import time
from pathlib import Path
from starknet_py.contract import Contract
from starknet_py.net.client import Client
from services.external_api.client import RetryConfig
from starkware.starknet.services.api.feeder_gateway.feeder_gateway_client import FeederGatewayClient
from starkware.starknet.cli.starknet_cli import get_feeder_gateway_client
from collections import namedtuple
from starkware.starknet.testing.starknet import Starknet
from starkware.starknet.testing.contract import StarknetContract
import pytest


@pytest.fixture
async def deploy_verify_contract():
    client = Client("testnet")

    # deploy verifying contract
    deployment_result = await Contract.deploy(
        client, compilation_source={"contracts/cairo/branch_verify.cairo"}, search_paths=["contracts"]
        # client, compilation_source={"../contracts/cairo/branch_verify.cairo"}, search_paths=["contracts"]
    )

    accepted = await deployment_result.wait_for_acceptance()
    print(accepted)
    contract_address = deployment_result.deployed_contract.address
    return contract_address

# @pytest.mark.asyncio


@pytest.fixture
async def test_get_hash():
    # sequence:
    # deploy contract to Gorli
    # get deployment address
    # get transaction hash
    # feed transaction hash to get_transaction_receipt, returns block_hash and block_number
    # use block_hash and block_number to get_state_update
    # from get_state_update use the contract address to find the contract_hash

    # get the storage_contract info
    storage_contract_address = "0x35572dec96ab362c35139675abc4f1c9d6b15ee29c98fbf3f0390a0f8500afa"
    storage_tx_hash = "0x5750bd4870d80c7f58c3f2e443f54001fa5427f36e3dad4b66a95fcd30874aa"
    # storage_contract_address = "0x035572dec96ab362c35139675abc4f1c9d6b15ee29c98fbf3f0390a0f8500afa"
    # storage_tx_hash = "0x507167c1abf2e485f8e58e57aad71b99295875953158e234c339f1cd4a077df"

    # get feeder_gateway_client
    retry_config = RetryConfig(n_retries=1)
    feeder_gateway_client = FeederGatewayClient(
        url="https://alpha4.starknet.io/feeder_gateway", retry_config=retry_config)

    block_hash = None
    block_number = None
    acceptance_iterator = 0
    while block_hash == None:
        acceptance_iterator += 1
        print(f"this is loop {acceptance_iterator}")
        tx_receipt = await feeder_gateway_client.get_transaction_receipt(tx_hash=storage_tx_hash)

        block_hash = tx_receipt.block_hash
        block_number = tx_receipt.block_number
        # print(tx_receipt)
        print(block_hash)
        print(block_number)
        time.sleep(15)

    block_state_updates = await feeder_gateway_client.get_state_update(
        block_hash=block_hash, block_number=block_number)

    dep_contract_list = block_state_updates["state_diff"]["deployed_contracts"]
    storage_contract_hash = 0
    for contract_iterator in dep_contract_list:
        if contract_iterator["address"] == storage_contract_address:
            storage_contract_hash = contract_iterator["class_hash"]

    assert storage_contract_hash != 0, "Contract not found on chain"

    return((block_number, storage_contract_address, storage_contract_hash))

# test the cairo branch verification works for an arbitrary contract storag_var
# will work once generate_proof outputs the correct outputs


@pytest.mark.asyncio
async def test_import_branch_suez(test_get_hash: tuple, deploy_verify_contract):

    print("Testing custom imported branch")

    client = Client("testnet")

    verify_contract_address = deploy_verify_contract

    (block_number, storage_contract_address, contract_hash) = test_get_hash
    block_number = 24_444
    branch_contract = await Contract.from_address(verify_contract_address, client)
    print(branch_contract)

    # we are generating a proof of a contract's storage variable
    # this contract variable corresponds to the address of an account

    contract_variables = [
        1042400286771102661652363919924244740833084544629561888149967508378012757441]
    storage_var_name = "balances"
    root_hash, storage_root, merkle_branch_high, merkle_branch_low = generate_proof("/mnt/volume_lon1_01/pathfinder/goerli.sqlite", block_number,
                                                                                    int(storage_contract_address, 16), storage_var_name, contract_variables)
    merkle_branch_high_tuple = [tuple(i) for i in merkle_branch_high]
    merkle_branch_low_tuple = [tuple(i) for i in merkle_branch_low[1:]]

    merkle_branch_low_dicts = [{"height": i[0], "position": i[1],
                                "length": i[2], "path": i[3], "value": i[4]} for i in merkle_branch_low[1:]]
    merkle_branch_high_dicts = [{"height": i[0], "position": i[1],
                                "length": i[2], "path": i[3], "value": i[4]} for i in merkle_branch_high]

    print(merkle_branch_low)
    leaf = merkle_branch_low[0]
    print(f"leaf elements {leaf}")

    total_len = 251

    # first need to call the contract, here storage_var will still be 0
    # leaf_tuple = (leaf[0], leaf[1], leaf[2], leaf[3], leaf[4])
    leaf_dict = {"height": leaf[0], "position": leaf[1],
                 "length": leaf[2], "path": leaf[3], "value": leaf[4]}
    res_hash = await branch_contract.functions["verify_both_branches"].invoke(leaf=leaf_dict, branch_low=merkle_branch_low_dicts, total_low_len=leaf[0],
                                                                              root_low_hash=int(storage_root, 16), contract_address=int(storage_contract_address, 16), contract_hash=int(contract_hash, 16),
                                                                              branch_high=merkle_branch_high_dicts,
                                                                              total_high_len=total_len, root_high_hash=int(root_hash, 16), max_fee=0)

    # root_hash, storage_root, merkle_branch_high, merkle_branch_low = generate_proof(block_num=block_number,
    #                                                                                 contract_address=contract_address, var_name="variable")
    print(res_hash)

    return()
