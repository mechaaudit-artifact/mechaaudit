"""Direct LLM baseline prompt (target-only), as run for the paper's Table IV
"Direct LLM" row (TP=14, FP=18, FN=56, TN=129).

This is the actual prompt-construction logic used to produce that baseline's
results, reduced to a standalone reference (path-independent, no project
manifest I/O). Its structure mirrors the Harm Verdict stage (see
mechaaudit/harm_verdict/harm_verdict.py) but omits the serial
Severity/Necessity/Feasibility clause chain: the model is asked to determine
vulnerability_present directly, in one shot, from target-side evidence only.

Forbidden inputs (deliberately excluded from the prompt): retrieval results,
historical audit reports, SMT solver witnesses, ground-truth labels, and any
prior MechaAudit verdict. Only the target function's source and formal PDG
facts are provided.
"""

import json
from typing import Any, Dict, List


FOCUSED_SCOPE = {
    "L1": "Unauthorized or incorrectly authorized privileged state transition, asset movement, or parameter change.",
    "S1-1": "Accounting/share/price/index logic that can mis-mint, mis-burn, mis-price, or mis-account value.",
    "S1-2": "Time, epoch, lock, reward, interest, or accumulation logic that can be manipulated or bypassed.",
    "S5-3": "External-call, callback, permission, or integration path that can break asset or privilege safety.",
}

PROMPT_VERSION = "target-only-direct-llm-v2"


def build_direct_llm_prompt(
    case: Dict[str, Any],
    target_function: Dict[str, Any],
) -> List[Dict[str, str]]:
    """Construct the Direct LLM baseline prompt for one target function.

    Args:
        case: contract-level case metadata (case_id, benchmark, focus_types, ...).
        target_function: compact PDG facts for the target function (source,
            modifiers, state_vars_read/written, external_calls, require_conditions,
            if_conditions, assignments, compact_graph, ...). No labels included.

    Returns:
        A chat-style message list (system + user) ready to send to an
        OpenAI-compatible LLM endpoint.
    """
    system = (
        "You are a smart-contract security auditor. Classify only the focused "
        "vulnerability families from target-side code facts. Do not assume "
        "a vulnerability from naming alone. If evidence is weak, return false. "
        "Do not reveal chain-of-thought. Return only the required JSON object."
    )
    user_payload = {
        "task": "target_only_direct_llm",
        "prompt_version": PROMPT_VERSION,
        "allowed_evidence": [
            "target function source",
            "formal PDG facts for the target function",
            "focused-scope family definitions",
        ],
        "forbidden_evidence": [
            "retrieval result",
            "historical report",
            "solver-backed proof or counterexample",
            "ground-truth label",
            "previous SemanticVulnMatch verdict",
        ],
        "focused_scope_definitions": FOCUSED_SCOPE,
        "decision_rule": (
            "Return vulnerability_present=true only if mechanism_present, "
            "business_harm, and attacker_triggerable are all true and "
            "focused_family is not NONE."
        ),
        "case": case,
        "target_function": target_function,
        "required_output": {
            "format": "one JSON object only; no markdown; no <think>; no prose",
            "schema": {
                "vulnerability_present": "boolean",
                "focused_family": "L1|S1-1|S1-2|S5-3|NONE",
                "mechanism_present": "boolean",
                "business_harm": "boolean",
                "attacker_triggerable": "boolean",
                "primary_failure": (
                    "NONE|out_of_scope|mechanism_absent|no_business_harm|"
                    "not_attacker_triggerable|insufficient_evidence"
                ),
                "confidence": "low|medium|high",
                "reason": "short target-only explanation",
                "evidence_refs": ["function/state/call/condition names only"],
            },
        },
    }
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": json.dumps(user_payload, ensure_ascii=False, indent=2)},
    ]


def parse_direct_llm_verdict(llm_response: str) -> bool:
    """Parse the boolean vulnerability_present field from the LLM's JSON reply."""
    obj = json.loads(llm_response)
    return bool(obj.get("vulnerability_present", False))
