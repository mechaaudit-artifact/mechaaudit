# AutoRoller three-stage trace

This page is the single running example for the paper's Figure 2 and the
requested three-stage presentation. It is provided for the presentation and
transparency concern: the same target case is followed from retrieval and MDL
through registry admission, SMT, and Harm Verdict. The Mover/Telcoin cases are
not part of this page; they are documented separately for the verifier
independence question.

The [solver evidence supplement](solver_evidence/README.md) provides complete
raw SMT-LIB, inputs, outputs, and provenance for a separate archived AutoRoller
`previewDeposit` check and an ERC4626 control. That archived-fact replay uses
the `bootstrap_share_inflation` route. The final `deposit` trace below uses
`share_ratio_dependency`, and its result should not be confused with that replay.

## AutoRoller.deposit: the paper running example

The paper's motivating example uses `2022-11-sense_AutoRoller`. Figure 1
(`mechanism-compare`) shows its share-ratio code beside the Hubble H-03 finding;
Figure 2 (`mdl-example`) shows the corresponding target-side and corpus-side
MDL representations. The Hubble finding is the explanatory source example in
the figures. In the final evaluation replay, the retrieved report for the same
AutoRoller target is `2022-03-prepo/H-02`; the trace below reports that actual
evaluation record rather than silently substituting the figure's Hubble text.

### Retrieval and MDL correspondence

The final Sherlock benchmark labels `2022-11-sense_AutoRoller` VULN. The target
is its `deposit` function in unit `U002`. The selected report
`2022-03-prepo/H-02` is rank 0 and passes the type, operation, condition, and
trigger gates. Its shared core operations are `asset_deposit` and
`share_ratio_computation`. The target condition record is:

```json
{
  "template_id": "C-S11b",
  "protected_action_kind": "valuation_dependent_decision",
  "protected_object_kind": "valuation_input",
  "deficiency_kind": "missing",
  "slots": {
    "protected_action": "previewDeposit",
    "source_kind": "share_ratio",
    "value_anchor": "initial totalSupply / totalAssets not seeded"
  }
}
```

The surface entry used by the target-side mechanism unit is `deposit`; the
retrieved route is `b2_attacker_movable_measurement`, variant
`share_ratio_dependency`.

### Concrete code facts

The relevant target code is:

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
    // cooldown branch omitted
}
```

The archived code-side facts include a zero-supply branch in `deposit`,
`previewDeposit`, and `convertToShares`; a raw `balanceOf(address(this))` carrier
in `deposit`, `convertToShares`, and `totalAssets`; and the connected transfer
and mint sinks. The existing `ZERO_SHARES` check is not the same as seeding the
initial supply or preventing an external balance donation from changing the
share ratio. The Harm Verdict therefore evaluates the reported share-ratio
obligation against these connected sinks rather than treating the SAT result as
a complete economic proof.

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
`entry=deposit`, `carrier=deposit`, and `path=[deposit]`.

The adopted final output records Severity, Necessity, and Feasibility as true.
Its evidence references include `deposit`, `previewDeposit`, `_mint`,
`SafeTransferLib.safeTransferFrom`, `BalancerVault.getPoolTokens`, and
`DividerLike.issue`. This is the complete Figure-2-to-pipeline trace: the
figure's mechanism abstraction is instantiated by a real target function and
then carried through registry admission and the three Harm Verdict checks.

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
facts or the solver result. The full paper cannot print the complete solver dump,
but this page exposes the target functions, the relevant registry clause keys,
the archived binding, and the downstream decision.
