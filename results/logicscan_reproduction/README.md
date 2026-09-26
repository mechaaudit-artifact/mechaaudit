# LogicScan Audit-Only Reproduction

This directory documents the exact reproduction configuration behind the
`LogicScan (Qwen3-32B, audit-only)` row in
`results/baselines/comparison_table.json`
(TP=34, FP=71, FN=36, TN=76, F1=0.3886), matching the paper's Table IV row
marked `\ddagger`.

## Completed evaluation

All **217 contracts have valid, decided outputs** in the combined archived run.
The table below is copied from that run's aggregate records, rather than obtained
by rerunning the detector. The full pipeline is evaluated on the same 70 VULN and
147 SAFE contracts with the same local Qwen3-32B-AWQ model.

| Benchmark | Valid | TP | FP | FN | TN |
|---|---:|---:|---:|---:|---:|
| Sherlock | 95 | 13 | 27 | 18 | 37 |
| Web3Bugs | 51 | 4 | 25 | 3 | 19 |
| DeFiHackLabs | 71 | 17 | 19 | 15 | 20 |
| **Total** | **217** | **34** | **71** | **36** | **76** |

LogicScan audit-only obtains precision 0.324, recall 0.486, FPR 0.483, and F1
0.389; MechaAudit obtains 0.766, 0.843, 0.122, and 0.803 respectively. Thus the
reported comparison includes a dedicated business-logic auditing component,
with 25 more true positives and 53 fewer false positives for MechaAudit under
the stated configuration. The audit-only scope is explained below and is also
marked in the submitted paper.

See [archived metrics by benchmark](audit_only_metrics.json) and the
[original comparison table](../baselines/comparison_table.json).

## Why "audit-only"

LogicScan's original design retrieves similar business-logic contracts from
an on-chain contract database before auditing. No official copy of that
retrieval database is publicly available, and it is the key material behind
LogicScan's reported performance. We therefore run LogicScan's own
`audit-functions` command directly on our benchmark's PDG-recovered target
functions, using LogicScan's own prompting strategy, but supply a synthetic
single-entry "retrieval result" per case instead of a real on-chain retrieval
hit. This isolates and measures LogicScan's audit/confirmation component; it
is explicitly **not paper-faithful** to LogicScan's full pipeline.

## Reproduction pipeline

1. **Input construction** (`prepare_case_inputs.py` in this directory mirrors
   the input-construction logic used for the reported run):
   for each benchmark case, read the case's formal PDG, select up to
   `max_functions_per_case` candidate target functions (from
   `candidate_target_functions`, falling back to any public/external function
   with source), and write two files per case:
   - `descriptions.json`: function name, signature, parameter types, and
     source code for each selected target function.
   - `retrieval_results.json`: one synthetic "match" per target function
     (see `template_for()` below), standing in for the unavailable on-chain
     retrieval hit.
2. **Tool invocation**: run LogicScan's own CLI —
   `python logicscan.py --repo-root <LogicScan-repo> audit-functions --input retrieval_results.json --descriptions descriptions.json`
   — against a local Qwen3-32B-AWQ OpenAI-compatible endpoint, retaining its audit
   and confirmation workflow and prompts. Local inference adaptations include
   the endpoint configuration and generation-token caps, described below.
3. **Verdict parsing**: LogicScan emits a Markdown audit report per function.
   A case is scored positive if any report contains the Chinese verdict
   marker `判断结果: 是` ("verdict: yes"); negative if it only contains
   `判断结果: 否` ("verdict: no"). Contract-level positive = any function
   positive.

   The confirmation agent's `confirmed` status means that it accepted its audit
   report, not that a vulnerability was found. Vulnerability predictions come
   from the report's explicit yes/no decision.

### Archived execution and local adaptation

The initial batch completed 66 cases before an inference-service failure. The
remaining 151 cases completed in a recovery batch with explicit generation caps
(768 tokens for audit and 128 for confirmation). The reported result combines
these successful outputs: 217 valid cases, zero remaining invalid or undecided
cases. Infrastructure failures were not scored as vulnerability negatives.
This provenance explains the reported completed experiment; it is not a claim
that the full batch used identical generation caps.

## Synthetic retrieval template

Because there is no real on-chain retrieval hit, each target function is
paired with a single generic template describing only its claimed mechanism
family (one of the paper's four families), not any concrete vulnerable code:

```json
{
  "id": 1,
  "contract_address": "local-template",
  "function_name": "template_<family>",
  "category": "Semantic",
  "score": 0.5,
  "function_source_code": "function secureTemplate() external { /* reference logic omitted in audit-only reproduction */ }",
  "description": "Reference template for focused families: <family>.",
  "logic_description": "Compare the target function against the claimed semantic vulnerability family. Decide whether attacker-controlled execution can cause concrete victim-adverse harm.",
  "dsl": "family=<family>"
}
```

This gives LogicScan's audit stage a mechanism-family label to reason
against, without leaking any of MechaAudit's retrieval, SMT, or harm-verdict
evidence, and without providing the concrete matched code that the original
on-chain retrieval database would have supplied.

## Files in this directory

- `README.md` — this file.
- `prepare_case_inputs.py` — standalone, path-independent version of the
  input-construction and synthetic-template logic described above.
- `audit_only_metrics.json` — archived completed metrics, including all three
  benchmark breakdowns; added as a documentation supplement on 2026-09-25.
