import React from "react";
import { Contract } from "starknet";
import { useStarknetInvoke } from '@starknet-react/core'
import { useStarknet } from '@starknet-react/core'
import { useCurrentContract } from "../../lib/Contract";
// import { useCurrentContract } from ''
import { starknetAddress } from "../../addresses";


// export function Transfer({ contract }: { contract?: Contract }) {
export function Transfer() {

  // const { account } = useStarknet();
  const { contract: currentContract } = useCurrentContract()

  // const { invoke } = useStarknetInvoke({ contract: currentContract, method: "initialise" })
  const { invoke: invoke_init } = useStarknetInvoke({ contract: currentContract, method: "initialise" })
  const { invoke } = useStarknetInvoke({ contract: currentContract, method: "verify_increment" })

  // const transactionStatus = useTransaction(hash);

  const [storage_var, setStorage] = React.useState("");
  const [block_number, setBlock] = React.useState("");
  const [state_root, setRoot] = React.useState("");

  //console.log(setAmount)
  const updateStorage = React.useCallback(
    (evt: React.ChangeEvent<HTMLInputElement>) => {
      setStorage(evt.target.value);
    },
    [setStorage]
  );

  const updateBlock = React.useCallback(
    (evt: React.ChangeEvent<HTMLInputElement>) => {
      setBlock(evt.target.value);
    },
    [setBlock]
  );
  const updateRoot = React.useCallback(
    (evt: React.ChangeEvent<HTMLInputElement>) => {
      setRoot(evt.target.value);
    },
    [setRoot]
  );

  async function handle_click(block_number, state_root) {
    // first perform the post request 
    // next send the result to the contract
    console.log("works?");

    const send_data = {
      // "block": "230071",
      "block": block_number,
      "contract": starknetAddress,
      "variable": "variable"
    }

    const response_data = await fetch(
      // fetch(
      "https://test.slush.dev/generate_proof",
      {
        method: 'POST',
        // mode: 'no-cors',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(send_data),
      })


    const response = await response_data.json()
    console.log(response)
    console.log("now")
    console.log(response.merkleb_high)

    // const state_root_ = state_root
    const state_root_ = String(BigInt(state_root))
    const leaf_height = String(BigInt(response.merkleb_low[0][0]))
    const leaf_position = String(BigInt(response.merkleb_low[0][1]))
    const leaf_length = String(BigInt(response.merkleb_low[0][2]))
    const leaf_path = String(BigInt(response.merkleb_low[0][3]))
    const leaf_value = String(BigInt(response.merkleb_low[0][4]))

    console.log("response.merkleb_low")
    console.log(response.merkleb_low)

    const root_low_hash = String(BigInt("0x" + response.storage_root))

    const root_high_hash = String(BigInt("0x" + response.root_hash))


    const merkle_branch_low_dict = []
    const merkle_branch_high_dict = []


    for (let i = 1; i <= response.merkleb_low.length - 1; i++) {
      merkle_branch_low_dict.push({
        height: String(BigInt(response.merkleb_low[i]["0"])), position: String(BigInt(response.merkleb_low[i]["1"])),
        length: String(BigInt(response.merkleb_low[i]["2"])), path: String(BigInt(response.merkleb_low[i]["3"])), value: String(BigInt(response.merkleb_low[i]["4"]))
      })
    }
    for (let i = 1; i <= response.merkleb_high.length - 1; i++) {
      // for (let i = 0; i <= 8; i++) {
      merkle_branch_high_dict.push({
        height: String(BigInt(response.merkleb_high[i]["0"])), position: String(BigInt(response.merkleb_high[i]["1"])),
        length: String(BigInt(response.merkleb_high[i]["2"])), path: String(BigInt(response.merkleb_high[i]["3"])), value: String(BigInt(response.merkleb_high[i]["4"]))
      })
    }

    const leaf = { height: String(BigInt(leaf_height)), position: String(BigInt(leaf_position)), length: String(BigInt(leaf_length)), path: String(BigInt(leaf_path)), value: String(BigInt(leaf_value)) }

    invoke({
      args: [state_root_, leaf,
        merkle_branch_low_dict, root_low_hash, merkle_branch_high_dict, root_high_hash
      ], metadata: { method: "verify_increment" },
    })


    console.log("get ehre?")
  }

  try {
    return (
      <div>

        <div className="row">
          {/* <input onChange={updateStorage} value={storage_var} type="text" placeholder="Value of storage variable" />
          &nbsp; */}
          {/*<input onChange={updateAmount} value={amount_low} type="text" />*/}
          <input onChange={updateBlock} value={block_number} type="text" placeholder="Block number" />
          &nbsp;
          <input onChange={updateRoot} value={state_root} type="text" placeholder="State root" />
          &nbsp;

          <button
            // onClick={() => verify_increment && verify_increment({ 0, 1, 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12 })}
            // onClick={() => handle_click(String(BigInt(block_number)), String(BigInt(state_root)))}
            onClick={() => handle_click(block_number, state_root)}
          // onClick={() => invoke({ args: ["0x12", "12"], metadata: { method: "initialise" } })}
          // onClick={() => invoke({
          //   // args: [state_root_, leaf_height, leaf_position, leaf_length, leaf_path, leaf_value,
          //   // branch_low, total_low_len, root_low_hash, branch_high, total_high_len, root_high_hash
          //   // args: [state_root_: state_root_, leaf: { leaf_height, leaf_position, leaf_length, leaf_path, leaf_value },
          //   // branch_low: branch_low, total_low_len: total_low_len, root_low_hash: root_low_hash, branch_high: branch_high, total_high_len: total_high_len, root_high_hash: root_high_hash
          //   args: ['0x11111111111', '0x1', '0x1', '0x1', '0x1', '0x1',
          //     '0x1', '0x1', '0x1', '0x1', '0x1', '0x1'], metadata: { method: "verify_increment", max_fee: '1000000' },
          // })}
          // onClick={() => transfer && transfer({ addr, amount_low, amount_high })}
          // onClick={() => ({ const { state_root_, leaf_height, leaf_position, leaf_length, leaf_path, leaf_value, branch_low, total_low_len, root_low_hash, branch_high, total_high_len, root_high_hash } = await handle_click(storage_var, block_number, state_root);
          // verify_increment && verify_increment({ state_root_, leaf_height, leaf_position, leaf_length, leaf_path, leaf_value, branch_low, total_low_len, root_low_hash, branch_high, total_high_len, root_high_hash }) }}
          //Tried transferWithError here, that did not catch the error either. 
          //disabled={!transfer || submitting}
          >
            Verify
          </button>
        </div>
        {/* {transactionStatus && hash && (
          <div className="row">
            <h2>Latest Transaction</h2>
            <p>Status: {transactionStatus?.code}</p>
            <p>
              Hash: <VoyagerLink.Transaction transactionHash={hash} />
            </p>
          </div>
        )} */}
      </div >
    );
  } catch (err) {
    console.error(err);
    return (<div>hello</div>);
  }
  //finally {(<div>bello</div>)}
}
