# Evaluation Protocol

This document describes how to reproduce MechaAudit's main evaluation (contract-level detection table in the paper).

## Level 1: Metric Verification (No LLM Required)

Pre-computed results are in `results/main/mechaaudit_metrics.json`.

```bash
python scripts/eval_metrics.py --results results/main/mechaaudit_metrics.json
```

Expected output:
```
  TP= 59  FP= 18  FN= 11  TN=129
  Precision: 0.7662
  Recall:    0.8429
  FPR:       0.1224
  F1:        0.8027
```

## Level 2: Theorem Registry Inspection (No LLM Required)

The theorem registry contains 16 theorems matching the paper's theorem-registry
table, plus 3 additional extension theorems included in this artifact but not
enumerated in the paper's table (see `registry_B.json`'s own `description` field):
- `a1–a5`: five core mechanism admission rules (in the paper's table)
- `b1–b11`: eleven extension theorems for cross-cutting patterns (in the paper's table)
- `b_e1–b_e3`: three additional extension theorems present in this artifact's
  implementation, not enumerated in the paper's table; their harm boundary is
  unconstrained (`HB = empty set`)

```python
import json

registry = json.load(open("theorem_registry/registry_B.json"))
for t in registry["core_theorems"]:
    print(t["theorem_id"], t["name"])
```

## Level 3: Full Pipeline Reproduction (LLM Required)

Reproducing the full pipeline requires:
1. PDG data for your target contracts (generate using `scripts/generate_pdg.sh`)
2. An LLM endpoint compatible with the OpenAI API (Qwen3-32B or equivalent)

### Step 1: Generate PDG for a target contract

```bash
bash scripts/generate_pdg.sh path/to/Contract.sol ContractName output/pdg.json
```

### Step 2: Run Mechanism Retrieval

```python
import json
from mechaaudit.retrieval.retrieval import retrieve_top_k

corpus = [json.loads(l) for l in open("corpus/corpus_manifest.jsonl")]
func_mdl = {
    "mechanism_family": "L1",
    "s_f": [{"name": "outbound_asset_transfer"}],
    "c_f": [{"template_id": "C-L1a"}],
}
candidates = retrieve_top_k(func_mdl, corpus, top_k=15)
```

### Step 3: Run Mechanism Satisfiability

```python
import json
from mechaaudit.satisfiability.registry_admission import load_registry, registry_admits

registry = load_registry("theorem_registry/registry_B.json")
theorem_id, root_hit = registry_admits(
    registry=registry,
    function_leaf="withdraw",
    function_core_ops=["outbound_asset_transfer"],
    function_condition_templates=["C-L1a"],
    report_type="L1",
)
print(theorem_id, root_hit)
```

### Step 4: Run Harm Verdict

The Harm Verdict stage runs a serial Severity -> Necessity -> Feasibility
LLM chain; failure at any stage short-circuits with a SAFE verdict. This is
a line-level port of the real production prompt harness (see the module
docstring in `harm_verdict.py` for exactly what is and is not reproduced).

```python
from mechaaudit.harm_verdict.harm_verdict import run_harm_verdict_chain

# `item` is the target-side handoff record produced by joining the SMT
# witness (Step 2) with the target function's PDG-derived structural facts.
# See harm_verdict.py's module docstring for the full required shape.
item = {
    "target_contract": "AutoRoller",
    "target_function": "deposit",
    "report_id": "2022-11-sense/H-03",
    "smt": {
        "route": {"template_id": "C-S11b", "route_variant": "bootstrap_share_inflation"},
        "witness": {"entry_function": "deposit", "carrier_function": "previewDeposit",
                    "path_nodes": ["deposit", "previewDeposit"]},
        "m_ref_alignment": {"code_side_price_source_read_sources": ["totalSupply"]},
    },
    "mechanism_slice": {
        "contract_name": "AutoRoller",
        "source_file": "AutoRoller.sol",
        "functions": [
            {"name": "deposit", "visibility": "external", "state_mutability": "nonpayable",
             "modifiers": [], "state_vars_read": ["totalSupply"], "state_vars_written": ["balances"],
             "external_calls": [], "internal_calls": ["previewDeposit"], "called_by": [],
             "require_conditions": []},
            {"name": "previewDeposit", "visibility": "public", "state_mutability": "view",
             "modifiers": [], "state_vars_read": ["totalSupply", "totalAssets"],
             "state_vars_written": [], "external_calls": [], "internal_calls": [],
             "called_by": ["deposit"], "require_conditions": []},
        ],
    },
    "entry_routes": {"entry_function": "deposit", "visibility": "external",
                      "modifiers": [], "require_conditions": [], "called_by": []},
}

def call_llm(prompt: str) -> str:
    # send `prompt` to an OpenAI-compatible endpoint and return the raw text response
    ...

verdict, trace = run_harm_verdict_chain(item, call_llm)
# verdict is "VULN" or "SAFE"; trace records the parsed response
# ({applicable, failed_condition, sub_reason, reason, evidence_refs}) for
# each condition actually evaluated (SEVERITY, then NECESSITY, then FEASIBILITY).
```

## Baseline Reproduction

Baseline results are in `results/baselines/comparison_table.json`.

Baseline tools:
- **Slither**: `pip install slither-analyzer==0.10.4`
- **Direct LLM**: prompt in `results/baselines/direct_llm_prompt.py`; no external tool required
- **GPTScan**: https://github.com/GPTScan/GPTScan
- **LogicScan**: reproduced under an audit-only configuration (no official retrieval
  assets are publicly available); see `results/logicscan_reproduction/` for the full
  protocol, synthetic retrieval template, and verdict-parsing rule
- **Knowdit**: https://github.com/IntelligentDDS/Knowdit (requires GPT/Claude environment)

## Ablation Study

Ablation results are in `results/ablations/ablation_table.json`.

| Variant                       | Recall | F1    | vs. Full MechaAudit          |
|--------------------------------|-------:|------:|-------------------------------|
| Full MechaAudit                | 0.8429 | 0.8027|                               |
| No Retrieval (rand.)           | 0.3857 | 0.4954| -0.457 recall                 |
| No SMT (retrieval + harm-verdict only) | 0.5714 | 0.4908| -0.271 recall, 3x FPR  |
| No Harm Verdict (SMT-only)      | 0.9714 | 0.6326| +0.129 recall, 4x FPR         |

The third variant predicts a contract positive whenever any function has at
least one SMT-admitted mechanism unit, without running the harm-verdict
chain. It shows that SMT admission alone proves mechanism existence but not
business harm: recall rises but FPR quadruples relative to the full pipeline.

## Retrieval Quality

Retrieval quality numbers are in `results/retrieval_quality/retrieval_recall_at_k.json`.

**Combined (n=239 VULN functions across all three benchmarks):**

| Variant              | R@1    | H@3    | H@5    | H@15   |
|----------------------|-------:|-------:|-------:|-------:|
| Type-only baseline   | ~0.06${}^{\dagger}$ | 0.2552 | 0.3180 | 0.5397 |
| MechaAudit           | 0.3724 | 0.6067 | 0.7113 | 0.8828 |

${}^{\dagger}$ The type-only baseline's R@1 is not computed on the full N=239
set; it is estimated from a 123-function diagnostic subset used during
retrieval-gate calibration (7/123 = 0.0569). See the `type_only_hit_at_1_diagnostic`
field in `retrieval_recall_at_k.json`.

**Per-benchmark breakdown (MechaAudit):**

| Benchmark     | n   | H@3    | H@5    | H@15   |
|---------------|-----|-------:|-------:|-------:|
| Sherlock      | 116 | 0.5431 | 0.6466 | 0.8448 |
| Web3Bugs      |  13 | 0.9231 | 0.9231 | 0.9231 |
| DeFiHackLabs  | 110 | 0.6364 | 0.7545 | 0.9182 |
