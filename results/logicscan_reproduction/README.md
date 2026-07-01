# LogicScan Audit-Only Reproduction

This directory documents the exact reproduction configuration behind the
`LogicScan (Qwen3-32B, audit-only)` row in
`results/baselines/comparison_table.json`
(TP=34, FP=71, FN=36, TN=76, F1=0.3886), matching the paper's Table IV row
marked `\ddagger`.

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
2. **Tool invocation**: run LogicScan's own CLI unmodified —
   `python logicscan.py --repo-root <LogicScan-repo> audit-functions --input retrieval_results.json --descriptions descriptions.json`
   — against a local Qwen3-32B-AWQ OpenAI-compatible endpoint.
3. **Verdict parsing**: LogicScan emits a Markdown audit report per function.
   A case is scored positive if any report contains the Chinese verdict
   marker `判断结果: 是` ("verdict: yes"); negative if it only contains
   `判断结果: 否` ("verdict: no"). Contract-level positive = any function
   positive.

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
