# Corpus construction and provenance

The corpus contains **394 historical Code4rena findings**, selected from 4,709
extracted findings by vulnerability-family classification and manual verification.
The four studied families define the selection scope. Classification of a report
and construction of its mechanism representation are separate steps.

## Selection and representation

1. **Select reports in scope.** LLM-assisted classification assigns vulnerability
   categories to the extracted findings. Manual review of the four-family
   candidates checks the reported flaw, missing protection, and causal chain,
   removing incorrect family assignments. This yields the 394 admitted findings.
2. **Construct shared vocabularies.** As described in the paper's prerequisite
   section, LLM-assisted semantic aggregation and consistency review produce the
   operation vocabulary and condition templates. Equivalent missing-protection
   descriptions are grouped into shared conditions. The final vocabulary contains
   23 code-observable operation types and 17 condition templates; the implementation
   also has a `none_applicable` skip marker.
3. **Encode and review findings.** The paper describes extracting each report's
   operation flow, missing conditions, and adversarial trigger with an LLM, followed
   by human inspection before admission. Corpus curation is offline; it is separate
   from SMT checking of a candidate mechanism in a target contract.

The original [public manifest](../corpus/corpus_manifest.jsonl) exports report IDs,
family annotations, operation records (`pi_r`), and condition records (`c_r`).
It is not a complete export of all original narratives, trigger records, or
individual human-review decisions. The
[17-template mapping](CONDITION_TEMPLATE_MAPPING.md) and
[structured examples](../corpus/template_examples.json) provide concrete source
findings and recorded condition assignments for every template. They document
provenance; they do not add inputs to detection.

## Corpus composition

Counts below are computed from the unchanged public manifest. Years refer to the
contest identifiers, not an independently inferred disclosure date.

| Family | Findings |
|---|---:|
| Reentrancy | 96 |
| Asset valuation manipulation | 72 |
| Slippage/sandwich | 101 |
| Missing access control | 125 |
| **Total** | **394** |

| Contest year | Findings |
|---|---:|
| 2021 | 84 |
| 2022 | 142 |
| 2023 | 85 |
| 2024 | 74 |
| 2025 | 9 |
| **Total** | **394** |

These distributions and the source-to-template examples establish the corpus basis
and studied scope. They do not measure exhaustive coverage of every possible
vulnerability in these families. Additional reports can be curated with the same
procedure, extending the vocabulary when a new missing-protection category is
needed. A template may apply across family contexts, and a report may instantiate
more than one template.

The full records and mappings are too extensive to reproduce in the page-limited
paper. The artifact supplies this detail alongside the paper's concise construction
description and representative examples.

Documentation supplement added on 2026-09-25. This description consolidates existing
method and curation records; it introduces no new experiment or corpus revision.
