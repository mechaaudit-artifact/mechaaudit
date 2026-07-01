"""
Mechanism Retrieval: select top-K report candidates for a target function.

Pipeline:
  1. Gate: type-compatibility filter (report type must match function's mechanism family)
  2. Rank: MDL-based score (operation overlap ratio + condition template overlap)
  3. TopK: return top K candidates (default K=15)

Input:  function MDL (pi_f, c_f extracted from PDG) + 394-report corpus
Output: ordered list of (report_id, score) candidates
"""

from typing import Dict, List, Optional, Tuple
from ..mdl.primitives import CONDITION_TEMPLATES, TEMPLATE_IDS


DEFAULT_TOP_K = 15

REPORT_TYPE_TO_FAMILY = {
    "L1": "L1",
    "S1-1": "S11",
    "S1-2": "S12",
    "S5-3": "S53",
}

FAMILY_TO_REPORT_TYPES = {v: k for k, v in REPORT_TYPE_TO_FAMILY.items()}


def _extract_op_names(s_list: list) -> set:
    return {op["name"] for op in s_list if isinstance(op, dict) and op.get("name")}


def _get_template_ids(cond_list: list) -> set:
    tids = set()
    for c in cond_list or []:
        if isinstance(c, dict):
            tid = c.get("template_id") or c.get("type")
            if tid and tid in TEMPLATE_IDS:
                tids.add(tid)
    return tids


def _type_compatible(func_family: str, report_type: str) -> bool:
    """Type-compatibility gate: the report type must match the function's family."""
    mapped = REPORT_TYPE_TO_FAMILY.get(report_type, report_type)
    return mapped == func_family


def _score_candidate(func_mdl: dict, report_mdl: dict) -> float:
    """Compute ranking score for a (function, report) candidate pair.

    Score = operation_overlap_ratio * 0.6 + condition_template_overlap * 0.4
    """
    func_ops = _extract_op_names(func_mdl.get("s_f", []))
    report_ops = _extract_op_names(report_mdl.get("s_r", []))

    if not report_ops:
        report_ops = {op.get("op", "") for op in report_mdl.get("pi_r", [])
                      if isinstance(op, dict) and op.get("op")}

    op_score = 0.0
    if report_ops:
        overlap = len(func_ops & report_ops)
        op_score = overlap / len(report_ops)

    func_templates = _get_template_ids(func_mdl.get("c_f", []))
    report_templates = set(report_mdl.get("template_ids", []))

    cond_score = 0.0
    if report_templates:
        overlap = len(func_templates & report_templates)
        cond_score = overlap / len(report_templates)

    return op_score * 0.6 + cond_score * 0.4


def retrieve_top_k(
    func_mdl: dict,
    corpus: List[dict],
    top_k: int = DEFAULT_TOP_K,
) -> List[Dict]:
    """Retrieve top-K report candidates for a target function.

    Args:
        func_mdl:  Function MDL dict with keys: mechanism_family, s_f, c_f.
        corpus:    List of report MDL dicts from corpus_manifest.jsonl.
        top_k:     Maximum number of candidates to return.

    Returns:
        List of candidate dicts, each with keys:
          report_id, mechanism_family, score, gate_pass
    """
    func_family = func_mdl.get("mechanism_family", "")

    candidates = []
    for report in corpus:
        report_type = report.get("mechanism_family", "")
        if not _type_compatible(func_family, report_type):
            continue

        score = _score_candidate(func_mdl, report)
        candidates.append({
            "report_id": report.get("report_id", ""),
            "mechanism_family": report_type,
            "score": score,
            "gate_pass": True,
        })

    candidates.sort(key=lambda x: x["score"], reverse=True)
    return candidates[:top_k]
