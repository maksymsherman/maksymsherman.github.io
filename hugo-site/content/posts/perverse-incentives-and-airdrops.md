---
title: "Perverse Incentives and Airdrops"
date: 2021-12-03
description: "Airdrops create perverse incentives for stakeholders with insider information to conduct Sybil attacks and profit from upcoming token distributions."
aliases: ["/p/perverse-incentives-and-airdrops.html"]
---

<h1>Perverse Incentives and Airdrops</h1>
<h5><time datetime="2021-12-03">December 3rd, 2021</time></h5>

<p>
  An “airdrop” is a distribution of crypto tokens for free (Pruden and Chokshi
  2021). Airdrops are a popular method to distribute tokens to users who
  interact with a cryptocurrency project. At the early stages of a project, the
  project’s governance needs to be centralized to allow for the project’s
  continued development. Although tokens can be of different types, most tokens
  airdropped by projects give holders voting rights over the project’s
  governance similar to publicly-traded stocks. Hence, when a protocol is ready
  to decentralize its governance, it releases tokens.
</p>
<p>
  Two primary methods of distribution tokens include airdrop and Inition Coin
  Offerings (ICOs). In an ICO, the price of each token is determined by the open
  market, and anyone can buy tokens regardless of their affiliation with the
  project or lack thereof. On the other hand, airdrops reward early adopters of
  the protocol and enhance project’s marketing. It is argued that early adopters
  care a lot about the long-term success of the protocol, so an airdrop that
  rewards those early adopters and endows them with voting rights leads to the
  better long-term success of the protocol compared to ICOs. As a marketing
  tool, airdrops generate media attention around the protocol and many potential
  users learn about the protocol’s existence. An example of a protocol that has
  utilizied an airdrop is Uniswap in September 2020. Uniswap is a decentralized
  finance protocol used to exchange cryptocurrencies. The airdrop distributed
  400 UNI tokens that, similarly to stocks, empowered their holders to vote on
  Uniswap’s governance decisions. Each UNI token was worth $3 each at the time
  of the airdrop, meaning each user of the protocol received $1200 worth of
  tokens. While airdrops may seem like the best token distribution mechanism,
  those knowing about an upcoming airdrop or working on designing an airdrop for
  a protocol have perverse incentives to profit from knowing insider
  information.
</p>
<p>
  Airdrops suffer from a potential of a Sybil attack. “The Sybil attack in
  computer security is an attack wherein a reputation system is subverted by
  forging identities in peer-to-peer networks” (infernal_toast, 2018). For
  airdrops, a Sybil attack would occur when a stakeholder creates many crypto
  wallets and satisfies the requirements for an upcoming aidrop with wallet
  based on insider information. A prime example of such an attack occurred
  earlier this year as Divergence Ventures, a venture firm with three employees,
  Sybil attacked Ribbon. Divergence Ventures was an early investor in Ribbon, a
  decentralized finance protocol that helps users access crypto structured
  products, such as options, futures, and fixed income built on top of the
  Ethereum blockchain (Introduction to Ribbon). According to Julian Koh,
  Ribbon’s cofounder, Ribbon sent an investor update email announcing the
  decision to conduct an airdrop in the near future on May 17 and the snapshot
  for the airdrop, a point in time that records blockchain’s history to
  determine addresses eligible for the airdrop, was taken on May 22 (Koh, 2021).
</p>
<p>
  Analyzing the Ethereum Blockchain history shows that many Divergent-controlled
  wallets Sybil-attacked Ribbon right after receiving the investor update. More
  specifically, Divergent created many wallets that bought financial instruments
  on Ribbon worth around $300. After the airdrop’s announcement, all wallets
  captured in the snapshot that satisfied the minimum deposit requirement of
  $100 (not disclosed in the investor update) received RBN governance tokens. On
  the first day of RBN token’s cashing out period in October, Divergence
  Ventures transferred Ether, Ethereum’s blockchain native cryptocurrency, from
  a combination of its early-investor wallets and Sybil-attacking wallets to a
  centralized wallet named “Divergent Ventures 1.” The total value of Ether
  Divergence Ventures acquired from its Ribbon-related transactions was more
  than $2.3 million (Volpicelli, 2021).
</p>
<p>
  Admittedly, Divergent Ventures did not conduct the most sophisticated Sybil
  attack. If Divergent Ventures cashed out its Ethereum into US dollars from
  each wallet individually, then it is unlikely someone would uncover their
  scheme. Giving preliminary notice to a cryptocurrency project’s investors
  about an inevitable airdrop creates perverse incentives for those investors. A
  high probability of outsized profits incentivizes investors with insider
  information to act upon that information in the belief their actions will not
  be uncovered. However, is it possible that knowing about an airdrop creates
  perverse incentives for project stakeholders beyond investors, such as project
  owners?
</p>
<p>
  To explore the above question, we should consider a hypothetical scenario that
  could have occurred with a recent airdrop. Ethereum Name Service (ENS) is a
  service that provides a usernames for wallets and projects on the Ethereum
  network. Any wallet can register an ENS username for a total price of around
  $200, including the variable gas fee, which is paid to the Ethereum network
  for conducting the transaction. On November 2, 2021, ENS announced it is
  issuing its governance token $ENS and the token’s allocation. The distribution
  of the tokens was the following:
</p>
<div class="captioned-image-container">
  <figure><img src="/p/images/piar.jpg"</figure>
</div>
<p>
  Starting November 8, 2021, everyone who purchased a username with the service
  as of October 31, 2021, was eligible for the airdrop (25% of the total
  allocation of tokens). As only 25% of all tokens were airdropped, even a
  large-scale Sybil attack would not threaten ENS with possibility of a 51%
  attack in which 51% of colluding token holders gain control of the whole
  crypto project. The airdrop formula was $ENS Tokens = 0.27X + 0.062Y where X
  is the number of days the account owned at least one ENS name and Y is the
  number of days until the expiration of the last name on the account (capped at
  eight years for this formula) ($ENS Token Allocation). If the account also had
  a Primary ENS name set, a process requiring more effort than merely buying a
  domain name, the total number of tokens multiplied by 2. ENS had no
  significant outside investors and did not announce the airdrop to anyone
  outside of its core contributors. Despite no outside knowledge of the airdrop,
  ENS insiders, such as eleven core contributors, had a perverse incentive to
  profit from what they knew about the airdrop.
</p>
<p>
  An ENS insider, a hypothetical person A, could partake in a Sybil attack to
  profit from the airdrop. Person A would create many wallets, buy an ENS domain
  for eight years, and set a Primary ENS name for all wallets. For a roughly
  $200 investment for each wallet, person A would receive ENS=2(0.271
  (day)+0.0622918 (days))=2181=362 (tokens).While the exact price of each token
  was unknown until the beginning of public trading, widespread public interest
  in ENS and ENS’s role in the future of the Ethereum ecosystem made a Sybil
  attack an attractive optiion for person A. Indeed, at the opening price of
  $23.64, each person A’s wallet would be worth $23.64362=$8558 for an
  investment of $200. Since the airdrop, the price of ENS’s token continued to
  increase, and one token is worth $54 as of December 3, 2021.
</p>
<p>
  Acting in a more refined manner than Divergent Ventures, person A could cash
  out Ether from each account into a fiat currency so the records of further
  transactions would evade a public blockchain. Alternatively, person A could
  transfer Ether from each wallet into a centralized wallet linked to Person A.
  To disguise the Sybil attack, person A could register some domain names for
  less than eight years without setting a Primary ENS name for some wallets.
  Another method would be to wait a few months before cashing out ENS tokens
  from all wallets instead of on the first day of public trading. In any case,
  it would be incredibly challenging to link a set of anonymous crypto wallets
  to a single individual unless blockchain records point to a wallet connected
  to a real-world entity like in the case of Divergence Ventures.
</p>
<p>
  Certainly, there are risks associated with person A’s Sybil attack. If the
  attack gets uncovered, that person would lose their position at the project
  they dedicated a lot of time to building. Nevertheless, an incredibly low
  chance of getting caught incentivizes person A to act upon the insider
  information by optimizing for an upcoming airdrop. As Gian M. Volpicelli
  noted, “many of the behaviors that crypto-sleuths expose take place in a
  regulatory vacuum. ‘Insider trading has a very specific meaning—using
  nonpublic information when trading on the stock market,’ says Nick Price, a
  crypto-asset disputes specialist at law firm Osborne Clarke. ‘These tokens are
  not stocks and shares. NFTs aren't regulated, so it is not insider trading.”
  (Wired). A sense of certainty about the absence of future judicial punishment
  logically plays a role in the deliberations of those with insider information.
  However, traditional governments cannot effectively regulate an anonymous
  blockchain and punish those who break ethical rules.
</p>
<p>
  A system built on anonymity prevents individual accountability. In the way
  they are currently conducted, airdrops create perverse incentives for those
  who know about the upcoming airdrop. Sybil attacks subvert the decentralized
  ethos of the blockchain ecosystem and contradict social notions of justice in
  which those with insider information should not be able to achieve outsized
  profit based on that information. Placing blind trust that humans, inherently
  fallible creatures, will ignore a perverse incentive is not a strategy that
  can be trusted in the long-term. Cryptocurrency projects are still in their
  infancy; to ensure long-term public trust in early-stage cryptocurrency
  projects, a better system of token distribution should be created to align
  stakeholders’ incentives.
</p>
<p>
  <em
    >Note:
    <a href="https://dune.com/blog/uni-airdrop-analysis?ref=maksymsherman.com"
      >The Uniswap Airdrop - Lessons for the Industry</a
    >, published in November 2022, provides a great overview of the perils of
    airdrops.</em
  >
</p>
<p>References</p>
<p>
  “$ENS Token Allocation.” Mirror. Accessed December 3, 2021.
  https://ens.mirror.xyz/-eaqMv7XPikvXhvjbjzzPNLS4wzcQ8vdOgi9eNXeUuY.
</p>
<p>
  infernal_toast. “All Token Distribution Is Flawed - A Primer on Sybil
  Attacks.” Medium. Medium, April 2, 2018.
  https://infernaltoast.medium.com/all-token-distribution-is-flawed-thats-why-we-need-pow-tokens-8a79b460f0aa.
</p>
<p>
  “Introduction to Ribbon.” Ribbon Finance. Accessed December 3, 2021.
  https://docs.ribbon.finance/.
</p>
<p>
  Koh, Julian. “Ribbon &amp; Divergence Ventures.” Medium. Medium, October 9,
  2021. https://juliankoh.medium.com/ribbon-divergence-ventures-653b03788612.
</p>
<p>
  ​​Pruden, Alex, and Sonal Chokshi. “Crypto Glossary: Cryptocurrencies and
  Blockchain.” Andreessen Horowitz, March 28, 2021.
  https://a16z.com/2019/11/08/crypto-glossary/.
</p>
<p>
  Volpicelli, Gian M. “Twitter Vigilantes Are Hunting Down Crypto Scammers.”
  Wired. Conde Nast, November 15, 2021.
  https://www.wired.com/story/twitters-crypto-vigilantes-are-just-getting-started/.
</p>
