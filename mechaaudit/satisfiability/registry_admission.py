"""
Theorem registry admission predicate for Mechanism Satisfiability.

A (function, report) pair is admitted by a theorem when:
  - The report type is in the theorem's report_types_any, AND
  - The function matches on any of: function-root / core-op / condition.

This is the label-blind gate before SMT solver execution.
No ground-truth label (VULN/SAFE) is consulted here.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, Set, Tuple


def _norm(value: Any) -> str:
    return str(value or "").strip()


def _leaf(value: Any) -> str:
    return _norm(value).split(".")[-1]


def _lower_set(values: Iterable[Any]) -> Set[str]:
    return {_norm(v).lower() for v in values or [] if _norm(v)}


def load_registry(path: Path) -> Dict[str, Any]:
    """Load a theorem registry JSON file."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _all_theorems(registry: Dict[str, Any]) -> list:
    """Collect all theorems from a registry (handles both flat and split formats)."""
    theorems = []
    if "theorems" in registry:
        theorems.extend(registry["theorems"])
    if "core_theorems" in registry:
        theorems.extend(registry["core_theorems"])
    if "extension_theorems" in registry:
        theorems.extend(registry["extension_theorems"])
    return theorems


def root_leaf_set(registry: Dict[str, Any]) -> Set[str]:
    """All function-root leaf names declared by any theorem (lowercased)."""
    roots: Set[str] = set()
    for theorem in _all_theorems(registry):
        function_side = theorem.get("function_side") or {}
        for value in function_side.get("function_roots_any") or []:
            leaf = _leaf(value).lower()
            if leaf:
                roots.add(leaf)
    return roots


def registry_admits(
    registry: Dict[str, Any],
    function_leaf: str,
    function_core_ops: Iterable[Any],
    function_condition_templates: Iterable[Any],
    report_type: str,
) -> Tuple[Optional[str], bool]:
    """Return (theorem_id, root_hit) for the first admitting theorem.

    theorem_id is None when no theorem admits the pair.
    root_hit is True when admission is by exact function-root match (strongest signal).
    """
    leaf = _leaf(function_leaf).lower()
    ops = _lower_set(function_core_ops)
    conditions = _lower_set(function_condition_templates)
    rtype = _norm(report_type)
    if not rtype:
        return None, False

    for theorem in _all_theorems(registry):
        report_types = set(theorem.get("report_side", {}).get("report_types_any") or [])
        if rtype not in report_types:
            continue
        function_side = theorem.get("function_side") or {}
        roots = {_leaf(v).lower() for v in function_side.get("function_roots_any") or [] if _leaf(v)}
        theorem_ops = _lower_set(function_side.get("ops_any"))
        theorem_conditions = _lower_set(function_side.get("conditions_any"))
        root_hit = leaf in roots
        if root_hit or (ops & theorem_ops) or (conditions & theorem_conditions):
            return _norm(theorem.get("theorem_id")), root_hit
    return None, False
