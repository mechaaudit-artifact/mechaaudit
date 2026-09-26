# AutoRoller three-stage trace

This page follows the AutoRoller target used in Figures 1–2 through the adopted
evaluation's retrieval, Mechanism Satisfiability, and Harm Verdict records.
The [archived three-stage record](solver_evidence/autoroller_deposit.archived.json)
provides the selected report, code context, solver result, downstream input,
clause-level verdicts, and source hashes. No stage was rerun for this page.

## AutoRoller.deposit: the paper running example

The paper's motivating example uses `2022-11-sense_AutoRoller`. Figure 1
(`mechanism-compare`) shows its share-ratio code beside the Hubble H-03 finding;
Figure 2 (`mdl-example`) shows the corresponding target-side and corpus-side
MDL representations. The Hubble finding is the explanatory source example in
the figures. In the final evaluation replay, the retrieved report for the same
AutoRoller target is `2022-03-prepo/H-02`. This is a trace of the same target
contract, with the report actually selected in the evaluation.

### Retrieval and MDL correspondence

The final Sherlock benchmark labels `2022-11-sense_AutoRoller` VULN. The target
is its `deposit` function in unit `U002`. The selected report
`2022-03-prepo/H-02` is rank 0 and passes the type, operation, condition, and
trigger gates. Its shared core operations are `asset_deposit` and
`share_ratio_computation`. The archived Sherlock configuration retained top-5
reports per member, separately from the top-15 retrieval-quality evaluation.
The target condition record is:

```json
{
  "template_id": "C-S11b",
  "protected_action_kind": "valuation_dependent_decision",
  "protected_object_kind": "valuation_input",
  "deficiency_kind": "missing",
  "slots": {
    "protected_action": "previewDeposit",
    "source_kind": "share_ratio",
    "carrier_kind": "direct",
    "value_anchor": "initial totalSupply / totalAssets not seeded"
  }
}
```

The surface entry used by the target-side mechanism unit is `deposit`. The
retrieved route is `b2_attacker_movable_measurement`, variant
`share_ratio_dependency`. This is the encoder's internal valuation-rule name,
corresponding to the asset-valuation category in Table II (a2). It is not the
paper registry's b2, which denotes delegated asset root action.

### Concrete code facts

The relevant code excerpts are below. `deposit` and `convertToShares` are
inherited from Solmate ERC4626, while AutoRoller overrides `totalAssets` and
`previewDeposit`. Signatures are shortened and the deposit event is omitted.

```solidity
function deposit(uint256 assets, address receiver)
    public returns (uint256 shares)
{
    require((shares = previewDeposit(assets)) != 0, "ZERO_SHARES");
    asset.safeTransferFrom(msg.sender, address(this), assets);
    _mint(receiver, shares);
    afterDeposit(assets, shares);
}

function convertToShares(uint256 assets) public view returns (uint256) {
    uint256 supply = totalSupply;
    return supply == 0 ? assets : assets.mulDivDown(supply, totalAssets());
}

function totalAssets() public view returns (uint256) {
    if (maturity == MATURITY_NOT_SET)
        return asset.balanceOf(address(this));
    // active-series branch omitted
}
```

The archived code-side facts include a zero-supply branch reachable from `deposit`,
`previewDeposit`, and `convertToShares`; a raw `balanceOf(address(this))` carrier
in `deposit`, `convertToShares`, and `totalAssets`; and the connected transfer
and mint sinks. In the cooldown branch, `previewDeposit` delegates to the inherited
share conversion. **The actual `ZERO_SHARES` check blocks a transfer that would
mint zero shares.** It does not seed the initial supply or prevent donations from
changing the share ratio. The trace records the pipeline's judgment of that
share-ratio dependency, not a successful zero-share-transfer exploit. The revised
running example must preserve this existing check.

### Registry constraint, SAT binding, and Harm Verdict

For this final route, the actual encoder clause keys are:

```python
["entry_is_entry", "entry_admissible", "entry_public",
 "path_entry_to_carrier", "carrier_share_ratio_source"]
```

Equivalently, the reduced formula is:

```text
exists entry, carrier, path:
    Entry(entry)
  and EntryAdmissible(entry)
  and PublicOrExternal(entry)
  and PathFromTo(path, entry, carrier)
  and ShareRatioSource(carrier)
```

`ShareRatioSource(carrier)` is true because the deterministic code facts connect
`deposit -> previewDeposit -> convertToShares -> totalAssets` and identify the
share-ratio reads. The archived SMT result is `sat` with
`entry=deposit`, `carrier=deposit`, and `path=[deposit]`. The carrier facts include
reachable helper code. This binding is not a four-function solver witness.

The adopted final output records Severity, Necessity, and Feasibility as true.
Its evidence references include `deposit`, `previewDeposit`, `_mint`,
`SafeTransferLib.safeTransferFrom`, `BalancerVault.getPoolTokens`, and
`DividerLike.issue`. These are the archived model judgments and evidence
references. The linked record preserves them as produced, including the
Necessity clause's reference to the existing `ZERO_SHARES` check.

For archival cross-checking, the input identifier is
`2022-11-sense_AutoRoller::2022-11-sense_AutoRoller::U002::deposit::2022-03-prepo/H-02`.
The adopted output is line 191 of the long-fix rerun; the corresponding SMT
replay record is row 321 (zero-based) of the final mechanism-unit replay.


## Field provenance

| Item | Source of the value |
|---|---|
| Report type, operation and condition proposal | LLM-assisted corpus representation and retrieval record |
| Entry/carrier/path candidates and code-side facts | Deterministic target-code/PDG extraction |
| Joint satisfiability (`sat`) | SMT solver over the finite encoded facts and registry rule |
| Severity, Necessity, Feasibility | Harm Verdict LLM chain, run only after admission |

`C_f` selects the obligation to check. It does not directly set the target-code
facts or the solver result. This page supplies the archived `deposit` trace and
its encoder clause, not a recovered raw SMT-LIB dump for that call. Complete raw
SMT-LIB is available for the separate
[Mover/Telcoin verifier contrast](MOVER_TELCOIN_VERIFIER_CONTRAST.md).

The [additional historical share-ratio checks](solver_evidence/README.md#complete-smt-lib-from-an-archived-fact-replay)
include an earlier AutoRoller `previewDeposit` call. That different
`bootstrap_share_inflation` route is not the `deposit` call documented here.
