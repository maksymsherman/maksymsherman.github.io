---
title: "Soulbound(less) Tokens"
date: 2025-02-09
description: "Vitalik Buterin introduced soulbound tokens as non-transferable NFTs, but fundamental technical limitations make true non-transferability impossible to enforce on the blockchain."
aliases: ["/p/soulbound(less)-tokens.html"]
---



# Soulbound(less) Tokens


##### <time datetime="2025-02-09">February 9th, 2025</time>


In January 2022, Vitalik Buterin introduced the concept of [soulbound tokens](https://vitalik.eth.limo/general/2022/01/26/soulbound.html)—NFTs that cannot be transferred once minted. While Vitalik discussed the use of soulbound NFTs for governance rights and certificates like drivers licenses and university degrees, fundamental technical limitations make true non-transferability impossible to enforce on the blockchain.


### Technical Challenges


Vitalik himself identified the core challenge of implementing soulbound tokens while discussing how POAP (Proof of Attendance Protocol) decided to not block the transferability of the POAPs:


> The security of non-transferability implemented "naively" is not very strong anyway because users could just create a wrapper account that holds the NFT and then sell the ownership of that.


As there were instances in which some POAPs got sold, the team suggested:


> that developers who care about non-transferability implement checks on their own: they could check on-chain if the current owner is the same address as the original owner, and they could add more sophisticated checks over time if deemed necessary.


But the very check of whether the current owner is the same address as the original falls prey to Vitalik's own idea of someone transferring ownership of a wrapper account that holds the NFT.


### How to address wrappers?


#### The EOA-only approach


One initially promising solution is to restrict soulbound tokens to externally owned accounts (EOAs) like the wallet you make in MetaMask. EOAs are controlled by a single private key, making them seemingly perfect for soulbound tokens: since you can't credibly "forget" a private key, you theoretically can't transfer ownership of the account. Ethereum's eth.getCode() and Solana's isOnCurve allow systems to distinguish between EOAs and smart contracts.


However, restricting soulbound tokens to EOAs is impractical. Individual wallets are moving in the direction of becoming smart contracts, especially for high-net worth users (whales) who demand better security than a single seed phrase or private key.


In addition, [EIP 7702](https://www.alchemy.com/blog/eip-7702-ethereum-pectra-hardfork) that is set to launch in the coming months will allow EOAs to become smart contracts. Even if you restrict soulbound token creation to EOAs, users could upgrade their EOAs to smart contracts through EIP 7702. If you add a restriction to only validate soulbound tokens held by EOAs at verification time, then migrating an EOA to a smart contract would result in losing "ownership" of the soulbound token.


In the future, EOAs will migrate to smart contracts since their public key generation relies on the Elliptic Curve Digital Signature Algorithm (ECDSA), which is vulnerable to quantum computers. As quantum computers become more powerful, EOAs will need to transition to quantum-resistant solutions, most likely upgrading to smart contract accounts using EIP 7702.


Hence, restricting soulbound tokens ownership to EOAs is not feasible. What about the implications of smart contracts owning soulbound tokens?


#### Smart contracts are inherently wrappers


As Vitalik mentioned in his original post, users can create a wrapper account that holds the soulbound token, and transfer ownership of that account. However, checks of the wrapper smart account cannot guarantee non-transferability.


Smart contracts can implement hidden ownership transfers through custom modules, making true non-transferability impossible. [This Grok conversation](/p/pdfs/Soulboundless_Grok.pdf) walks through how to add shadow owners without triggering visible events and to ensure the shadow owner's address is obfuscated on the blockchain. Anyone who attempts to verify underlying smart contract ownership would not be able to understand which accounts can sign that smart contract's transactions.


### Conclusion


Soulbound tokens cannot practically be bound to a soul. The atomic unit of a blockchain is an account, not a human. As Tim Roughgarden [said:](https://x.com/Tim_Roughgarden/status/1512847113599729668)


> Blockchains are (virtual) computers, not databases.


Enforcing transfer restrictions on Turing-complete blockchains requires handling all possible edge cases. Given the Turing-complete nature of smart contracts, non-transferability cannot be enforced.


We need to switch our thinking from accounts being default-human to default-account, default-bot, or default-AI. Traditional analogies where we assume one account is owned by one human are not applicable in the blockchain world.


One lesson of crypto is that motivated actors will use all technically feasible methods to get a sufficiently lucrative reward. In the non-blockchain space, important applications run in closed environments with strict permissioning. But blockchains are general purpose computers. It is impossible to fully constrain how people interact with an application. Given sufficiently high stakes, users will find ways to circumvent soulbound token restrictions. Soulbound tokens are soulboundless.


---


Here is a simple [GitHub Project which simulates ownership transfer of a wrapper account in SafeIntegrationTest.t.sol.](https://github.com/maksymsherman/Soulboundless)


---


---


Disclosure: *This article is for informational and educational purposes only. Nothing in this article should be construed as legal, technical, or professional advice. The views expressed are solely those of the author and do not represent the views of any affiliated organizations. Readers should conduct their own research and consult with qualified professionals before making any decisions based on this information. The author may hold positions in cryptocurrencies or digital assets discussed in this article. The author does not assume any liability for errors, omissions, or actions taken based on the information provided.*
