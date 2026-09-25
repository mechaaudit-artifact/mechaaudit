# Complete case trace: retrieval, code facts, SMT admission, and Harm Verdict

This document supplies one complete archived trace that is too long for the
paper. It is intended to make the connection between a retrieved finding, its
condition instance, the target-code facts, the theorem-registry rule, the SMT
admission result, and the final Harm Verdict inspectable.

The records below are from the final Sherlock evaluation input/output chain. No
benchmark label is used by retrieval or admission. The archived trace is
identified by the target case and report IDs; the code excerpts are the target
contract functions used to derive the code-side facts.

## 1. Paper running example: `AutoRoller.deposit`

The paper's motivating example uses `2022-11-sense_AutoRoller`. Figure 1
(`mechanism-compare`) shows its share-ratio code beside the Hubble H-03 finding;
Figure 2 (`mdl-example`) shows the corresponding target-side and corpus-side
MDL representations. The Hubble finding is the explanatory source example in
the figures. In the final evaluation replay, the retrieved report for the same
AutoRoller target is `2022-03-prepo/H-02`; the trace below reports that actual
evaluation record rather than silently substituting the figure's Hubble text.

### Retrieval and MDL correspondence

The target is `2022-11-sense_AutoRoller.deposit` in unit `U002`. The selected
report `2022-03-prepo/H-02` is rank 0 and passes the type, operation, condition,
and trigger gates. Its shared core operations are `asset_deposit` and
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

## 2. Positive contrast for A: `HardenedTopupProxy.initialize`

Target case: `2022-10-mover_HardenedTopupProxy` (benchmark label VULN).
The associated audit report is `2021-08-notional/H-08`, titled “DOS by
Frontrunning NoteERC20 initialize() Function”. The report is the second ranked
candidate for this target unit (`report_rank=1`), and the retrieval gate passes.

### Retrieved condition and registry route

The target condition record is:

```json
{
  "template_id": "C-S53a",
  "protected_action_kind": "authority_assignment",
  "protected_object_kind": "caller_authority",
  "deficiency_kind": "missing",
  "slots": {
    "authority_basis": "initializer_once",
    "protected_action": "initialize"
  }
}
```

The shared report/target operation is `role_assignment`; the target also has a
privileged-state mutation. The archived route is the authority-handoff /
escalation rule, initializer-entry variant. In the paper's notation this is
the privilege-escalation rule (Table II, a5). The report type, operation and
condition guide the route; they do not assert that the target code has the
reported missing protection.

### Target code and independently extracted facts

The target entry is:

```solidity
function initialize(uint _chainId, bytes memory _chainIdRLP)
    public initializer
{
    _setupRole(DEFAULT_ADMIN_ROLE, _msgSender());
    CHAIN_ID = _chainId;
    CHAIN_ID_RLP = _chainIdRLP;
    // ...
}
```

The helper chain reaches the state write:

```solidity
_roles[role].members[account] = true;
```

The code-side extractor therefore records a public initialization entry, no
caller-identity authorization guard, and an authority-state write reachable
from the entry (`initialize -> _setupRole -> _grantRole`). The `initializer`
modifier limits repeated initialization; it does not identify an authorized
first caller. Thus a first successful caller can obtain the administrator role.

### Reduced form of the actual admission constraint

The production encoder constructs a finite-function/finite-path formula. Omitting
datatype declarations and fixed facts, the following is the relevant logical
conjunction (the atom names are the encoder's semantic names; the exact source
clause keys are shown immediately below):

```text
exists entry, carrier, path:
    Entry(entry)
  and PublicOrExternal(entry)
  and InitializerEntry(entry)
  and NoCallerAuthGuard(entry)
  and PathFrom(entry, carrier, path)
  and WritesNonInitializationState(carrier)
  and (ExactAuthorityWrite(carrier)
       or WritesCallerGuardState(carrier))
```

Here `NoCallerAuthGuard(entry)` is populated from the code-side fact, not from
`deficiency_kind=missing`. The real encoder uses the corresponding finite
enumeration constants and Boolean atoms, then calls `solver.check()`.

The code-to-formula connection is explicit in the encoder. For the caller-guard
atom it adds the opposite Boolean fact when the code extractor finds a guard:

```python
if not ff.auth_guard_present:
    solver.add(NoCallerAuthGuard(fn_const))
else:
    solver.add(Not(NoCallerAuthGuard(fn_const)))
```

The authority-handoff rule requires these atoms:

```python
["entry_is_entry", "entry_admissible", "entry_public",
 "entry_no_caller_auth", "path_entry_to_carrier",
 "carrier_writes_non_init", "carrier_authority_state_mutation"]
```

Thus the `missing` label in the retrieved condition selects
`entry_no_caller_auth` as a required test; it cannot make that atom true.

The archived solver record binds `entry=initialize`, `carrier=initialize`, and
`path=[initialize]`, and returns `sat`. The helper calls are part of the
code-fact closure used for the entry; the stored witness is not a claim that
Z3 printed a three-function model.

For archival cross-checking, the positive input identifier is
`2022-10-mover_HardenedTopupProxy::2022-10-mover_HardenedTopupProxy::U001::initialize::2021-08-notional/H-08`.
The SAT record is row 46 (zero-based) of the archived SMT replay, and the
adopted final output is line 32 of the long-fix rerun.

### Harm Verdict

The accepted candidate is passed to the serial Severity/Necessity/Feasibility
chain. The archived final output records all three as true and
`e4c.applicable=true`: the caller can acquire administrator authority through
the public initialization path, the missing caller authorization is necessary
to the reported issue, and the path is triggerable under its initialization
precondition.

## 3. Negative contrast: `TieredOwnership.acceptExecutorship`

Target case: `2022-11-telcoin_TieredOwnership` (benchmark label SAFE). The
retrieved report is `2021-05-yield/M-07`, ranked first, and its retrieval gate
also passes. Its archived condition record uses the same high-level authority
handoff rule and also says `deficiency_kind=missing`.

The target function is:

```solidity
function acceptExecutorship() external {
    require(
        _msgSender() == nominatedExecutor(),
        "TieredOwnership: You must be nominated before you can accept executorship"
    );
    emit ExecutorChanged(executor(), nominatedExecutor());
    _executor = nominatedExecutor();
    _nominatedExecutor = address(0);
}
```

The code-side extractor finds both an authority-state write and a caller
identity guard. Consequently `NoCallerAuthGuard(entry)` is false, the same
joint rule is `unsat`, and the candidate has no downstream Harm Verdict input or
output. The model-proposed `missing` condition is therefore not accepted as a
code fact. The corresponding archived fields are
`code_side_no_auth_guard=false`,
`code_side_caller_guard_state_carriers=[acceptExecutorship]`, and
`solver_result=unsat` (SMT replay row 692, zero-based).

This pair is the important boundary: both candidates are retrieved and both
propose an authority-protection deficiency, but independent target-code facts
separate the vulnerable initialization from the guarded handoff.

## 4. Provenance of each field

| Item | Source of the value |
|---|---|
| Report type, operation and condition proposal | LLM-assisted corpus representation and retrieval record |
| Entry/carrier/path candidates and caller-guard facts | Deterministic target-code/PDG extraction |
| Joint satisfiability (`sat`/`unsat`) | SMT solver over the finite encoded facts and registry rule |
| Severity, Necessity, Feasibility | Harm Verdict LLM chain, run only after admission |

`C_f` selects the obligation to check. It does not directly set
`NoCallerAuthGuard`, the authority-write predicate, or the solver result. The
full paper cannot print the complete solver dump, but this page exposes the
actual target functions, the relevant rule conjunction, the archived bindings,
and the resulting branch before Harm Verdict.
