# MDL Primitives Reference

Mechanism Description Language (MDL) represents a vulnerability mechanism as a triple
**M = (Π, C, τ)**, where Π is the operation trace, C is the missing-condition set, and τ is
the adversarial trigger description.

Π and C are the two closed, corpus-validated vocabularies below (Tables 1 and 2): every
`pi_r`/`pi_f` operation and `c_r`/`c_f` condition instance is drawn from one of these fixed
symbol sets, which is what makes structural comparison between a report and a target function
decidable. τ is **not** reduced to a closed vocabulary: `adversarial_trigger` is stored as free
natural-language text per corpus report (see `corpus/corpus_manifest.jsonl`), recording the
auditor-established exploit channel. This is by design: τ is not needed by retrieval, which
compares only Π/C; its role is in Harm Verdict, where the LLM receives `τ_r` as input to
identify the relevant harm category and judges reachability from the target's PDG-grounded
evidence (see `mechaaudit/harm_verdict/harm_verdict.py`). `τ_f = ∅` by construction — static
analysis cannot recover the adversary's access channel from the target alone. τ is
correspondingly absent from the `pi_r`/`pi_f` and `c_r`/`c_f` comparisons below and from
the retrieval-equivalence check that groups findings into mechanism units.

Report-side extraction (from audit findings) and contract-side extraction (from PDG analysis)
project onto the same shared Π/C vocabulary, enabling structural comparison across protocols.

---

## Table 1 — Operation Vocabulary (24 entries)

Induced from 394 audited findings across four mechanism families (L1, S1-1, S1-2, S5-3).

| ID | Operation | Description |
|----|-----------|-------------|
| 1 | `outbound_asset_transfer` | Sending assets to an external address (`transfer`, `send`, `call{value}`) |
| 2 | `nft_safe_interaction` | NFT mint/transfer triggering a receiver callback (`_safeMint`, `safeTransferFrom`) |
| 3 | `cross_contract_state_read` | Reading state from another contract mid-update (read-only reentrancy) |
| 4 | `share_ratio_computation` | Computing shares/assets ratio where denominator can be near zero |
| 5 | `spot_price_read` | Reading price from a manipulable source (AMM reserves, `slot0`, `balanceOf`) |
| 6 | `oracle_window_read` | Reading price from a time-windowed oracle (`TWAP`, `exchangeRateStored`) |
| 7 | `direct_balance_dependency` | Contract accounting depends directly on `balanceOf(this)` (donation attack surface) |
| 8 | `reward_weight_computation` | Computing stake weight or reward base from a manipulable input |
| 9 | `exchange_execution` | Swap/liquidity operation requiring price-time boundary protection |
| 10 | `asset_value_operation` | Non-swap asset operation whose output depends on external price (vault deposit/mint/redeem) |
| 11 | `role_assignment` | Assigning an admin/owner role during initialization |
| 12 | `privileged_state_mutation` | Modifying protocol parameters or critical state (`setRate`, `pause`, `rescue`) |
| 13 | `protocol_internal_call` | Function intended to be called only by specific protocol components (e.g. `onlyRouter` target) |
| 14 | `role_modification` | Changing role assignments or permission delegation |
| 15 | `delegated_action` | Operating on behalf of another user (`transferFrom`, `withdraw-for`, `claim-for`) |
| 16 | `asset_withdrawal` | User withdrawing assets from protocol (`withdraw`, `redeem`, `repay`) |
| 17 | `asset_deposit` | User depositing assets into protocol (`deposit`, `supply`, `stake`) |
| 18 | `reward_claim` | Claiming rewards or earnings (`claim`, `distribute`, `harvest`) |
| 19 | `asset_swap` | Exchanging one asset for another (`swap`, `trade`) |
| 20 | `token_mint` | Minting tokens or NFTs |
| 21 | `settlement` | Settling/finalizing an order or auction |
| 22 | `governance_execute` | Governance or batch execution (`DAO.execute`, multisig) |
| 23 | `lending_operation` | Lending/borrowing operations (`lend`, `borrow`, `repay`) |
| 24 | `none_applicable` | Step describes attacker behavior rather than a code-observable operation — skip |

---

## Table 2 — Condition Templates (17 entries)

Induced from the `missing_what` fields of 394 audited findings. Templates are orthogonal to
mechanism families: the same template can appear across L1, S1-1, S1-2, and S5-3 findings.
The ID prefix (C-L1*, C-S11*, etc.) indicates the induction source, not a type restriction.

| ID | Name | Description | Predicates |
|----|------|-------------|------------|
| C-L1a | `reentrancy_guard` | Missing `nonReentrant` modifier or equivalent reentrancy protection | `guard(nonReentrant)` |
| C-L1b | `CEI_pattern` | Not following Checks-Effects-Interactions (external call before state update) | `pattern(CEI)` |
| C-L1c | `state_update_before_call` | Specific state variable not updated before external call (concrete CEI instance) | `pattern(CEI)` |
| C-L1d | `cross_scope_reentrancy` | Missing cross-function or cross-contract reentrancy protection | `guard(nonReentrant)` |
| C-S11a | `manipulation_resistant_price` | Price/rate from manipulable source (AMM spot/reserves/`balanceOf`) without TWAP/oracle | `invariant(price_manipulation)`, `check(oracle_freshness)` |
| C-S11b | `first_depositor_protection` | Missing minimum shares/liquidity check allowing inflation when `totalSupply` is near zero | `check(totalSupply > minimum)`, `pattern(virtual_offset)` |
| C-S11c | `flash_loan_protection` | Missing protection against flash-loan-induced price/state distortion | `invariant(price_manipulation)`, `invariant(checkpoint_time_separation)` |
| C-S11d | `exchange_rate_validation` | Exchange rate or reserve ratio not validated for a reasonable range | `invariant(price_manipulation)` |
| C-S12a | `slippage_protection` | Swap/liquidity operation missing minimum output amount check | `check(cost_bound)` |
| C-S12b | `deadline_protection` | Transaction missing a validity time limit (deadline/timeout) | `check(deadline)` |
| C-S12c | `dynamic_slippage` | Slippage parameter hardcoded or improperly calculated (e.g. ignoring fees) | `check(cost_bound)` |
| C-S12d | `actual_amount_verification` | Missing balance before/after check to verify actual received amount | `check(balance_before_after)` |
| C-S53a | `admin_access_control` | Sensitive function missing admin/owner/role-based access control | `check(msg.sender == onlyOwner)`, `check(msg.sender == protocol_role)` |
| C-S53b | `ownership_verification` | Operation not verifying that the caller is the asset owner | `check(msg.sender == onlyOwner)` |
| C-S53c | `role_specific_gate` | Missing role-specific modifier (`onlyRouter`/`onlyBorrower`/`onlyLender`, etc.) | `check(msg.sender == protocol_role)` |
| C-S53d | `approval_delegation_check` | Not verifying that the caller has approval/delegation for the operation | `check(msg.sender == protocol_role)` |
| C-S53e | `initializer_guard` | Initialize function missing re-initialization protection | `guard(initializer)`, `check(msg.sender == trusted_deployer)` |

---

## Core Operations per Sub-direction

The table below lists the mechanism-essential operations for each sub-direction.
Matching requires that at least one CORE operation be present on both the report side
and the contract side. Note that CORE assignments are per sub-direction, not per operation:
the same operation (e.g. `outbound_asset_transfer`) can be CORE in one sub-direction and
AUX in another.

| Sub-direction | CORE Operation(s) |
|---------------|-------------------|
| L1 — callback state finalization | `outbound_asset_transfer` |
| L1 — NFT receiver callback | `nft_safe_interaction` |
| L1 — read-only reentrancy | `cross_contract_state_read` |
| S1-1 — bootstrap share inflation | `share_ratio_computation` |
| S1-1 — reserve direct manipulation | `spot_price_read` |
| S1-1 — market-derived oracle window | `oracle_window_read` |
| S1-1 — share/total-assets distortion | `direct_balance_dependency` |
| S1-1 — stake weight / reward base | `reward_weight_computation` |
| S1-2 — disabled price-time boundary | `exchange_execution` |
| S1-2 — hardcoded slippage threshold | `exchange_execution` |
| S1-2 — missing min guard on asset op | `asset_value_operation` |
| S5-3 — initializer admin capture | `role_assignment` |
| S5-3 — missing gate on privileged op | `privileged_state_mutation` |
| S5-3 — missing trusted-caller auth | `protocol_internal_call` |
| S5-3 — role self-escalation | `role_modification` |
| S5-3 — privileged auth bypass | `delegated_action` |
