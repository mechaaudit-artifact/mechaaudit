"""LogicScan audit-only input construction (standalone reference).

Builds the two input files LogicScan's own `audit-functions` CLI expects
(`descriptions.json`, `retrieval_results.json`) from a target contract's
formal PDG, substituting a synthetic single-entry retrieval template for the
unavailable on-chain retrieval database. See README.md in this directory for
the full reproduction protocol.
"""

import json
from pathlib import Path
from typing import Any, Dict, List


def pdg_functions(pdg: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Flatten a formal PDG's contracts/functions into name -> function dict."""
    out: Dict[str, Dict[str, Any]] = {}
    contracts = pdg.get("contracts") or [pdg]
    for contract in contracts:
        for fn in contract.get("functions", []) or []:
            name = fn.get("name")
            source = fn.get("source")
            if name and source and name not in out:
                out[name] = fn
    return out


def choose_functions(
    pdg: Dict[str, Any],
    candidate_target_functions: List[str],
    max_functions: int = 1,
) -> List[Dict[str, Any]]:
    """Select up to max_functions target functions for audit."""
    funcs = pdg_functions(pdg)
    wanted = []
    for name in candidate_target_functions:
        if name in funcs:
            wanted.append(funcs[name])
        if len(wanted) >= max_functions:
            break
    if not wanted:
        for fn in funcs.values():
            if fn.get("visibility") in {"public", "external"}:
                wanted.append(fn)
                break
    if not wanted and funcs:
        wanted.append(next(iter(funcs.values())))
    return wanted[:max_functions]


def template_for(focus_types: List[str]) -> Dict[str, Any]:
    """Synthetic retrieval-result template standing in for the unavailable
    on-chain LogicScan retrieval database. Carries only the claimed mechanism
    family, not any concrete matched code.
    """
    family = ",".join(focus_types or [])
    return {
        "id": 1,
        "contract_address": "local-template",
        "function_name": f"template_{family or 'semantic_vulnerability'}",
        "category": "Semantic",
        "score": 0.5,
        "function_source_code": "function secureTemplate() external { /* reference logic omitted in audit-only reproduction */ }",
        "description": f"Reference template for focused families: {family or 'unknown'}.",
        "logic_description": (
            "Compare the target function against the claimed semantic vulnerability family. "
            "Decide whether attacker-controlled execution can cause concrete victim-adverse harm."
        ),
        "dsl": f"family={family or 'unknown'}",
    }


def write_case_inputs(
    case_id: str,
    benchmark: str,
    focus_types: List[str],
    functions: List[Dict[str, Any]],
    output_dir: Path,
) -> None:
    """Write descriptions.json and retrieval_results.json for one case."""
    output_dir.mkdir(parents=True, exist_ok=True)
    descriptions = {
        "chain": benchmark,
        "address": case_id,
        "category": ",".join(focus_types or []),
        "functions": [
            {
                "function_name": fn.get("name"),
                "signature": fn.get("name"),
                "input_types": [str(p) for p in fn.get("parameters", []) or []],
                "description": f"Audit target function {fn.get('name')} for focused families {','.join(focus_types or [])}.",
                "context_source": fn.get("source", ""),
                "target_source": fn.get("source", ""),
            }
            for fn in functions
        ],
    }
    retrieval_results = [
        {"function_name": fn.get("name"), "matches": [template_for(focus_types)]}
        for fn in functions
    ]
    (output_dir / "descriptions.json").write_text(
        json.dumps(descriptions, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (output_dir / "retrieval_results.json").write_text(
        json.dumps(retrieval_results, ensure_ascii=False, indent=2), encoding="utf-8"
    )


POSITIVE_MARKER = "判断结果: 是"
NEGATIVE_MARKER = "判断结果: 否"


def parse_verdict(report_markdown: str) -> "bool | None":
    """Parse LogicScan's own report verdict marker. Returns True/False/None
    (None if neither marker is present)."""
    if POSITIVE_MARKER.replace(" ", "") in report_markdown.replace(" ", ""):
        return True
    if NEGATIVE_MARKER.replace(" ", "") in report_markdown.replace(" ", ""):
        return False
    return None
