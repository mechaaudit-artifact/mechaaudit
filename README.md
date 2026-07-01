# MechaAudit

## Overview

MechaAudit detects DeFi vulnerabilities by matching mechanism descriptions
from historical audit reports against formal program dependence graphs (PDGs)
of target contracts, verified by SMT theorem admission.

The pipeline has three stages:
1. **Mechanism Retrieval** — semantic top-K candidate selection from a 394-report corpus
2. **Mechanism Satisfiability** — SMT-backed theorem admission (16 theorems matching the paper's theorem-registry table, plus 3 additional extension theorems included in this artifact; see `theorem_registry/registry_B.json`)
3. **Harm Verdict** — serial Severity/Necessity/Feasibility LLM chain (see `mechaaudit/harm_verdict/harm_verdict.py`)

## Benchmark

217 contracts across three datasets (70 VULN, 147 SAFE):

| Dataset       | VULN | SAFE | Total |
|---------------|-----:|-----:|------:|
| Sherlock      |   31 |   64 |    95 |
| Web3Bugs      |    7 |   44 |    51 |
| DeFiHackLabs  |   32 |   39 |    71 |
| **Total**     |**70**|**147**|**217**|

## Main Results (contract-level detection table)

| System          | Precision | Recall | FPR   | F1     |
|-----------------|----------:|-------:|------:|-------:|
| MechaAudit      | 0.7662    | 0.8429 | 0.1224| 0.8027 |
| Slither         | 0.3333    | 0.2714 | 0.2585| 0.2992 |
| Direct LLM      | 0.4375    | 0.2000 | 0.1224| 0.2745 |
| GPTScan (Qwen)  | 0.4615    | 0.2609 | 0.1489| 0.3333 |
| GPTScan (gpt-5) | 0.6000    | 0.2903 | 0.1017| 0.3913 |
| LogicScan†      | 0.3238    | 0.4857 | 0.4830| 0.3886 |
| Knowdit‡        | N/A       | N/A    | N/A   | N/A    |

† No official retrieval assets for LogicScan were found anywhere online; those assets are the key material for LogicScan to achieve good performance. The results reported here are from a test without such assets (audit-only mode). See `results/logicscan_reproduction/`.

‡ Local Qwen3-32B reproduction produced 0 valid findings. The original Knowdit paper uses GPT/Claude in a specialized agent environment not reproduced here; these numbers are not directly comparable. See `results/baselines/comparison_table.json`.

## Repository Structure

```
mechaaudit/               Core pipeline implementation
  mdl/
    primitives.py         MDL vocabulary (OPERATION_VOCAB, CONDITION_TEMPLATES)
    matching.py           pi_match and condition_match
  retrieval/
    retrieval.py          Type-compatibility gate + MDL-based TopK ranking (simplified reference)
  satisfiability/
    registry_admission.py Theorem registry admission predicate
  harm_verdict/
    harm_verdict.py       Serial Severity/Necessity/Feasibility LLM chain

theorem_registry/
  registry_B.json         16 theorems matching the paper's table (a1-a5 core + b1-b11
                           extension), plus 3 additional extension theorems (b_e1-b_e3)
                           included here but not in the paper's table

corpus/
  corpus_manifest.jsonl   394 audited findings with MDL triples (pi_r, c_r)

benchmark/
  manifest.jsonl          217 evaluated benchmark contracts (case_id, label, focus_types)
  sample_pdgs/            2 sample PDGs

results/
  main/
    mechaaudit_metrics.json   Main evaluation results (217 contracts)
  baselines/
    comparison_table.json     All baseline comparison numbers (incl. Direct LLM)
    direct_llm_prompt.py      Direct LLM baseline prompt (target-only)
  ablations/
    ablation_table.json       Ablation study results (No Retrieval / No SMT / No Harm Verdict)
  retrieval_quality/
    retrieval_recall_at_k.json  Retrieval R@1/3/5/15 across all 3 benchmarks
  logicscan_reproduction/
    README.md                 LogicScan audit-only reproduction protocol
    prepare_case_inputs.py     Input construction and synthetic retrieval template

scripts/
  eval_metrics.py         Compute metrics from results or custom predictions
  generate_pdg.sh         Generate PDG for a single Solidity contract
```

## Quick Start

```bash
# View main results
python scripts/eval_metrics.py --results results/main/mechaaudit_metrics.json

# View theorem registry
python -c "import json; r = json.load(open('theorem_registry/registry_B.json')); print(len(r['core_theorems']), 'core theorems,', len(r['extension_theorems']), 'extension theorems')"

# Count corpus reports by mechanism family
python -c "
import json
from collections import Counter
c = Counter(json.loads(l)['mechanism_family'] for l in open('corpus/corpus_manifest.jsonl'))
print(c)
"
```

## PDG Data

Sample PDGs for 2 contracts are in `benchmark/sample_pdgs/`.

## Dependencies

```
python >= 3.10
slither-analyzer == 0.10.x   # for PDG generation only
```

No training, no fine-tuning. The harm verdict stage uses an LLM API endpoint
(Qwen3-32B or compatible); the rest of the pipeline is deterministic.

## Reproducibility Notes

- All results use the label-blind evaluation pipeline; no per-case or per-contract manual adjustment is applied at any pipeline stage.
- The theorem registry and corpus are frozen; reproducing SMT results requires
  running the full pipeline against the PDGs and an LLM endpoint.
- Metric recomputation from the provided results JSON requires no LLM.

See `EVALUATION_PROTOCOL.md` for step-by-step reproduction instructions.
