# Artifact Description

## Summary

This artifact provides the implementation, datasets, and experimental results for
MechaAudit, a mechanism-based vulnerability detection system for DeFi smart contracts.

## Artifact Contents

### Code

| File | Description |
|------|-------------|
| `mechaaudit/mdl/primitives.py` | MDL vocabulary: 23 Operation Vocabulary types (+ 1 non-applicable sentinel), 17 Condition Templates, predicate definitions |
| `mechaaudit/mdl/matching.py` | `pi_match` (operation set matching) and `condition_match` (template matching) |
| `mechaaudit/retrieval/retrieval.py` | Type-compatibility gate and MDL-based TopK ranking (simplified reference implementation; the full 9-signal lexicographic ranking used for the paper's results is described in the paper's ranking-signals table) |
| `mechaaudit/satisfiability/registry_admission.py` | Theorem registry admission predicate (label-blind) |
| `mechaaudit/harm_verdict/harm_verdict.py` | Serial Severity/Necessity/Feasibility LLM harm-verdict chain, ported line-for-line from the production harm-verdict prompt harness that generated the E4c judgments underlying the paper's main results table |
| `results/baselines/direct_llm_prompt.py` | Direct LLM baseline prompt (target-only, no retrieval, no SMT) |
| `results/logicscan_reproduction/prepare_case_inputs.py` | LogicScan audit-only input construction and synthetic retrieval template |
| `scripts/eval_metrics.py` | Metric computation script |
| `scripts/generate_pdg.sh` | PDG generation wrapper (requires Slither) |

### Data

| File | Description |
|------|-------------|
| `theorem_registry/registry_B.json` | 16 theorems matching the paper's theorem-registry table (a1-a5 core + b1-b11 extension), plus 3 additional extension theorems (b_e1-b_e3) included in this artifact's implementation but not enumerated in the paper's table (see the file's own `description` field) |
| `corpus/corpus_manifest.jsonl` | 394 audited findings with MDL triples (pi_r, c_r, tau_r) |
| `benchmark/manifest.jsonl` | 217 evaluated contracts with ground-truth labels |
| `benchmark/sample_pdgs/` | 2 sample PDGs (VULN + SAFE) |

### Results

| File | Description |
|------|-------------|
| `results/main/mechaaudit_metrics.json` | Main evaluation: 217 contracts, contract-level detection table in the paper |
| `results/baselines/comparison_table.json` | Baseline comparison: Slither, Direct LLM, GPTScan, LogicScan, Knowdit |
| `results/ablations/ablation_table.json` | Ablation: No Retrieval, No SMT, No Harm Verdict variants |
| `results/retrieval_quality/retrieval_recall_at_k.json` | Retrieval R@1/3/5/15, retrieval-recall table in the paper |
| `results/logicscan_reproduction/` | LogicScan audit-only reproduction protocol and synthetic retrieval template |

## Label-Blindness Guarantee

The detection pipeline makes no use of ground-truth labels during execution:
- Theorem registry admission (`registry_admits`) takes only structural function features and report type
- Retrieval ranking uses only MDL operation/condition overlap scores
- Harm verdict LLM prompts contain no benchmark labels or expected outcomes

Labels (`VULN`/`SAFE`) in `benchmark/manifest.jsonl` are provided only for metric computation.

## Correspondence to Paper Claims

| Paper Claim | Artifact Location |
|-------------|-------------------|
| MDL vocabulary $V$, $\mathcal{L}$ (no dedicated table in the paper; moved to the artifact due to page limits) | `mechaaudit/mdl/primitives.py` -> `OPERATION_VOCAB`, `CONDITION_TEMPLATES`; `docs/MDL_PRIMITIVES.md` |
| MDL adversarial-trigger space $\mathcal{T}$ | The corpus (`corpus/corpus_manifest.jsonl`) stores `adversarial_trigger` as a free natural-language record per report, not a closed categorical vocabulary like $V$/$\mathcal{L}$ (see `docs/MDL_PRIMITIVES.md`). It is not consumed by retrieval, SMT admission, or the Harm Verdict prompts; those independently re-derive triggerability from target-side PDG evidence (`mechaaudit/harm_verdict/harm_verdict.py`, FEASIBILITY condition). |
| Theorem registry $B$ (theorem-registry table) | `theorem_registry/registry_B.json` |
| 394-report corpus | `corpus/corpus_manifest.jsonl` |
| Contract-level detection (main results table) | `results/main/mechaaudit_metrics.json` |
| Baseline comparison (same table as main results) | `results/baselines/comparison_table.json` |
| Retrieval quality (retrieval-recall table) | `results/retrieval_quality/retrieval_recall_at_k.json` |
| Component ablation table | `results/ablations/ablation_table.json` |
| Harm Verdict prompts (simplified in the paper's figure) | `mechaaudit/harm_verdict/harm_verdict.py` |
| Direct LLM baseline prompt | `results/baselines/direct_llm_prompt.py` |
| LogicScan audit-only reproduction details | `results/logicscan_reproduction/` |
| Per-contract FN/FP attribution | `docs/ERROR_CASE_ATTRIBUTION.md` |
| McNemar's test significance | `docs/STATISTICAL_SIGNIFICANCE.md` |

## Limitations

- Full pipeline reproduction requires an LLM endpoint (harm verdict stage).
- Knowdit baseline used local Qwen3 reproduction with 0 valid findings; the original
  paper's numbers use GPT/Claude in a different agent environment.
- LogicScan: no official retrieval assets were found online; those assets are the key material for LogicScan to achieve good performance. The reported results are from a test without such assets (audit-only mode); see `results/logicscan_reproduction/`.
- `mechaaudit/retrieval/retrieval.py` is a simplified reference implementation of the retrieval gate and ranking score. It demonstrates the type-compatibility gate and MDL-overlap ranking concept; it does not implement the full 9-signal lexicographic ranking (`>_lex`) used to produce the paper's retrieval-quality numbers.
- `mechaaudit/harm_verdict/harm_verdict.py` reproduces the real production harness's per-family (L1/S1-1/S1-2/S5-3) SEVERITY/NECESSITY/FEASIBILITY guidance, boundary rules, and output schema verbatim. Every judgment in the paper's results is produced by this serial LLM chain alone, with no per-case or per-contract manual adjustment.
