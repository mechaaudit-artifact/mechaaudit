# Error Case Attribution

This document lists all false negative (FN) and false positive (FP) cases in the
MechaAudit evaluation across three benchmarks (Sherlock 95 + Web3Bugs 51 + DeFiHackLabs 71
= 217 contracts evaluated, 70 VULN + 147 SAFE).

Overall: **TP 59 / FP 18 / FN 11 / TN 129** (Precision 0.766, Recall 0.843, F1 0.803).

---

## 1. False Negatives (11 cases)

A false negative occurs when a ground-truth VULN contract receives a SAFE verdict.
Two distinct failure modes are observed.

### Failure Mode A — Harm verdict not confirmed (9 cases)

The mechanism structure was admitted by the SMT gate (structural SAT), but the harm
verdict stage could not confirm a concrete attacker-beneficial, victim-adverse value delta
in the target-side program slice. The root cause is that the actual on-chain exploitation
either requires multi-block state accumulation that falls outside the bounded slice or
involves governance / parameter drift that is not modeled as a single-transaction harm
channel. The SMT theorem correctly fires, but the verdict stage conservatively rejects the
case because no immediate value sink is reachable within the slice.

| Benchmark | Contract | Triggered Family | Verdict Failure |
|-----------|----------|-----------------|-----------------|
| Sherlock | `2022-10-merit-circle_TimeLockPool` | S1-2 | consequence unreachable in bounded slice |
| Sherlock | `2024-06-leveraged-vaults_WithdrawRequestBase` | S1-2 | view-only path; harm delta not reachable |
| Web3Bugs | `104_Splitter` | S5-3 | no concrete value sink identified |
| Web3Bugs | `192_Position` | S5-3 | no concrete value sink identified |
| DeFiHackLabs | `bsc_AkashaOFT_0xc3B1b45e` | S5-3 | no concrete value sink identified |
| DeFiHackLabs | `bsc_ROIToken_0xe48b75dc` | S5-3 | no concrete path to harm boundary |
| DeFiHackLabs | `eth_PLNTOKEN_0xe0c218e1` | S5-3 | no concrete path to harm boundary |
| DeFiHackLabs | `eth_Token_0x418c2419` | S5-3 | no concrete value sink identified |
| DeFiHackLabs | `eth_TransparentUpgradeableProxy_0xf169bd68` | S5-3 | no concrete value sink identified |

**Pattern.** Seven of the nine cases involve family S5-3 (access-control/privileged-mutation).
In these contracts the privileged function exists and the admission theorem is satisfied, but
the in-scope target slice lacks a direct asset-transfer or state-write path that constitutes
an immediately exploitable harm delta. The two Sherlock cases involve S1-2 (missing output
bound) in which the actual financial harm requires observing the price impact across multiple
transactions rather than in a single atomic call.

### Failure Mode B — Structural mismatch (2 cases)

The retrieval and SMT stages found no satisfying mechanism-report pair for any function in
the contract: all theorem-to-function pairs were UNSAT. No E4 evaluation was attempted.
The root cause is that the contract's vulnerable mechanism does not sufficiently overlap
with the MDL operation vocabulary induced from the training corpus, so no corpus report
reaches the SMT SAT threshold.

| Benchmark | Contract | SMT Result | Note |
|-----------|----------|------------|------|
| Web3Bugs | `52_Synth` | All pairs UNSAT | Vulnerability mechanism not covered by current corpus |
| DeFiHackLabs | `bsc_Token_0xe1747a23` | All pairs UNSAT | Vulnerability mechanism not covered by current corpus |

---

## 2. False Positives (18 cases)

A false positive occurs when a ground-truth SAFE contract receives a VULN verdict.
All 18 FP cases passed the SMT gate and received a positive harm verdict from the verdict
stage. The primary cause is that the mechanism theorem is structurally satisfied by a
legitimate (non-vulnerable) code pattern, and the verdict stage incorrectly infers a harm
path that does not correspond to an actual exploitable vulnerability.

### 2.1 Sherlock (9 cases)

| Contract | Triggered Function(s) | Triggered Family | Attribution |
|----------|-----------------------|-----------------|-------------|
| `2023-01-derby_MainVault` | `rebalance`, `claimTokens` | S1-1 | Price-dependency theorem fires on reward accounting; actual design is intentionally oracle-free |
| `2023-01-derby_Vault` | `setTotalUnderlying`, `rebalance` | S1-1 | Same oracle-free accounting pattern as `MainVault` |
| `2024-01-napier_NapierPool` | `swapUnderlyingForExactBaseLpToken` | S1-2 | Slippage theorem fires; contract enforces bounds at caller level rather than internally |
| `2024-03-wagmileverage-v2_LightQuoterV3` | `calculateExactZapIn` | S1-1 | Valuation-dependency theorem fires on a view function with no state-write path |
| `2024-03-wagmileverage-v2_LiquidityBorrowingManager` | `borrow` | S1-1 | Price-dependency theorem fires; contract uses its own TWAP that the slice does not expose |
| `2024-06-leveraged-vaults_Kelp` | `triggerExtraStep` | L1 | Callback-settlement theorem fires on a governance-guarded function with no user-facing asset path |
| `2024-06-leveraged-vaults_TradingModule` | `executeTrade` | L1 | Callback-settlement theorem fires; actual execution is fully access-controlled |
| `2024-06-velocimeter_Gauge` | `notifyRewardAmount` | S1-1 | Reward-weight theorem fires on admin-only distribution; no user-extractable delta |
| `2024-08-sentiment-v2_PositionManager` | `liquidate` | S1-1 | Price-dependency theorem fires; liquidation pricing is constrained by design |

### 2.2 Web3Bugs (4 cases)

| Contract | Triggered Function(s) | Triggered Family | Attribution |
|----------|-----------------------|-----------------|-------------|
| `13_RCOrderbook` | `addBidToOrderbook`, `removeBidFromOrderbook`, `removeUserFromOrderbook` | S5-3 | Access-control theorem fires on orderbook functions; actual privilege constraint is enforced at the application layer |
| `25_AccessControl` | `renounceRole` | S5-3 | Role-modification theorem fires on a standard `renounceRole` implementation that is intentionally permissionless |
| `61_StrategyRegistry` | `initialize` | S5-3 | Initializer theorem fires; contract is deployed behind a factory that enforces single-call semantics externally |
| `61_adminVerifier` | `initialize` | S5-3 | Same factory-enforced initialization pattern as `StrategyRegistry` |

### 2.3 DeFiHackLabs (5 cases)

| Contract | Triggered Function(s) | Triggered Family | Attribution |
|----------|-----------------------|-----------------|-------------|
| `arbitrum_MixedSwapRouter_0x58637aaa` | `_swap`, `swapTokensForETH` | S1-2 | Slippage theorem fires; router enforces caller-supplied bounds that the slice does not model |
| `bsc_BFCToken_0x595eac4a` | `getUserMintAmount`, `balanceOf` | S1-1 | Share-ratio theorem fires on a read-path function with no downstream state-write |
| `bsc_StakingRewards_0xeaf83465` | `getTokenPrice`, `_buySellc`, `getTokenPriceUs`, `_buy` | S1-1 | Price-dependency theorem fires; internal pricing uses fee-adjusted accounting that the slice exposes only partially |
| `bsc_Token_0x13b1f2e2` | `_burn` | S5-3 | Privileged-mutation theorem fires on `_burn`; function is guarded by `onlyController` with no exploitable escalation path |
| `eth_EHIVE_0x4ae2cd1f` | `_burn` | S5-3 | Same `onlyController`-guarded burn pattern as `bsc_Token_0x13b1f2e2` |

---

## Summary

| Category | Count | Root cause |
|----------|-------|------------|
| FN — harm verdict not confirmed | 9 | Bounded slice lacks direct value sink; multi-block or governance-dependent harm |
| FN — structural mismatch | 2 | Vulnerable mechanism outside current corpus coverage |
| FP — legitimate pattern triggers theorem | 18 | Access-control or slippage constraint enforced at caller/factory level, not visible in target slice |

The FP pattern predominates in S5-3 (access-control family, 9 of 18 FP) and S1-1
(valuation-dependency family, 6 of 18 FP). Both reflect structural theorems that are
intentionally permissive at the SMT gate stage to preserve recall; the verdict stage is the
primary discriminator, and these cases represent its current precision boundary.
