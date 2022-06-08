import React from "react";
import { Contract } from "starknet";
import { useStarknetInvoke } from '@starknet-react/core'
import { useStarknet } from '@starknet-react/core'
import { useCurrentContract } from "../../lib/Contract";
// import { useCurrentContract } from ''


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

  async function handle_click(storage_var, block_number, state_root) {
    // first perform the post request 
    // next send the result to the contract
    console.log("works?");

    const send_data = {
      // "block": "230071",
      "block": block_number,
      "contract": "0x071cdfdb934f450e8441dd201c5d89d5f6a82a68c02969de99f5481bd7a828f8",
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
    // .then(response_data => response_data.json())
    // .then(res => console.log(res))
    // .then(merkleb_low_0_0 = response_data.)

    // parse the result from the POST request to send it to the contract

    // console.log(response_data.json())

    const response = await response_data.json()
    console.log(response)
    console.log("now")
    console.log(response.merkleb_high)

    const state_root_ = state_root
    // const state_root_ = String(BigInt(state_root))
    const leaf_height = 251
    const leaf_position = 778741677097751136629359488410499500026881115738990894538495916875030189956
    const leaf_length = response.merkleb_low[0][2]
    const leaf_path = response.merkleb_low[0][3]
    const leaf_value = response.merkleb_low[0][4]
    console.log("response.merkleb_low.lenght")
    console.log(response.merkleb_low.length)
    // console.log(leaf_length)

    console.log("response.merkleb_low")
    console.log(response.merkleb_low)
    const branch_low = response.merkleb_low.slice(1, 5).flat();

    console.log("merkleb_low_truncated.length")
    const merkleb_low_truncated_length = branch_low.length
    console.log(branch_low)

    const total_low_len = String(251)
    const root_low_hash = String(BigInt("0x" + response.storage_root))

    const branch_high = response.merkleb_high.slice(1, 5).flat();

    const total_high_len = response.merkleb_high.length;
    const root_high_hash = String(BigInt("0x" + response.root_hash))

    console.log("vars")
    console.log(response.merkleb_low)
    console.log(leaf_height)
    console.log(leaf_position)
    console.log(leaf_length)
    console.log(leaf_path)
    console.log(leaf_value)
    console.log(branch_low)
    console.log("branch_high")
    console.log(branch_high)
    console.log(root_low_hash)
    console.log(root_high_hash)
    console.log(state_root_)
    console.log(branch_high)

    console.log("type of vars")
    console.log(typeof response.merkleb_low)
    console.log(typeof leaf_height)
    console.log(typeof leaf_position)
    console.log(typeof leaf_length)
    console.log(typeof leaf_path)
    console.log(typeof leaf_value)
    console.log(typeof branch_low)
    console.log(typeof branch_high)
    console.log(typeof root_low_hash)
    console.log(typeof root_high_hash)
    console.log(typeof state_root_)
    console.log(typeof branch_high)
    console.log(typeof total_high_len)
    console.log(typeof total_low_len)

    var branch_low_dict: { [id: string]: number } = {
      "height": 1,
      "position": 1,
      "length": 1,
      "path": 1,
      "value": 1
    };
    console.log(typeof branch_low_dict)

    var merkle_branch_low_dict = []
    var merkle_branch_high_dict = []
    for (let i = 1; i <= 8; i++) {
      merkle_branch_low_dict.push({
        "height": response.merkleb_low[i]["0"], "position": response.merkleb_low[i]["1"],
        "length": response.merkleb_low[i]["2"], "path": response.merkleb_low[i]["3"], "value": response.merkleb_low[i]["4"]
      })
    }
    // for (let i = 0; i <= response.merkleb_high.length - 1; i++) {
    for (let i = 0; i <= 8; i++) {
      merkle_branch_high_dict.push({
        "height": response.merkleb_high[i]["0"], "position": response.merkleb_high[i]["1"],
        "length": response.merkleb_high[i]["2"], "path": response.merkleb_high[i]["3"], "value": response.merkleb_high[i]["4"]
      })
    }

    // for (let i = 0; i <= 251; i++) {
    //   merkle_branch_low_dict.push({
    //     "height": response.merkleb_high[i], "position": response.merkleb_high[i],
    //     "length": response.merkleb_high[i], "path": response.merkleb_high[i], "value": response.merkleb_high[i]
    //   })
    // }

    console.log(response.merkleb_low.length)
    console.log(merkle_branch_low_dict)
    console.log(merkle_branch_high_dict)


    // none of these function calls  work
    invoke({
      args: [1, { height: 71, position: 72, length: 73, path: 74, value: 75 },
        [{ height: 71, position: 71, length: 73, path: 74, value: 75 }], 8, 9, [{ height: 101, position: 102, length: 103, path: 104, value: 105 }], 11, 12
      ], metadata: { method: "verify_increment" }
    })

    // invoke({
    //   args: [[1], { height: 71, position: 72, length: 73, path: 74, value: 75 }, [1],
    //   [{ height: 71, position: 71, length: 73, path: 74, value: 75 }], [8], [9], [1], [{ height: 101, position: 102, length: 103, path: 104, value: 105 }], [11], [12]
    //   ], metadata: { method: "verify_increment" }
    // })

    // invoke({
    //   args: [1, { height: 71, position: 72, length: 73, path: 74, value: 75 },
    //     [{ height: 71, position: 72, length: 73, path: 74, value: 75 }, { height: 71, position: 72, length: 73, path: 74, value: 75 }],
    //     [8], 9, [{ height: 101, position: 102, length: 103, path: 104, value: 105 }, { height: 71, position: 72, length: 73, path: 74, value: 75 }], [11], 12
    //   ], metadata: { method: "verify_increment" }
    // })


    //invoke({
    //  args: [1, 2, 3, 4, 5, 6,
    //    [{ "height": 71, "position": 72, "length": 73, "path": 74, "value": 75 }], 8, 9, [{ "height": 101, "position": 102, "length": 103, "path": 104, "value": 105 }], 11, 12
    //  ], metadata: { method: "verify_increment" }
    //})
    //invoke({
    //  args: [1, 2, 3, 4, 5, 6,
    //    [{ "height": 71, "position": 72, "length": 73, "path": 74, "value": 75 }], 8, 9, [{ "height": 101, "position": 102, "length": 103, "path": 104, "value": 105 }], 11, 12
    //  ], metadata: { method: "verify_increment" }
    //})

    // // this works
    // invoke_init({
    //   args: ["0x12", "1"], metadata: { method: "initialise" }
    // })


    // invoke_init({
    //   args: [state_root_, leaf_height], metadata: { method: "initialise" }
    // })



    // invoke({
    //   args: [state_root_, leaf_height, leaf_position, leaf_length, leaf_path, leaf_value,
    //     [merkle_branch_low_dict], total_low_len, root_low_hash, [merkle_branch_high_dict], total_high_len, root_high_hash
    //   ], metadata: { method: "verify_increment" }
    // })
    // invoke({
    //   args: [state_root_, leaf_height, leaf_position, leaf_length, leaf_path, leaf_value,
    //     branch_low, total_low_len, root_low_hash, branch_high, total_high_len, root_high_hash
    //     // args: [state_root_: state_root_, leaf: { leaf_height, leaf_position, leaf_length, leaf_path, leaf_value },
    //     // branch_low: branch_low, total_low_len: total_low_len, root_low_hash: root_low_hash, branch_high: branch_high, total_high_len: total_high_len, root_high_hash: root_high_hash
    //   ], metadata: { method: "verify_increment" }
    // })
    // return ({state_root_, leaf_height, leaf_position, leaf_length, leaf_path, leaf_value, branch_low, total_low_len, root_low_hash, branch_high, total_high_len, root_high_hash})
    console.log("get ehre?")
  }

  try {
    return (
      <div>

        <div className="row">
          <input onChange={updateStorage} value={storage_var} type="text" placeholder="Value of storage variable" />
          &nbsp;
          {/*<input onChange={updateAmount} value={amount_low} type="text" />*/}
          <input onChange={updateBlock} value={block_number} type="text" placeholder="Block number" />
          &nbsp;
          <input onChange={updateRoot} value={state_root} type="text" placeholder="State root" />
          &nbsp;

          <button
            // onClick={() => verify_increment && verify_increment({ 0, 1, 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12 })}
            onClick={() => handle_click(storage_var, block_number, state_root)}
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
