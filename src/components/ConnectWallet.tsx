// import { useStarknet } from '@starknet-react/core'

// export function ConnectWallet() {
//   const { account, connect, disconnect, connectors } = useStarknet()

//   if (account) {
//     return (
//       <div>
//         <p>Account: {account}</p>
//         <button onClick={() => disconnect()}>Disconnect</button>
//       </div>
//     )
//   }

//   return (
//     <>
//       {connectors.map((connector, idx) => (
//         <button key={idx} onClick={() => connect(connector)}>
//           Connect
//         </button>
//       ))}
//     </>
//   )
// }

import { useStarknet, InjectedConnector } from '@starknet-react/core'

export function ConnectWallet() {
  const { account, connect, disconnect } = useStarknet()

  if (account) {
    return (
      <div>
        <p>Account: {account}</p>
        <button onClick={() => disconnect(new InjectedConnector())}>Disconnect</button>
      </div>
    )
  }

  return <button onClick={() => connect(new InjectedConnector())}>Connect</button>
}