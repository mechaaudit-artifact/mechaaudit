# Mover/Telcoin: reconstructed solver traces

The two calls in the [verifier contrast](../../MOVER_TELCOIN_VERIFIER_CONTRAST.md)
now have complete SMT-LIB, encoder inputs, solver outputs, and provenance.
These traces were reconstructed on 2026-09-26. They are not recovered historical
SMT-LIB files.

**Both results reproduce the historical decisions. The registry route, witness,
and every saved code/proposal alignment field match the historical records
exactly.** No fact or constraint was adjusted to obtain that agreement.

| Sherlock target | Raw SMT-LIB | Reconstructed input | Reconstructed output | Historical output |
|---|---|---|---|---|
| `2022-10-mover_HardenedTopupProxy.initialize` | [499 lines](mover_initialize.smt2) | [all encoder facts](mover_initialize.input.json) | [SAT](mover_initialize.output.json) | [row 46](../mover_initialize.archived.json) |
| `2022-11-telcoin_TieredOwnership.acceptExecutorship` | [326 lines](telcoin_acceptExecutorship.smt2) | [all encoder facts](telcoin_acceptExecutorship.input.json) | [UNSAT](telcoin_acceptExecutorship.output.json) | [row 692](../telcoin_acceptExecutorship.archived.json) |

The saved proposals are available separately for
[Mover](mover_initialize.proposal.json) and
[Telcoin](telcoin_acceptExecutorship.proposal.json).
The [provenance manifest](provenance.json) records source hashes, tool versions,
the complete final formulas, and comparisons against the historical records.

## How the traces were reconstructed

1. Load the saved report/target proposal for each call. Verify the hashes of the
   encoder, PDGs, retrieval records, and historical result file against the
   previously recorded evidence hashes.
2. Run the source encoder's deterministic fact extractor on the existing target
   source and PDG. Compilation occurs in temporary project copies with project
   preparation disabled. No LLM or retrieval stage is rerun.
3. Pass the extracted facts to the unmodified `solve_case` implementation.
   Capture its assertions and export them through Z3's `to_smt2()`.
4. Parse the exported files independently and check their results. Compare
   results, routes, witnesses, and all saved alignment fields to the historical
   records. All comparisons pass for both cases.

The reconstruction used solc 0.8.20, Slither 0.11.5, crytic-compile 0.3.11, and
Z3 4.16.0. The manifest pins the original implementation checkout's commit and
encoder hash. Its `source_files` paths refer to that checkout, not paths in this
public artifact. The only solver instrumentation records assertions and sets a
20-second timeout.
The full reconstructed input was not stored in the historical result rows, so
the agreement claim is limited to the historical fields that were saved.

## What the code facts decide

Both saved proposals contain `template_id=C-S53a` and
`deficiency_kind=missing`. Nevertheless, the caller-guard facts differ.

For Mover, `fn_46_0` denotes `initialize`. Code analysis identifies its public
initialization entry and the call to
`_setupRole(DEFAULT_ADMIN_ROLE, _msgSender())`, with no caller-authorization
guard. The raw formula contains:

```smt2
(assert
 (NoCallerAuthGuard_46 fn_46_0))
```

For Telcoin, `fn_692_0` denotes `acceptExecutorship`. Code analysis finds
`require(_msgSender() == nominatedExecutor())`. The raw formula contains:

```smt2
(assert
 (not (NoCallerAuthGuard_692 fn_692_0)))
```

The LLM's `missing` label did not supply either truth value. It selected a rule
that requires the caller-guard-absence predicate to hold for the entry.

Here is Mover's complete final query, with whitespace expanded for reading:

```smt2
(exists ((w_entry_46 Fn_46) (w_carrier_46 Fn_46) (w_path_46 Path_46))
  (and (IsEntry_46 w_entry_46)
       (EntryAdmissible_46 w_entry_46)
       (PublicOrExternal_46 w_entry_46)
       (NoCallerAuthGuard_46 w_entry_46)
       (PathFromTo_46 w_path_46 w_entry_46 w_carrier_46)
       (WritesNonInitState_46 w_carrier_46)
       (or (ExactAuthorityPrimitive_46 w_carrier_46)
           (WritesCallerGuardState_46 w_carrier_46))
       (InitializerSurface_46 w_entry_46)))
```

It requires a public, admissible initialization entry without caller
authorization, connected to a carrier that changes non-initialization state
and either performs an authority primitive or writes state used by caller
guards. The facts include the role-assignment write reached through
`initialize -> _setupRole -> _grantRole`. The recovered SAT binding is
`entry=initialize`, `carrier=initialize`, `path=[initialize]`, because the
carrier facts include its helper-call closure.

Telcoin uses the non-initializer branch of the same authority rule. Its caller
guard contradicts the required guard absence, so the conjunction is UNSAT. The
complete negative query and fixed facts are in its raw file.

The theory uses finite enumerated datatypes, Boolean-valued predicates,
equality, and quantifiers. An equivalent direct evaluator over these facts and
constraints can return the same decisions. These results establish consistency
with the encoded mechanism conditions, conditional on the proposed rule.

## Check the raw files

```sh
z3 -smt2 mover_initialize.smt2
z3 -smt2 telcoin_acceptExecutorship.smt2
```

Expected outputs are `sat` and `unsat`. The serializer's initial
`(set-info :status unknown)` is metadata, not the result of `check-sat`.
The [Mover model](mover_initialize.model.txt) is the reconstructed Z3 model.
The human-readable witness in the output JSON is recovered by deterministic
enumeration after SAT, as in the encoder, rather than printed as an existential
assignment by Z3. Harm Verdict was not rerun.
