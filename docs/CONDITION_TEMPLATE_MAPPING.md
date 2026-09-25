# Condition templates: families, operation flows, and source findings

This table connects **all 17 condition templates** to a vulnerability-family context,
the concrete operation flow, the required protection and its reported deficiency,
and a representative audit finding from the existing 394-finding corpus.

The templates describe missing or ineffective protections. During offline corpus
construction, missing-protection descriptions were grouped with LLM assistance and
reviewed for semantic consistency; extracted report representations were inspected
before admission. The existing [template definitions](MDL_PRIMITIVES.md#table-2--condition-templates-17-entries)
give the shared predicates. The table below makes their source-finding correspondence
explicit.

**How to read the table.** The family column is the family of the cited finding, not
an exclusive applicability restriction. A template can be reused across families,
and one finding can instantiate multiple templates. Arrows summarize the cited
finding's causal/operation flow; they are explanatory summaries, not newly generated
solver traces. Report IDs follow the existing corpus identifiers; the links open
the original public findings.

This is a **source-documentation table**, not an additional detection stage or
retrieval input. Concrete function and variable names identify the cited reports;
the arrows are readable report summaries, not serialized MDL operation lists.
The linked JSON is a documentation sidecar: neither it nor this table is loaded
by the detector. Existing corpus records and evaluation inputs are unchanged.

| Template | Family of representative finding | Operation flow in the finding | Required protection and reported deficiency | Representative finding |
|---|---|---|---|---|
| `C-L1a` — reentrancy guard | Reentrancy | MarginRouter swap entry → external pair call → re-entry → trade output credited twice. | A reentrancy guard covering the external swap entry. **Deficiency:** The swap entry permits re-entry during the pair call. | [2021-04-marginswap/H-01](https://github.com/code-423n4/2021-04-marginswap-findings/issues/19) |
| `C-L1b` — CEI pattern | Reentrancy | Withdrawal → external reward-token transfer → internal withdrawal accounting update. | Commit accounting effects before external interaction (CEI). **Deficiency:** The external transfer precedes the accounting update. | [2021-11-malt/M-06](https://github.com/code-423n4/2021-11-malt-findings/issues/333) |
| `C-L1c` — state update before call | Reentrancy | `_withdraw` → `safeTransfer` callback → `earned` reads stale `_userWithdrawn`. | Update `_userWithdrawn[account]` before transferring the reward. **Deficiency:** This specific balance/accounting field remains stale during the callback. | [2021-11-malt/M-06](https://github.com/code-423n4/2021-11-malt-findings/issues/333) |
| `C-L1d` — cross scope reentrancy | Reentrancy | `lend` → caller callback → access to other functions before claims/reserves are updated. | Protection across the affected function scope, or completion of shared-state updates before callback. **Deficiency:** The reported lock does not protect against cross-function reentrancy. | [2022-01-timeswap/H-05](https://github.com/code-423n4/2022-01-timeswap-findings/issues/5) |
| `C-S11a` — manipulation resistant price | Asset valuation manipulation | Manipulated pool price → `DAO.bond` valuation → DAO commits matching BASE liquidity. | Validate the valuation against a manipulation-resistant reference, such as a TWAP. **Deficiency:** The matching BASE allocation follows a manipulable pool price. | [2021-07-spartan/M-14](https://github.com/code-423n4/2021-07-spartan-findings/issues/178) |
| `C-S11b` — first depositor protection | Asset valuation manipulation | Minimal first deposit → donation to strategy controller → inflated share price → later deposit mints zero shares. | Initial minimum-liquidity protection and a nonzero-share check. **Deficiency:** The first depositor can inflate the ratio without these protections. | [2022-03-prepo/H-02](https://github.com/code-423n4/2022-03-prepo-findings/issues/27) |
| `C-S11c` — flash loan protection | Asset valuation manipulation | Flash-loan reserve change → price-feed update when its update window permits → borrowing/liquidation consumes the price. | A valuation input resistant to temporary reserve manipulation, such as a TWAP. **Deficiency:** Reserve manipulation can determine the price when an update is permitted. | [2021-04-marginswap/H-03](https://github.com/code-423n4/2021-04-marginswap-findings/issues/21) |
| `C-S11d` — exchange rate validation | Asset valuation manipulation | Reserve manipulation → synth mint at distorted exchange rate → reverse manipulation → synth redemption. | Validate or anchor the mint/redemption exchange rate to a manipulation-resistant reference. **Deficiency:** The exchange rate used for synth valuation is accepted from manipulated reserves. | [2021-11-vader/H-02](https://github.com/code-423n4/2021-11-vader-findings/issues/3) |
| `C-S12a` — slippage protection | Slippage/sandwich | `withdrawAll` → Curve swap without an effective minimum return → sandwich exposure. | An enforced minimum output/cost bound on the swap. **Deficiency:** The swap does not specify an effective minimum return amount. | [2021-09-yaxis/M-06](https://github.com/code-423n4/2021-09-yaxis-findings/issues/7) |
| `C-S12b` — deadline protection | Slippage/sandwich | Join/exit request with a deadline → external swap receives `block.timestamp` instead. | Propagate and enforce the request's intended expiration time. **Deficiency:** Substituting the execution timestamp discards the supplied time limit. | [2021-12-amun/M-06](https://github.com/code-423n4/2021-12-amun-findings/issues/47) |
| `C-S12c` — dynamic slippage | Slippage/sandwich | `calc_token_amount` quote → additional slippage subtraction → `add_liquidity` minimum. | A correctly derived minimum that accounts for what the quote already includes. **Deficiency:** The bound applies an additional slippage deduction to a quote that already reflects slippage. | [2022-02-redacted-cartel/M-05](https://github.com/code-423n4/2022-02-redacted-cartel-findings/issues/35) |
| `C-S12d` — actual amount verification | Slippage/sandwich | Check `finalOutputAmount` → transfer fee-charging token → user can receive less than `finalAmountMin`. | Check the recipient's actual balance increase after transfer. **Deficiency:** The minimum is checked before the transfer fee reduces the received amount. | [2021-10-slingshot/M-02](https://github.com/code-423n4/2021-10-slingshot-findings/issues/77) |
| `C-S53a` — admin access control | Missing access control | Unauthorized repeated `liquidate` calls → maintainer failure counter increases → attacker obtains payouts. | Authorization for the sensitive liquidation action. **Deficiency:** Unrestricted calls can trigger the maintainer punishment/payout path. | [2021-04-marginswap/M-04](https://github.com/code-423n4/2021-04-marginswap-findings/issues/5) |
| `C-S53b` — ownership verification | Missing access control | `offerWithETH` records the router as owner → another caller invokes `cancelForETH` → refund. | Track the initiating user and verify ownership when cancelling. **Deficiency:** Cancellation does not bind the caller to the offer's actual user owner. | [2022-05-rubicon/H-01](https://github.com/code-423n4/2022-05-rubicon-findings/issues/17) |
| `C-S53c` — role specific gate | Missing access control | Direct `BasePool.mint` call → bypass router-side input validation → mint. | Restrict the pool entry to the trusted router (`onlyRouter`). **Deficiency:** The pool entry omits the router-specific gate. | [2021-11-vader/M-13](https://github.com/code-423n4/2021-11-vader-findings/issues/148) |
| `C-S53d` — approval delegation check | Missing access control | `retrieveFromStrategy(from=victim)` → cross-chain message → `strategyWithdraw` processes victim's position. | Validate the initiating caller's approval/delegation for the supplied `from` account. **Deficiency:** The request reaches the withdrawal path without that approval check. | [2023-07-tapioca/H-34](https://github.com/code-423n4/2023-07-tapioca-findings/issues/1032) |
| `C-S53e` — initializer guard | Missing access control | Owner calls `initialize` again → core collection variables are reset. | A one-time initialization guard, in addition to caller authorization. **Deficiency:** `onlyOwner` exists, but the initialized flag is not checked to prevent another run. | [2022-03-joyn/H-04](https://github.com/code-423n4/2022-03-joyn-findings/issues/4) |

## Coverage and traceability

The source corpus contains 394 findings from 2021–2025: 96 reentrancy,
72 asset valuation manipulation, 101 slippage/sandwich, and 125 missing access
control findings. It was selected from 4,709 Code4rena findings by family
classification and manual verification. These counts describe the corpus, not
disjoint subsets defined by the 17 templates.

Each row above has both a recorded template assignment and a source finding in
that corpus. This supports the templates' origin and their use in the four studied
families; it does not establish exhaustive coverage of every case in those families.
Additional reports can be processed using the same construction and review steps
to extend the vocabulary when new missing-protection semantics are encountered.

The [machine-readable examples](../corpus/template_examples.json) retain the
archived condition instances, their validation notes, the conditions already
published in [the original corpus manifest](../corpus/corpus_manifest.jsonl), and
the original finding links. The two Malt rows deliberately share a source: the
general CEI violation and the specific stale-accounting condition are related
templates, not two independent findings. Similarly, the Joyn example distinguishes
a missing one-time initialization check from its existing owner check.

## Reading the source records

The JSON preserves two distinct archived representations: the conditions in the
original public manifest and normalized instances with explicit template IDs.
They need not use identical wording or granularity. They are retained as recorded,
rather than rewritten to match the explanatory table. `template_predicates` lists
the template's associated vocabulary; it does not assert that every listed
predicate is absent in each example. In particular:

- **Timeswap (`C-L1d`):** the manifest describes callback-before-update ordering;
  the normalized instance records cross-function protection. The original finding
  discusses both and explicitly acknowledges an existing local lock.
- **Redacted Cartel (`C-S12c`):** a minimum-output check exists but is incorrectly
  calculated. The manifest records a weak check; the normalized instance uses
  `deficiency_kind: missing`. The table describes the missing *effective* bound,
  not absence of all checking code.
- **Vader (`C-S53c`):** the normalized slot names `addLiquidity`, while the public
  finding locates the missing `onlyRouter` gate at `BasePool.mint`. The former is
  the intended router operation whose validation the direct pool call bypasses.
  The table names the actual unguarded entry.
- **Tapioca (`C-S53d`):** the original report follows an unauthorized initiating
  caller through message delivery to `strategyWithdraw`. This is a corpus example
  of missing delegation checks, not an evaluation of MechaAudit's cross-chain
  execution analysis.
- **Report identifiers:** corpus IDs are stable identifiers, not a restatement
  of current issue titles or severity. For example, the linked Tapioca issue has
  an `HF06` title and the Joyn issue discusses medium severity; their archived
  corpus IDs remain `H-34` and `H-04` respectively.

For corpus selection, vocabulary construction, and the role of human review, see
[Corpus construction and provenance](CORPUS_CONSTRUCTION.md). The detailed table
and source records are supplied here because a page-limited paper cannot reproduce
all of them; they supplement the paper's method description.

Documentation supplement added on 2026-09-25. The table consolidates existing
definitions and report records; it does not change the corpus, benchmark labels,
detector, or reported experimental results.
