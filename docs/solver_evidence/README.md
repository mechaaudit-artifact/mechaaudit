# Solver inputs, outputs, and provenance

This supplement makes the saved solver evidence available as files. It separates
historical evaluation results from SMT-LIB exported during an already completed
fact replay. Publishing these files does not introduce a new detection experiment.

## Historical authority-check contrast

The [Mover/Telcoin case study](../MOVER_TELCOIN_VERIFIER_CONTRAST.md) explains how
code facts accept or reject the proposed missing protection.

| Sherlock case | Function | Historical solver result | Saved evidence |
|---|---|---|---|
| `2022-10-mover_HardenedTopupProxy` | `initialize` | SAT | [proposal, code facts, binding, and Harm output](mover_initialize.archived.json) |
| `2022-11-telcoin_TieredOwnership` | `acceptExecutorship` | UNSAT | [proposal, code facts, and rejection](telcoin_acceptExecutorship.archived.json) |

The records come from rows 46 and 692 (zero-based) of the historical solver log.
Their `solver_result` and `witness` fields are copied unchanged. The witness is
recovered by deterministic code after SAT, rather than a printed Z3 assignment.
No complete historical SMT-LIB text was located for these two calls. These JSON
records are not represented as raw SMT-LIB dumps.

## Complete SMT-LIB from an archived-fact replay

The following complete files were exported on 2026-09-24 from a replay of saved
function/path facts using the source encoder. The recorded replay used Z3 4.16.0
and reproduced the archived SAT/UNSAT decisions. It made no LLM calls and did not
re-extract code facts. Older fact records lacked fields for unrelated predicates.
The exact default additions are listed in [provenance](provenance.json).

| Case and entry | Raw SMT-LIB | Encoder input | Historical record | Replay output |
|---|---|---|---|---|
| `2022-11-sense_AutoRoller.previewDeposit` | [SMT-LIB](autoroller_previewDeposit.smt2) | [facts](autoroller_previewDeposit.input.json) | [SAT](autoroller_previewDeposit.archived.json) | [SAT](autoroller_previewDeposit.output.json) |
| `2022-10-rage-trade_ERC4626Upgradeable.deposit` | [SMT-LIB](erc4626_deposit_control.smt2) | [facts](erc4626_deposit_control.input.json) | [UNSAT](erc4626_deposit_control.archived.json) | [UNSAT](erc4626_deposit_control.output.json) |

These two calls use `C-S11b`, the `bootstrap_share_inflation` route. They are
separate from the authority-check contrast above. The AutoRoller call here is
also distinct from the final `deposit` / `share_ratio_dependency` call in the
[three-stage running example](../AUTOROLLER_THREE_STAGE_TRACE.md).

The theory comprises finite enumerated datatypes, Boolean-valued predicates,
equality, and quantifiers. It does not encode symbolic Solidity arithmetic or
an entire execution trace. For AutoRoller, the complete final query in the raw
SMT-LIB is:

```smt2
(exists ((w_entry_5 Fn_5) (w_carrier_5 Fn_5) (w_path_5 Path_5))
  (and (IsEntry_5 w_entry_5)
       (EntryAdmissible_5 w_entry_5)
       (PublicOrExternal_5 w_entry_5)
       (PathFromTo_5 w_path_5 w_entry_5 w_carrier_5)
       (ZeroSupplyBranch_5 w_carrier_5)
       (RawBalanceOfSelf_5 w_carrier_5)))
```

The saved input explains each predicate: the entry is `previewDeposit`, and
the carrier `convertToShares` has both the `supply == 0` branch and a resolved
dependency on `asset.balanceOf(address(this))`. The enumerated path connects
`previewDeposit` to `convertToShares`. The conjunction asks for one consistent
entry/carrier/path combination with both code facts. The recorded witness is
that pair and path. An equivalent evaluator over the same finite facts can
return the same decision.

To check the complete exported formulas with Z3:

```sh
z3 -smt2 autoroller_previewDeposit.smt2
z3 -smt2 erc4626_deposit_control.smt2
```

Expected outputs are `sat` and `unsat`. The raw files include all declarations,
fixed facts, the final query, and `check-sat`. The [provenance manifest](provenance.json)
records source hashes, file hashes, the replay date, and the distinction between
historical outputs and replay outputs. Replay timings are not evaluation-wide
solver runtimes.
