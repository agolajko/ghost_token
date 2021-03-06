//import React from "react";
import container from "./App.css";
import { useCurrentContract } from "./lib/Contract";
// import { useStarknetCall } from "./lib/hooks";
// import {
//   BlockHashProvider,
//   useBlockHash,
// } from "./providers/BlockHashProvider";
import { StarknetProvider, InjectedConnector } from '@starknet-react/core'

// import { StarknetProvider } from "./providers/StarknetProvider";
import { Transaction, useStarknetTransactionManager } from '@starknet-react/core'
import { starknetAddress } from "./addresses";

// do the below lines need to be rewritten?
// import {
//   TransactionsProvider,
//   useTransactions,
// } from "./providers/TransactionsProvider";

// import { useStarknetInvoke } from "./lib/hooks";
// import { useStarknet } from "./providers/StarknetProvider";
// import { useTransaction } from "./providers/TransactionsProvider";
// import { Contract as StarkwareContract } from "starknet";

import { ConnectWallet } from "./components/ConnectWallet";
import { GetBalance } from "./components/getBalance";
import { Transfer } from "./components/Transfer";
import { VoyagerLink } from "./components/VoyagerLink";
import React, { useEffect, useState } from "react";
// import useWeb3Modal from "./hooks/useWeb3Modal";

declare let window: any;



///////////////////////////////////////////////////////////////
//function WithdrawL2({ contract}: { contract?: StarkwareContract} ) {

////////////////////////////////////////


function App() {
  // const blockNumber = useBlockHash();
  const { contract: currentContract } = useCurrentContract();

  const { transactions } = useStarknetTransactionManager()

  // const { transactions } = useTransactions();
  // const [provider, loadWeb3Modal, logoutOfWeb3Modal] = useWeb3Modal();
  // const [addrL1, setL1Address] = React.useState("0xadd");
  // const updateL1Address = React.useCallback(
  //   (evt: React.ChangeEvent<HTMLInputElement>) => {
  //     setL1Address(evt.target.value);
  //   },
  //   [setL1Address]
  // );

  return (
    <div className="container">

      <ConnectWallet />
      &nbsp; <a href="https://chrome.google.com/webstore/detail/argent-x-starknet-wallet/dlcobpjiigpikoobohmabehhmhfoodbb"><img src="/argentx-button-download.svg" width="200" /></a>

      <h1>Verify a storage variable</h1>
      {<GetBalance contract={currentContract} />}

      <p> This is a proof-of-concept for an inter zkRollup trustless bridge. For now it works "Starknet to Starknet".
        You can verify the value of a storage variable.
      </p>
      <p>
        Get one of the latest blocks from <a href="https://goerli.voyager.online/blocks"> https://goerli.voyager.online/blocks</a>,
        input the Block number and State root and you'll be able to verify the current storage value as well as increase it's value by one.
      </p>

      {/* <Transfer contract={currentContract} /> */}
      <Transfer />

      <div>
        &nbsp;
      </div>
      <div className="rowgrey">
        Starknet Contract Address: {starknetAddress}

      </div>

    </div>
  );
};

function AppWithProviders() {
  const connectors = [new InjectedConnector({ showModal: true })]

  return (
    <StarknetProvider connectors={connectors}>

      {/* <StarknetProvider> */}
      {/* <BlockHashProvider> */}
      {/* <TransactionsProvider> */}
      <App />

      {/* </TransactionsProvider> */}
      {/* </BlockHashProvider> */}
    </StarknetProvider>
  );
}
export default AppWithProviders;
