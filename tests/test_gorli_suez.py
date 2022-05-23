# how does the cairo testing look?
# Use code from Fossil


# make contract deployable
# deploy contract
# call contract on the test input
# call python code on test input
# verify contract gives same output as the python output
from .generate_merkleb import generate_proof
import time
from pathlib import Path
from starknet_py.contract import Contract
from starknet_py.net.client import Client
from services.external_api.base_client import RetryConfig
from starkware.starknet.services.api.feeder_gateway.feeder_gateway_client import FeederGatewayClient
from starkware.starknet.cli.starknet_cli import get_feeder_gateway_client
from collections import namedtuple
from starkware.starknet.testing.starknet import Starknet
from starkware.starknet.testing.contract import StarknetContract
import pytest

# from tkinter import W
# from typing import NamedTuple


# from python_hash_branch import hash_branch_named_tuple
# from starkware.starknet.cli.starknet_cli import get_state_update
# starknet_py

# @pytest.fixture
# async def starknet_ins() -> Starknet:
#     return await Starknet.empty()


# @pytest.fixture
# async def branch_contract(starknet_ins: Starknet) -> StarknetContract:
#     # return await starknet_ins.deploy(source="/home/ago/projects/ghost_token/contracts/cairo/branch_verify.cairo", cairo_path=["contracts"])
#     return await starknet_ins.deploy(source="../contracts/cairo/branch_verify.cairo", cairo_path=["contracts"])


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

    client = Client("testnet")

    # deployment_result = await Contract.deploy(
    #     client, compilation_source={"/home/proj/ghost_token/contracts/cairo/branch_verify.cairo"}, search_paths=["contracts"]
    # )

    contract_address = "0x35572dec96ab362c35139675abc4f1c9d6b15ee29c98fbf3f0390a0f8500afa"

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
        tx_receipt = await feeder_gateway_client.get_transaction_receipt(tx_hash="0x5750bd4870d80c7f58c3f2e443f54001fa5427f36e3dad4b66a95fcd30874aa")

        block_hash = tx_receipt.block_hash
        block_number = tx_receipt.block_number
        # print(tx_receipt)
        print(block_hash)
        print(block_number)
        time.sleep(15)

    block_state_updates = await feeder_gateway_client.get_state_update(
        block_hash=block_hash, block_number=block_number)

    dep_contract_list = block_state_updates["state_diff"]["deployed_contracts"]
    contract_hash = 0
    for contract_iterator in dep_contract_list:
        if contract_iterator["address"] == contract_address:
            contract_hash = contract_iterator["contract_hash"]

    assert contract_hash != 0, "Contract not found on chain"

    return((block_number, contract_address, contract_hash))

# test the cairo branch verification works for an arbitrary contract storag_var
# will work once generate_proof outputs the correct outputs


# @pytest.mark.asyncio
# async def test_import_branch(test_get_hash: tuple):

#     print("Testing custom imported branch")

#     # real_branch = [[251, 2087021424722619777119509474943472645767659996348769578120564519014510906823, 0, 0, 925923027743716088412580218759933356705924200491378477898922997267440127909], [19, 302391, 232, 804599282193126534729012206945677246823683991466037958900426319638155, 2845907075484037364340839605230938759614031545690464816023248203590004103890], [15, 18898, 1, 1, 2068999822834717155277431254277993556996921809430267328221339871988239691498], [14, 9448, 0, 0, 2626297209765236621112568054025023411157280018298857612198388327438765672720], [13, 4725, 0, 0, 114042384147459021247589628548989524378804968261581027693897228674841869060], [12, 2363, 0, 0, 363544692136358849593922891137150500414254016895051513683597360015525958644], [11, 1180, 0, 0, 1455217617578759071219323265713615622485361384186997712159947788454446006627], [
#     #     10, 591, 0, 0, 2206032403902298161642980152874228407049484295795844662530069446718827489044], [9, 294, 0, 0, 2987505503067271205655009149904786789113847611235725839287179543737548254375], [8, 146, 0, 0, 888666846273684553742385526466199882452300571760042010132161258023056564811], [7, 72, 0, 0, 1628637071339699414739222192994669561688627612078636828121896912385471552952], [6, 37, 0, 0, 1345256175674707089191791658560608135523660778760243573736085934114218009965], [5, 19, 0, 0, 3398541956851574724602720438280143714473047022802377852322768518123275525521], [4, 8, 0, 0, 1622095540731265172145181973183423146174436422526103308238267871709620380432], [3, 5, 0, 0, 456614750810695172736454163323963431217958450263303308677873234045662684514], [2, 3, 0, 0, 312345566541817044255288812116449046262495767671064483232498601625367264889], [1, 0, 0, 0, 908782179392994200239506909464745281819857492057798832247104747873438968770]]

#     # root_hash = 2100660188095084288620515079086904656261336581214533446535447348142332014717
#     client = Client("testnet")

#     (block_number, contract_address, contract_hash) = test_get_hash
#     print(block_number)
#     branch_contract = Contract.sync.from_address(contract_address, client)

#     root_hash, storage_root, merkle_branch_high, merkle_branch_low = generate_proof(block_num=block_number,
#                                                                                     contract_address=contract_address, var_name="variable")
#     merkle_branch_high_tuple = [tuple(i) for i in merkle_branch_high]
#     merkle_branch_low_tuple = [tuple(i) for i in merkle_branch_low[1:]]
#     leaf = merkle_branch_low[0]

#     total_len = 251

#     assert leaf.value == 0, "Leaf value not 0"

#     # first need to call the contract, here storage_var will still be 0

#     res_hash = await branch_contract.verify_both_branches(leaf=leaf, branch_low=merkle_branch_low_tuple, total_low_len=leaf.height,
#                                                           root_low_hash=storage_root, contract_address=contract_address, contract_hash=contract_hash,
#                                                           branch_high=merkle_branch_high_tuple,
#                                                           total_high_len=total_len, root_high_hash=root_hash).call()

#     root_hash, storage_root, merkle_branch_high, merkle_branch_low = generate_proof(block_num=block_number,
#                                                                                     contract_address=contract_address, var_name="variable")

#     merkle_branch_high_tuple = [tuple(i) for i in merkle_branch_high]
#     merkle_branch_low_tuple = [tuple(i) for i in merkle_branch_low[1:]]
#     leaf = merkle_branch_low[0]
#     # first need to call the contract, here storage_var will still be 18
#     assert leaf.value == 18, "Leaf value not 18"

#     res_hash = await branch_contract.verify_both_branches(leaf=leaf, branch_low=merkle_branch_low_tuple, total_low_len=leaf.height,
#                                                           root_low_hash=storage_root, contract_address=contract_address, contract_hash=contract_hash,
#                                                           branch_high=merkle_branch_high_tuple,
#                                                           total_high_len=total_len, root_high_hash=root_hash).call()
#     return()

@pytest.mark.asyncio
async def test_import_branch_suez(test_get_hash: tuple):

    print("Testing custom imported branch")

    client = Client("testnet")

    (block_number, contract_address, contract_hash) = test_get_hash
    print(block_number)
    branch_contract = Contract.from_address(contract_address, client)
    print(branch_contract)

    root_hash, storage_root, merkle_branch_high, merkle_branch_low = generate_proof(block_num=block_number,
                                                                                    contract_address=int(contract_address, 16), var_name="balances")
    merkle_branch_high_tuple = [tuple(i) for i in merkle_branch_high]
    merkle_branch_low_tuple = [tuple(i) for i in merkle_branch_low[1:]]
    leaf = merkle_branch_low[0]

    total_len = 251

    # first need to call the contract, here storage_var will still be 0

    # res_hash = await branch_contract.verify_both_branches(leaf=leaf, branch_low=merkle_branch_low_tuple, total_low_len=leaf.height,
    #                                                       root_low_hash=storage_root, contract_address=contract_address, contract_hash=contract_hash,
    #                                                       branch_high=merkle_branch_high_tuple,
    #                                                       total_high_len=total_len, root_high_hash=root_hash).call()

    # root_hash, storage_root, merkle_branch_high, merkle_branch_low = generate_proof(block_num=block_number,
    #                                                                                 contract_address=contract_address, var_name="variable")

    return()
