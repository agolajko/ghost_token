import React from "react";
import { Contract } from "starknet";
import { useStarknetInvoke } from "../../lib/hooks";
import { useStarknet } from "../../providers/StarknetProvider";
import { useTransaction } from "../../providers/TransactionsProvider";
import { VoyagerLink } from "../VoyagerLink";

import styles from "./index.module.css";

export function Transfer({ contract }: { contract?: Contract }) {

  const { account } = useStarknet();
  const {
    invoke: verify_increment,
    hash,
    submitting,
  } = useStarknetInvoke(contract, "verify_increment");

  const transactionStatus = useTransaction(hash);

  const [storage_var, setStorage] = React.useState("");
  const [block_number, setBlock] = React.useState("");
  const [state_root, setRoot] = React.useState("");
  // const [amount_high, setAmount_high] = React.useState("");
  // const [addr, setAddress] = React.useState("");

  // const updateAmount = React.useCallback(
  //   (evt: React.ChangeEvent<HTMLInputElement>) => {
  //     setAmount(evt.target.value);
  //     setAmount_low(get_amount_low(evt.target.value));
  //     setAmount_high(get_amount_high(evt.target.value));
  //   },
  //   [setAmount]
  // );

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

  // function get_amount_low(one_num) {
  //   if (one_num == "") { return String(0) }
  //   let new_int = BigInt(Math.floor(10 ** 18 * parseFloat(one_num)));
  //   let am_low = new_int % BigInt((2 ** 128));
  //   return String(am_low)
  // }

  // function get_amount_high(one_num) {
  //   if (one_num == "") { return String(0) }
  //   const new_int = BigInt(Math.floor(10 ** 18 * parseFloat(one_num)));
  //   console.log(new_int)
  //   const am_high = String(new_int / BigInt(2 ** 128));
  //   return am_high
  // }

  // function transferWithError(params) {
  //   try {
  //     if (transfer) transfer(params);
  //     return (1)
  //   }
  //   catch { return (0) }
  //   finally { return (0) }
  // }
  //console.log(contract)
  //if (!account) return null;

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

    const merkleb_low_0_0 = 0

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
    const leaf_height = "251"
    const leaf_position = "778741677097751136629359488410499500026881115738990894538495916875030189956"
    const leaf_length = response.merkleb_low[0][2]
    const leaf_path = response.merkleb_low[0][3]
    const leaf_value = response.merkleb_low[0][4]
    console.log("response.merkleb_low.lenght")
    console.log(response.merkleb_low.length)
    // console.log(leaf_length)

    const branch_low = response.merkleb_low.shift();

    console.log("merkleb_low_truncated.length")
    const merkleb_low_truncated_length = branch_low.length
    console.log(branch_low)

    const total_low_len = "251"
    const root_low_hash = response.storage_root

    const branch_high = response.merkleb_high;

    const total_high_len = "251"
    const root_high_hash = response.root_hash


    verify_increment && verify_increment({ state_root_, leaf_height, leaf_position, leaf_length, leaf_path, leaf_value, branch_low, total_low_len, root_low_hash, branch_high, total_high_len, root_high_hash })
  }

  try {
    return (
      <div className={styles.counter}>

        <div className="row">
          <input onChange={updateStorage} value={storage_var} type="text" placeholder="Value of storage variable" />
          &nbsp;
          {/*<input onChange={updateAmount} value={amount_low} type="text" />*/}
          <input onChange={updateBlock} value={block_number} type="text" placeholder="Block number" />
          &nbsp;
          <input onChange={updateRoot} value={state_root} type="text" placeholder="State root" />
          &nbsp;

          <button
            // onClick={() => transfer && transfer({ addr, amount_low, amount_high })}
            onClick={() => handle_click(storage_var, block_number, state_root)}
          //Tried transferWithError here, that did not catch the error either. 
          //disabled={!transfer || submitting}
          >
            Verify
          </button>
        </div>
        {transactionStatus && hash && (
          <div className="row">
            <h2>Latest Transaction</h2>
            <p>Status: {transactionStatus?.code}</p>
            <p>
              Hash: <VoyagerLink.Transaction transactionHash={hash} />
            </p>
          </div>
        )}
      </div>
    );
  } catch (err) {
    console.error(err);
    return (<div>hello</div>);
  }
  //finally {(<div>bello</div>)}
}
