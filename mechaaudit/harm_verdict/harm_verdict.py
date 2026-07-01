"""Harm Verdict: three-condition LLM chain (Severity -> Necessity -> Feasibility).

FIDELITY NOTE (read before using): this module is a faithful, line-level port
of the production harm-verdict prompt-construction logic used to produce the
E4c judgments underlying the paper's main results table (TP=59, FP=18,
FN=11, TN=129; see `results/main/mechaaudit_metrics.json`). Every judgment
is produced by this serial LLM chain alone; no per-case or per-contract
manual adjustment is applied at any point in the pipeline.

Given a (target function, reference report) pair where Mechanism
Satisfiability has confirmed a mechanism match (SMT admission), this module
determines whether the target contract's specific execution context
constitutes an actual, exploitable vulnerability. Each condition is asked as
a separate LLM call and executes serially: failure at any stage
short-circuits the chain and yields a SAFE verdict.

  1. SEVERITY:    would the mechanism, if unprotected, cause real economic
                  or authority harm to users (not just admin inconvenience,
                  a tunable governance parameter, or a bare DoS/revert)?
  2. NECESSITY:   does protection responsibility belong to THIS contract,
                  rather than being delegated to another contract in the
                  architecture or already covered by an equivalent guard?
  3. FEASIBILITY: can an ordinary external attacker actually trigger the
                  mechanism in this contract's specific business context
                  (as opposed to only an admin/governance-restricted path)?

A VULN verdict requires all three conditions to pass (applicable=true). This
is the basis for the paper's Figure 4 (Harm Verdict prompts, simplified).
"""

from __future__ import annotations

import json
from typing import Any, Dict, Iterable, List, Optional, Tuple


# ── Family classification ──────────────────────────────────────────────────
# Maps a report-side condition template (see mechaaudit/mdl/primitives.py,
# CONDITION_TEMPLATES) to one of the four vulnerability families this module
# has dedicated guidance for.

FAMILY_BY_TEMPLATE = {
    "C-L1a": "L1", "C-L1b": "L1", "C-L1c": "L1", "C-L1d": "L1",
    "C-S11a": "S1-1", "C-S11b": "S1-1", "C-S11c": "S1-1", "C-S11d": "S1-1",
    "C-S12a": "S1-2", "C-S12b": "S1-2", "C-S12c": "S1-2", "C-S12d": "S1-2",
    "C-S53a": "S5-3", "C-S53b": "S5-3", "C-S53c": "S5-3",
    "C-S53d": "S5-3", "C-S53e": "S5-3",
}


class HarmVerdictError(RuntimeError):
    """Raised when the input item does not satisfy the required contract."""


# ── Per-family condition guidance (verbatim from the production harness) ──

SEVERITY_GUIDANCE = {
    "L1": (
        "\n## Template Assessment Context: Reentrancy (L1)\n"
        "Scenario: Function '{vulnerable_function}' makes external call '{external_call}' before "
        "updating state variable '{state_variable}'. An attacker can re-enter '{vulnerable_function}' "
        "through the callback, exploiting the un-updated '{state_variable}' to extract funds or "
        "corrupt state.\n\n"
        "Key question for SEVERITY: Does re-entering '{vulnerable_function}' while "
        "'{state_variable}' is stale actually allow extraction of funds or corruption of critical "
        "accounting? If '{state_variable}' is not used in any value-dependent computation during "
        "the re-entry path, the consequence may be unreachable."
    ),
    "S1-1": (
        "\n## Template Assessment Context: Price Manipulation (S1-1)\n"
        "Scenario: Function '{price_function}' derives a price from '{price_source}' (an AMM "
        "reserve, spot price, or balanceOf query). Function '{dependent_operation}' uses this "
        "price for a critical decision (minting, liquidation, swap amount).\n\n"
        "Key question for SEVERITY: Is '{price_source}' a spot value that can be manipulated "
        "within a single transaction (e.g., Uniswap reserve, raw balanceOf), or a time-averaged/"
        "oracle value resistant to flash-loan manipulation? If '{price_source}' is a TWAP, "
        "Chainlink oracle, or internal accounting variable, manipulation cost is prohibitively high. "
        "Even for manipulable sources, severity requires a concrete attacker-beneficial and "
        "victim-adverse delta, not merely a public sync, routing, or bookkeeping operation."
    ),
    "S1-2": (
        "\n## Template Assessment Context: Missing User Protective Bound (S1-2)\n"
        "Scenario: Function '{swap_function}' performs a price- or time-sensitive asset operation "
        "without enforcing the caller's protective bound '{amount_parameter}'. The bound may be "
        "minimum output, maximum input, deadline/time validity, or a fixed tolerance.\n\n"
        "Key question for SEVERITY: Which bound is missing for this exact route? Min-out protects "
        "exact-input variable-output flows; max-input protects exact-output flows; deadline protects "
        "against stale execution after the caller's intended time window. Do not reject a deadline "
        "route merely because the harm is not a min-out sandwich."
    ),
    "S5-3": (
        "\n## Template Assessment Context: Missing Access Control (S5-3)\n"
        "Scenario: Function '{privileged_function}' modifies critical state variable "
        "'{critical_state}' without access control.\n\n"
        "Key question for SEVERITY: Can an unauthorized modification of '{critical_state}' by "
        "an external caller lead to fund extraction or irreversible state corruption? Authority "
        "or permanent-state corruption can be severe even without an immediate token transfer."
    ),
}

NECESSITY_GUIDANCE = {
    "L1": (
        "\n## Template Responsibility Context (L1: Reentrancy)\n"
        "The concern suggests '{vulnerable_function}' should follow checks-effects-interactions "
        "pattern: update '{state_variable}' BEFORE making external call '{external_call}'.\n"
        "Key delegation question: Does '{vulnerable_function}' delegate the actual asset operation "
        "to an underlying contract where reentrancy is already handled?"
    ),
    "S1-1": (
        "\n## Template Responsibility Context (S1-1: Price Manipulation)\n"
        "The concern suggests '{price_function}' should validate or protect '{price_source}' "
        "against manipulation.\n"
        "Key delegation question: Is price validation the responsibility of an upstream oracle or "
        "price feed provider, not '{price_function}'? Does the contract merely consume a trusted "
        "price feed?"
    ),
    "S1-2": (
        "\n## Template Responsibility Context (S1-2: User Protective Bound)\n"
        "The concern suggests '{swap_function}' should enforce the route-specific user protective "
        "bound '{amount_parameter}'.\n"
        "Key delegation question: Does the caller/router already pass the exact equivalent bound "
        "for this path, such as min-out, max-input, deadline, or fixed tolerance? Does the contract "
        "delegate execution to a component that enforces that same bound before value moves?"
    ),
    "S5-3": (
        "\n## Template Responsibility Context (S5-3: Missing Access Control)\n"
        "The concern suggests '{privileged_function}' needs access control to protect "
        "'{critical_state}'.\n"
        "Key delegation question: Is access control enforced by a proxy contract, inherited "
        "AccessControl module, or external authorization system? The `initializer` modifier alone "
        "is a one-time execution gate, not proof of legitimate authorization."
    ),
}

FEASIBILITY_GUIDANCE = {
    "L1": (
        "\n## Template Scope Constraint: Reentrancy (L1)\n"
        "The template's role function is vulnerable_function='{vulnerable_function}'.\n"
        "You MUST assess whether '{vulnerable_function}' is accessible to external attackers.\n"
        "Do NOT substitute other functions as the attack entry point."
    ),
    "S1-1": (
        "\n## Template Scope Constraint: Price Manipulation (S1-1)\n"
        "The template's role functions are price_function='{price_function}' and "
        "dependent_operation='{dependent_operation}'.\n"
        "You MUST assess whether '{dependent_operation}' (which uses the manipulable price) "
        "is accessible to external attackers.\n"
        "Do NOT substitute other functions as the attack entry point."
    ),
    "S1-2": (
        "\n## Template Scope Constraint: Missing Slippage Protection (S1-2)\n"
        "The template's role function is swap_function='{swap_function}'.\n"
        "You MUST assess whether '{swap_function}' is accessible to external attackers.\n"
        "Do NOT substitute other functions as the attack entry point."
    ),
    "S5-3": (
        "\n## Template Scope Constraint: Missing Access Control (S5-3)\n"
        "The template's role function is privileged_function='{privileged_function}'.\n"
        "You MUST assess whether '{privileged_function}' is accessible to external attackers.\n"
        "Do NOT substitute other functions as the attack entry point."
    ),
}


# ── Small helpers over the target-side item dict ───────────────────────────
#
# `item` is the per-(target function, report) handoff record assembled from
# retrieval (Mret) + SMT witness (Msat). Required shape:
#   {
#     "target_contract": str, "target_function": str, "report_id": str,
#     "smt": {"route": {"template_id": str, "route_variant": str},
#             "witness": {"entry_function": str, "carrier_function": str,
#                         "path_nodes": [...]},
#             "m_ref_alignment": {...}},
#     "mechanism_slice": {"contract_name": str, "source_file": str,
#                          "functions": [{"name", "visibility",
#                          "state_mutability", "modifiers",
#                          "state_vars_read", "state_vars_written",
#                          "external_calls", "internal_calls", "called_by",
#                          "require_conditions", "assignments"}, ...],
#                          "target_causal_chain": {...}},
#     "entry_routes": {"entry_function", "visibility", "modifiers",
#                       "require_conditions", "called_by", ...},
#   }

def _flatten_unique(values: Iterable[Any]) -> List[str]:
    seen: set = set()
    out: List[str] = []
    for value in values:
        nested = value if isinstance(value, (list, tuple, set)) else [value]
        for item in nested:
            text = str(item).strip()
            if text and text not in seen:
                seen.add(text)
                out.append(text)
    return out


def _first_nonempty(*values: Any) -> str:
    for value in values:
        if isinstance(value, list):
            flat = _flatten_unique(value)
            if flat:
                return ", ".join(flat[:6])
        elif isinstance(value, dict):
            flat = _flatten_unique(value.values())
            if flat:
                return ", ".join(flat[:6])
        elif value:
            return str(value)
    return "not present in current target-side handoff"


def _format_with_roles(template: str, roles: Dict[str, str]) -> str:
    class RoleDict(dict):
        def __missing__(self, key: str) -> str:
            return "not present in current target-side handoff"

    return template.format_map(RoleDict(roles))


def _short_json(value: Any, limit: int = 2000) -> str:
    text = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)
    if len(text) <= limit:
        return text
    return text[: limit - 80] + "\n... [truncated; see full handoff record for complete JSON]"


def family_for_template(template_id: str) -> str:
    family = FAMILY_BY_TEMPLATE.get(template_id)
    if not family:
        raise HarmVerdictError(f"unsupported family for template: {template_id}")
    return family


def _functions(item: Dict[str, Any]) -> List[Dict[str, Any]]:
    return list((item.get("mechanism_slice") or {}).get("functions") or [])


def _carrier_function(item: Dict[str, Any]) -> Dict[str, Any]:
    carrier = ((item.get("smt") or {}).get("witness") or {}).get("carrier_function")
    funcs = _functions(item)
    for func in funcs:
        if func.get("name") == carrier:
            return func
    return funcs[0] if funcs else {}


def _all_of(item: Dict[str, Any], key: str) -> List[str]:
    return _flatten_unique(func.get(key) or [] for func in _functions(item))


AUTH_TERMS = (
    "owner", "admin", "govern", "timelock", "role", "auth", "keeper",
    "operator", "controller", "vault", "pool", "router", "strategy",
)


def _auth_guard_summary(modifiers: List[str], require_conditions: List[str]) -> str:
    guard_bits = modifiers + require_conditions
    auth_bits = [b for b in guard_bits if any(t in b.lower() for t in AUTH_TERMS)]
    if auth_bits:
        return "auth-like guard evidence: " + "; ".join(auth_bits[:6])
    if guard_bits:
        return "no authority guard; non-authority gates only: " + "; ".join(guard_bits[:6])
    return "no authority guard"


AUTHORITY_STATE_TERMS = (
    "role", "owner", "admin", "authority", "auth", "signer", "governance",
    "governor", "controller", "operator", "guardian", "pauser", "upgrader",
)
AUTHORITY_PRIMITIVE_TERMS = (
    "_grantrole", "_setroleadmin", "_setuprole", "_revokerole",
    "_transferownership", "transferownership", "setowner", "setadmin",
    "renounceownership", "grantrole", "setroleadmin",
)


def _contains_any(text: Any, terms: Iterable[str]) -> bool:
    lower = str(text or "").lower()
    return any(term in lower for term in terms)


def _authority_state_evidence(item: Dict[str, Any]) -> Dict[str, List[str]]:
    funcs = _functions(item)
    writes = _all_of(item, "state_vars_written")
    reads = _all_of(item, "state_vars_read")
    internal_calls = _all_of(item, "internal_calls")
    external_calls = _all_of(item, "external_calls")
    return {
        "authority_state_writes": [v for v in writes if _contains_any(v, AUTHORITY_STATE_TERMS)][:12],
        "authority_state_reads": [v for v in reads if _contains_any(v, AUTHORITY_STATE_TERMS)][:12],
        "authority_primitives": [
            c for c in internal_calls + external_calls if _contains_any(c, AUTHORITY_PRIMITIVE_TERMS)
        ][:12],
        "entry_modifiers": _flatten_unique(f.get("modifiers") or [] for f in funcs)[:12],
    }


def _public_mechanism_kind(route_variant: Optional[str]) -> str:
    mapping = {
        "external_call_state_reentrancy": "external interaction before later state settlement",
        "receiver_callback_reentrancy": "receiver/callback interaction before settlement",
        "spot_price_dependency": "spot or reserve-derived value dependency",
        "direct_balance_dependency": "balance-derived value dependency",
        "external_value_dependency": "external component value dependency",
        "reward_weight_dependency": "reward or stake-weight value dependency",
        "share_ratio_dependency": "share-ratio value dependency",
        "bootstrap_share_inflation": "initial share-ratio dependency",
        "direct_missing_min_out_execution": "asset execution without an observed output bound in the target slice",
        "missing_deadline_execution": "time-sensitive asset execution without an observed time-validity bound in the target slice",
        "fixed_tolerance_execution": "asset execution controlled by a fixed tolerance in the target slice",
        "direct_privileged_surface": "open privileged state-changing surface",
        "role_self_escalation_or_acl_bypass": "open path can mutate authority, role, or privileged-configuration state",
        "initializer_capture": "open path can mutate authority, role, or privileged-configuration state",
    }
    return mapping.get(route_variant or "", route_variant or "unknown mechanism kind")


def _neutral_mechanism_meaning(item: Dict[str, Any], family: str) -> str:
    route_variant = (item.get("smt") or {}).get("route", {}).get("route_variant")
    kind = _public_mechanism_kind(route_variant)
    tail = {
        "L1": "E4c must decide whether the delayed/stale state is consumed by a value, "
              "authority, or critical accounting consequence in this target business.",
        "S1-1": "E4c must decide whether this value dependency reaches a concrete "
                "attacker-beneficial and victim-adverse business effect, or only supports "
                "reporting, routing, synchronization, quoting, or local bookkeeping.",
        "S1-2": "E4c must decide whether the observed bound is the business-relevant bound "
                "for this operation and whether absence of that bound causes user-value loss.",
        "S5-3": "E4c must decide whether the written authority/configuration/protocol state "
                "is business-critical and externally abusable in this target context.",
    }.get(family, "")
    return f"Mechanism candidate: the witnessed target path has {kind}. {tail}".strip()


def route_roles(item: Dict[str, Any]) -> Dict[str, str]:
    """Extract the family-specific role slots used to fill SEVERITY/NECESSITY/
    FEASIBILITY_GUIDANCE templates (vulnerable_function, price_source, ...)."""
    smt = item["smt"]
    route = smt["route"]
    witness = smt["witness"]
    alignment = smt.get("m_ref_alignment") or {}
    family = family_for_template(route["template_id"])
    carrier = witness.get("carrier_function") or item["target_function"]
    entry = witness.get("entry_function") or item["target_function"]
    carrier_func = _carrier_function(item)
    state_written = _all_of(item, "state_vars_written")
    external_calls = _flatten_unique(
        [carrier_func.get("external_calls") or [], _all_of(item, "external_calls")]
    )
    require_conditions = _flatten_unique(f.get("require_conditions") or [] for f in _functions(item))
    modifiers = _flatten_unique(f.get("modifiers") or [] for f in _functions(item))

    if family == "L1":
        return {
            "vulnerable_function": carrier,
            "external_call": _first_nonempty(external_calls, carrier_func.get("internal_calls")),
            "state_variable": _first_nonempty(state_written),
        }
    if family == "S1-1":
        return {
            "price_function": carrier,
            "price_source": _first_nonempty(alignment.get("code_side_price_source_read_sources")),
            "dependent_operation": _first_nonempty(entry, carrier),
        }
    if family == "S1-2":
        slots = ((alignment.get("m_ref_best_function_condition") or {}).get("slots") or {})
        return {
            "swap_function": carrier,
            "amount_parameter": _first_nonempty(
                slots.get("amount_parameter"), slots.get("protected_object"), slots.get("value_anchor")
            ),
            "asset_operation": _first_nonempty(external_calls, carrier),
        }
    if family == "S5-3":
        authority = _authority_state_evidence(item)
        return {
            "privileged_function": carrier,
            "critical_state": _first_nonempty(
                authority["authority_state_writes"], authority["authority_state_reads"], state_written
            ),
            "authority_effect": _first_nonempty(
                authority["authority_primitives"], authority["authority_state_writes"]
            ),
            "authority_guard": _auth_guard_summary(modifiers, require_conditions),
        }
    raise HarmVerdictError(f"unhandled family: {family}")


# ── Family-specific boundary rules (verbatim from the production harness) ──

_COMMON_BOUNDARY_RULES = [
    "The upstream structural stage only grounds a mechanism candidate. E4c must still judge business harm using target-side business evidence.",
    "Do not use report text or offline labels. Do not invent missing proxy/oracle/router facts.",
    "A public/external entry alone proves possible calling, not business harm. SEVERITY must still find a target-side value/state/authority consequence.",
    "Business harm requires a source-to-sink chain inside the mechanism slice: the witnessed mechanism source/carrier must connect to target-side consumer context or effect sinks such as asset movement, state-changing accounting update, authority effect, liquidation/borrow/mint/burn/reward effect, or an equivalent irreversible consequence.",
    "FEASIBILITY cannot create harm that SEVERITY did not prove; if the only evidence is that a function is public/external, the condition is not sufficient for vulnerable.",
]

_FAMILY_BOUNDARY_RULES = {
    "S5-3": [
        "For S5-3, an open unauthorized privileged operation that writes persistent protocol state is real severity even without an immediate token transfer.",
        "For S5-3, target-side calls such as grantRole, setRoleAdmin, setupRole, revokeRole, transferOwnership, setOwner, or setAdmin are authority-state harm sinks when reachable without an owner/admin/timelock guard.",
        "For S5-3, authority capture, role-admin mutation, ownership transfer, signer/admin assignment, or privileged configuration control is itself business harm. Do NOT require a separate asset transfer, mint, burn, liquidation, or user-value sink.",
        "For an open privileged operational action, do NOT downgrade to governance_operational_risk merely because the written variable is upgrade, migration, lifecycle, deployment, or configuration state.",
        "An initializer/reinitializer modifier is a one-time lifecycle gate. It is not an owner/admin/timelock authorization guard, and it does not by itself prove or disprove severity. Judge severity from authority or privileged-state effects, then judge triggerability in FEASIBILITY.",
        "Do not claim proxy/wrapper/deployment-system delegation unless the target-side slice explicitly shows an authorization layer for this exact initializer or privileged function.",
    ],
    "S1-1": [
        "For S1-1, upstream_oracle_responsibility is valid only for explicit trusted oracle/TWAP/feed validation shown in target-side evidence.",
        "Do NOT classify raw balanceOf(address(this)), target totalAssets/totalSupply/share-ratio math, bootstrap share inflation, or reward accounting as upstream oracle responsibility.",
        "If the witness function is a helper/view/validation/quote predicate with no state write, asset movement, liquidation execution, mint/burn, borrow/withdraw, reward transfer, target-side consumer context, or state-changing sink, SEVERITY must be false as helper_only/view_only even if it reads a manipulable price.",
        "Exception: a view/helper valuation carrier is not helper_only when target-side called_by or consumer context includes ERC4626/vault/lending user-value operations such as previewDeposit, previewMint, previewRedeem, previewWithdraw, convertToShares, convertToAssets, mint, withdraw, redeem, borrow, repay, liquidate, seize.",
        "For any S1-1 route, SEVERITY must identify the victim-adverse delta: attacker receives extra assets/shares/rewards, pays less debt/collateral, causes unfair liquidation, or corrupts accounting used for user value. If the sink only reports, synchronizes, routes, or rebalances protocol-owned/user-requested funds with no target-side attacker profit or victim loss, return false as workflow_no_profit_path or no_value_sink.",
        "For S1-1, return false as self_claim_no_victim or no_value_sink when the same target path appears self-balanced: the caller's received value and required payment/collateral/fees/settlement amount are computed together from current balances or actual execution results, and the slice does not show cross-user entitlement corruption, protocol underpayment, or victim-adverse accounting.",
        "For dedicated RiskEngine/Oracle/Router/Pool/Bridge/VaultController validation calls, NECESSITY is false as downstream_pool_responsibility or upstream_oracle_responsibility unless the target-side slice shows the target bypasses, ignores, or corrupts that returned protection.",
    ],
    "S1-2": [
        "For S1-2, missing min-out harm applies to exact-input user asset execution with variable output.",
        "For direct_missing_min_out_execution, asset transfer plus an absent min_out name is not sufficient. SEVERITY requires a user-value equation where a caller commits input or shares and can receive an adversarially worse output, overpay input, or lose claim value because the target path lacks the relevant bound.",
        "For missing_deadline_execution, do NOT require the same min-out style asymmetric output proof. The severity question is whether a user-authorized asset/market action can execute after its intended time-validity window, reaching swap, liquidation, repayment, collateral, transfer, or accounting sinks without an equivalent deadline.",
        "For S1-2, structured bound parameters such as minAmountOut/minShares/minAssets/maxAssetsIn/maxSharesOut/deadline/slippage are business-protection evidence. If the route says the relevant bound is missing, but target-side signature/evidence includes the equivalent bound for the operation direction, NECESSITY must be false as equivalent_protection.",
        "For exact-output functions, the relevant protection is max-input/overpayment, not min_out. If the route only asserts missing min_out for an exact-output flow, SEVERITY must be false as wrong_operation unless target-side evidence separately shows unbounded input loss.",
        "If caller/router supplies equivalent slippage/deadline protection for this exact path, NECESSITY must be false.",
        "A swap-like name is not enough; SEVERITY requires concrete user value loss through the target-side asset path.",
    ],
    "L1": [
        "For L1, external call before state update is not enough. SEVERITY requires the delayed/stale state or settlement effect to connect through the mechanism slice to value, authority, repeated claim/mint/redeem, or critical accounting consequence.",
        "For L1, refund/cooldown/last-claim/withdrawn/reward checkpoint variables are critical accounting sinks when the external interaction happens before the marker is updated and the marker controls repeated refund, claim, stake/delegate, reward, or withdrawal eligibility. Do not require a separate token transfer if the stale marker itself enables repeated value or accounting claims.",
        "NECESSITY must not contradict the SMT witness by re-deciding that the state update happens before the witnessed callback/external interaction; only target-side business-equivalent protection outside the SMT witness can make NECESSITY false.",
        "Deployment, governance, orchestration, or process bookkeeping without value-relevant stale-state reuse should fail SEVERITY.",
        "Calls into executor/timelock/governance orchestration are not automatically attacker-controlled callbacks. Keep SMT's witness as real, but business severity still requires a target-side stale-state consequence, not only the existence of an external call.",
        "Factory creation, queueing, proposal lifecycle, executor scheduling, registry updates, and process counters are process bookkeeping unless the same target-side slice proves direct asset extraction, authority capture, or value-bearing accounting corruption.",
    ],
}


def _semantic_boundary_rules(family: str) -> str:
    rules = list(_COMMON_BOUNDARY_RULES) + list(_FAMILY_BOUNDARY_RULES.get(family, []))
    return _short_json({"family": family, "rules": rules}, limit=1700)


# ── Evidence assembly (target-side context blocks, no report text/labels) ──

def _contract_business_summary(item: Dict[str, Any]) -> str:
    mechanism_slice = item["mechanism_slice"]
    entry_routes = item.get("entry_routes") or {}
    funcs = _functions(item)
    func_names = [str(f.get("name")) for f in funcs if f.get("name")]
    external_components = _flatten_unique(f.get("external_calls") or [] for f in funcs)
    state_writes = _all_of(item, "state_vars_written")
    state_reads = _all_of(item, "state_vars_read")
    guards = _flatten_unique(
        [entry_routes.get("modifiers") or [], entry_routes.get("require_conditions") or []]
    )
    return "\n".join(
        [
            f"Contract: {item['target_contract']} ({mechanism_slice.get('source_file')})",
            f"Target function: {item['target_function']}",
            f"Mechanism witness entry/carrier: {item['smt']['witness'].get('entry_function')} / "
            f"{item['smt']['witness'].get('carrier_function')}",
            f"Entry visibility/modifiers: {entry_routes.get('visibility')} / {entry_routes.get('modifiers') or []}",
            f"Bounded anchor functions: {', '.join(func_names[:8]) or 'not present'}",
            f"Observed external components/calls: {', '.join(external_components[:8]) or 'not present'}",
            f"Observed state writes: {', '.join(state_writes[:8]) or 'not present'}",
            f"Observed state reads: {', '.join(state_reads[:8]) or 'not present'}",
            f"Observed guards/workflow checks: {', '.join(guards[:8]) or 'not present'}",
            "This summary is target-only. It contains no report text, report-derived path, offline "
            "label, or SMT proof dump.",
        ]
    )


def _deep_business_analysis(item: Dict[str, Any], roles: Dict[str, str]) -> str:
    funcs = [
        {
            "name": f.get("name"), "visibility": f.get("visibility"),
            "state_mutability": f.get("state_mutability"), "modifiers": f.get("modifiers") or [],
            "state_vars_read": f.get("state_vars_read") or [], "state_vars_written": f.get("state_vars_written") or [],
            "external_calls": f.get("external_calls") or [], "internal_calls": f.get("internal_calls") or [],
            "called_by": f.get("called_by") or [], "require_conditions": f.get("require_conditions") or [],
        }
        for f in _functions(item)
    ]
    analysis = {
        "mechanism_roles": roles,
        "bounded_anchor_functions": funcs,
        "interpretation_limit": (
            "These are bounded target-code observations for business reasoning. They are not a "
            "vulnerability verdict and do not include report-derived evidence."
        ),
    }
    return _short_json(analysis, limit=1900)


def _anchor_function_intents_text(item: Dict[str, Any]) -> str:
    lines = []
    for func in _functions(item):
        called_by = func.get("called_by") or []
        line = f"- {func.get('name')} ({func.get('visibility') or 'unknown'}, {func.get('state_mutability') or 'unknown'}"
        if called_by:
            line += f", called by: {', '.join(map(str, called_by[:5]))}"
        line += ")"
        reads = _first_nonempty(func.get("state_vars_read") or [])
        writes = _first_nonempty(func.get("state_vars_written") or [])
        calls = _first_nonempty(func.get("external_calls") or [], func.get("internal_calls") or [])
        lines.append(f"{line}: reads [{reads}], writes [{writes}], calls [{calls}].")
    return "\n".join(lines) or "No anchor functions present in current target-side handoff."


def _anchor_compact_graph(item: Dict[str, Any]) -> str:
    summaries = [
        {
            "name": f.get("name"), "visibility": f.get("visibility"),
            "called_by": (f.get("called_by") or [])[:5],
            "internal_calls": (f.get("internal_calls") or [])[:8],
            "external_calls": (f.get("external_calls") or [])[:8],
            "state_reads": (f.get("state_vars_read") or [])[:8],
            "state_writes": (f.get("state_vars_written") or [])[:8],
        }
        for f in _functions(item)
    ]
    return _short_json({"bounded_anchor_function_summaries": summaries}, limit=1900)


def _vulnerability_evidence_chain(item: Dict[str, Any], family: str, roles: Dict[str, str]) -> str:
    witness = item["smt"]["witness"]
    chain = {
        "status": "upstream structural grounding found this target-side mechanism candidate; this is not a business-harm verdict",
        "family": family,
        "mechanism_kind": _public_mechanism_kind(item["smt"]["route"].get("route_variant")),
        "neutral_mechanism_meaning": _neutral_mechanism_meaning(item, family),
        "witness_binding": {
            "entry_function": witness.get("entry_function"),
            "carrier_function": witness.get("carrier_function"),
            "path_nodes": witness.get("path_nodes") or [],
        },
        "mechanism_roles": roles,
    }
    return "## Target-Side Mechanism Hypothesis (Not a Business-Harm Verdict)\n" + _short_json(chain, limit=1750)


def _condition_evidence(item: Dict[str, Any], condition: str) -> str:
    entry_routes = item.get("entry_routes") or {}
    witness = item["smt"]["witness"]
    base: Dict[str, Any] = {
        "condition": condition.upper(),
        "witness_path": witness.get("path_nodes") or [],
        "mechanism_kind": _public_mechanism_kind(item["smt"]["route"].get("route_variant")),
    }
    if condition == "severity":
        base["target_effect_context"] = {
            "state_reads": _all_of(item, "state_vars_read")[:8],
            "state_writes": _all_of(item, "state_vars_written")[:8],
            "external_calls": _all_of(item, "external_calls")[:8],
            "internal_calls": _all_of(item, "internal_calls")[:8],
            "authority_effects": _authority_state_evidence(item),
            "note": "Use these target-code effects to decide whether the mechanism reaches real "
                    "user-value, accounting, authority, or asset consequences.",
        }
    elif condition == "necessity":
        base["responsibility_context"] = {
            "modifiers": _all_of(item, "modifiers")[:12],
            "require_conditions": _all_of(item, "require_conditions")[:12],
            "note": "Use this to decide whether protection responsibility belongs to this target "
                    "path or to an equivalent/delegated component.",
        }
    elif condition == "feasibility":
        base["trigger_context"] = {
            "entry_function": entry_routes.get("entry_function"),
            "visibility": entry_routes.get("visibility"),
            "modifiers": entry_routes.get("modifiers") or [],
            "require_conditions": entry_routes.get("require_conditions") or [],
            "called_by": entry_routes.get("called_by") or [],
            "note": "Use this to decide whether an ordinary attacker can trigger the "
                    "already-harmful mechanism in the target business state machine.",
        }
    else:
        raise HarmVerdictError(f"unknown condition evidence: {condition}")
    return _short_json(base, limit=2000)


# ── Per-condition "first-principles test" + output schema ─────────────────
# (verbatim numbered checklists and JSON schemas from the production harness)

_SEVERITY_TEST = """First-principles test:
1. Start from applicable=false. The upstream structural stage only grounds a mechanism hypothesis; it does not establish business harm.
2. Set applicable=true only after target-side evidence proves concrete fund loss, unfair value exchange, corrupted user-value accounting, authority capture, or irreversible critical-state corruption.
3. Return false for helper/view/quote/display-only paths only when there is no target-side consumer/effect sink. Do not discard a view/internal carrier that feeds a bounded mint/deposit/withdraw/redeem/borrow/liquidation/swap/reward/accounting consumer.
4. For authority mechanisms, authority/role/owner/admin/signer/privileged-configuration mutation is a concrete harm sink when not protected by an owner/admin/timelock guard. Do not require a separate token transfer.
5. For non-authority mechanisms, identify the concrete target-side sink that consumes the witnessed source. If no same-slice sink exists, return false; do not postpone this to FEASIBILITY.
6. For value-measurement routes, name the attacker-beneficial and victim-adverse delta. A user-value function name is not enough: prove that the witnessed measurement gives the attacker more claim/assets/rewards, less required payment/debt/collateral, unfair liquidation, or cross-user/protocol accounting corruption.
7. Return false when the same target path appears self-balanced: the caller's received value and required payment/collateral/fees/settlement amount are computed together from current balances, and no cross-user entitlement corruption, protocol underpayment, or victim-adverse accounting is shown.
8. If the mechanism only changes a protocol workflow, report, route, synchronization state, or self-balanced settlement without target-side profit/loss evidence, return false.
9. A reason that only says "could", "may", "potentially", "can lead to", "enabling", or "risk" without naming the concrete sink and delta is insufficient and must return applicable=false."""

_NECESSITY_TEST = """First-principles test:
1. Determine whether this target contract is responsible for the missing protection.
2. Return false if target-side evidence shows equivalent protection already exists, protection responsibility is delegated to an underlying contract/oracle/router, or the architecture makes this exact protection irrelevant.
3. Do not infer protection from report text or labels. Use only modifiers, require conditions, callers/callees, state writes, and route roles.
4. Do not re-decide SMT-proven mechanism existence. NECESSITY may not claim an equivalent protection that directly contradicts the SMT witness or route facts.
5. Equivalent protection must protect the exact missing business condition, such as a user amount bound for a swap path or an explicit trusted oracle/TWAP/feed for a price path.
6. For dedicated validation components such as RiskEngine, oracle, router, pool, bridge, or vault controller, decide whether the target is merely consuming their protection. If so, return false unless the target-side slice shows this function bypasses or invalidates that protection.
7. Equivalent protection or delegated responsibility makes NECESSITY false. Self-balanced settlement without a victim-adverse delta should already fail SEVERITY; do not turn it into vulnerable merely because the entry is public or a user-value operation exists."""

_FEASIBILITY_TEST = """First-principles test:
1. Decide whether an external attacker can trigger the exact witness entry/carrier/path in this target business model.
2. Public/external functions are attacker-triggerable unless target-side guards prove otherwise.
3. Internal functions must be judged through their listed callers; do not mark internal functions safe solely because they are internal.
4. Admin/governance/timelock-only gates block ordinary attackers; protocol-internal caller roles (onlyController/onlyPool/onlyKeeper/onlyVault/onlyRouter/onlyStrategy) do NOT automatically block attacker access because attackers may enter through those protocols.
5. State-machine or workflow gates such as prerequisite-funds-received checks, cross-chain synchronization guards, required protocol phases, or allocation-completion flags are not "no guard"; require target-side evidence that an attacker can satisfy them.
6. If the only feasibility evidence is public/external visibility plus an assumed ability to satisfy a workflow gate, return false as no_concrete_path.
7. Do not use FEASIBILITY to repair a missing source-to-sink harm chain; if there is no proved harmful sink, the correct failure is earlier SEVERITY, not FEASIBILITY=true."""


def _condition_reasoning(item: Dict[str, Any], condition: str, family: str, roles: Dict[str, str]) -> str:
    boundary = _semantic_boundary_rules(family)
    if condition == "severity":
        guidance = _format_with_roles(SEVERITY_GUIDANCE[family], roles)
        return (
            f"{guidance}\n\nEvaluate only SEVERITY now.\n\n{_SEVERITY_TEST}\n\n"
            "## Binding Mechanism Boundary Rules\n"
            "These rules override the generic template context above. If a boundary rule says to "
            "return false, you MUST return false even when the function is public/external and the "
            f"mechanism hypothesis is structurally grounded.\n{boundary}\n\n"
            "Output consistency is mandatory:\n"
            '- If applicable=true, failed_condition MUST be "NONE" and sub_reason MUST be "none".\n'
            '- If applicable=false, failed_condition MUST be "SEVERITY" and sub_reason MUST name the '
            "first severity failure.\n\n"
            'Return a single compact JSON object only. Start with "{" as the first character and end '
            'with "}". Do not include markdown, prose, or hidden reasoning.\n'
            '{"applicable": true/false, "failed_condition": "NONE"/"SEVERITY", "sub_reason": '
            '"none/dos_revert/negligible_impact/consequence_unreachable/governance_operational_risk/'
            'design_parameter/view_only/helper_only/no_value_sink/wrong_operation/self_claim_no_victim/'
            'workflow_no_profit_path", "reason": "one sentence", "evidence_refs": '
            '["witness/function/state references only"]}'
        )
    if condition == "necessity":
        guidance = _format_with_roles(NECESSITY_GUIDANCE[family], roles)
        return (
            f"{guidance}\n\nEvaluate only NECESSITY now. The concern has passed SEVERITY.\n\n"
            f"{_NECESSITY_TEST}\n\n"
            "## Binding Mechanism Boundary Rules\n"
            "These rules override the generic template context above. Equivalent protection or "
            "delegated responsibility makes NECESSITY false even when the mechanism hypothesis is "
            f"structurally grounded.\n{boundary}\n\n"
            "Output consistency is mandatory:\n"
            '- If applicable=true, failed_condition MUST be "NONE" and sub_reason MUST be "none".\n'
            '- If applicable=false, failed_condition MUST be "NECESSITY" and sub_reason MUST name the '
            "first responsibility/protection failure.\n\n"
            'Return a single compact JSON object only. Start with "{" as the first character and end '
            'with "}". Do not include markdown, prose, or hidden reasoning.\n'
            '{"applicable": true/false, "failed_condition": "NONE"/"NECESSITY", "sub_reason": '
            '"none/wrapper_delegation/equivalent_protection/architecture_mismatch/'
            'upstream_oracle_responsibility/downstream_pool_responsibility/user_bound_protection/'
            'downstream_router_protection", "reason": "one sentence", "evidence_refs": '
            '["witness/function/state references only"]}'
        )
    if condition == "feasibility":
        guidance = _format_with_roles(FEASIBILITY_GUIDANCE[family], roles)
        return (
            f"{guidance}\n\nEvaluate only FEASIBILITY now. The concern has passed SEVERITY and "
            f"NECESSITY.\n\n{_FEASIBILITY_TEST}\n\n"
            "## Binding Mechanism Boundary Rules\n"
            "These rules override the generic template context above. Public/external visibility "
            "alone is never sufficient when a workflow/business gate or missing harm chain "
            f"remains.\n{boundary}\n\n"
            "Output consistency is mandatory:\n"
            '- If applicable=true, failed_condition MUST be "NONE" and sub_reason MUST be "none".\n'
            '- If applicable=false, failed_condition MUST be "FEASIBILITY" and sub_reason MUST name '
            "the first trigger/access failure.\n\n"
            'Return a single compact JSON object only. Start with "{" as the first character and end '
            'with "}". Do not include markdown, prose, or hidden reasoning.\n'
            '{"applicable": true/false, "failed_condition": "NONE"/"FEASIBILITY", "sub_reason": '
            '"none/admin_restricted/wrong_operation/business_model_mismatch/no_concrete_path/'
            'not_externally_accessible", "reason": "one sentence", "evidence_refs": '
            '["witness/function/state references only"]}'
        )
    raise HarmVerdictError(f"unknown condition: {condition}")


CONDITION_ORDER = ("severity", "necessity", "feasibility")


def build_condition_prompt(item: Dict[str, Any], condition: str) -> str:
    """Build the full prompt text for one condition ("severity", "necessity",
    or "feasibility") given a target-side handoff item. See the module
    docstring for the required `item` shape."""
    route = item["smt"]["route"]
    family = family_for_template(route["template_id"])
    roles = route_roles(item)
    return f"""You are a smart contract security auditor running MechaAudit's Harm Verdict stage.

The upstream structural stage has grounded a target-side mechanism hypothesis. Do NOT re-check mechanism existence.
The mechanism hypothesis is not a vulnerability verdict. You must independently decide business harm.
Do NOT replace witness functions or move to another function.
Do NOT use report text, report-derived paths, benchmark labels, or offline evaluation fields.
Return only the requested compact JSON object.

{_vulnerability_evidence_chain(item, family, roles)}

## Contract Business Context
{_contract_business_summary(item)}

## Deep Business Analysis (from target source/PDG only)
{_deep_business_analysis(item, roles)}

## Anchor Function Purpose
{_anchor_function_intents_text(item)}

## Anchor Function Code Structure (from PDG static analysis)
{_anchor_compact_graph(item)}

NOTE ON INTERNAL FUNCTIONS: Anchor functions marked as internal are implementation details invoked by public/external callers. Evaluate accessibility based on the callers' visibility and access controls, not only the anchor function's own visibility.

## Condition-Specific Target Evidence
{_condition_evidence(item, condition)}

{_condition_reasoning(item, condition, family, roles)}
"""


def build_condition_prompts(item: Dict[str, Any]) -> Dict[str, str]:
    """Build all three condition prompts for one target-side handoff item."""
    return {condition: build_condition_prompt(item, condition) for condition in CONDITION_ORDER}


def parse_condition_response(llm_response: str) -> Optional[Dict[str, Any]]:
    """Parse one condition's JSON verdict: {applicable, failed_condition,
    sub_reason, reason, evidence_refs}. Returns None if not valid JSON."""
    try:
        obj = json.loads(llm_response)
    except (json.JSONDecodeError, TypeError):
        return None
    if "applicable" not in obj:
        return None
    return obj


def run_harm_verdict_chain(item: Dict[str, Any], call_llm) -> Tuple[str, Dict[str, Any]]:
    """Run the full serial SEVERITY -> NECESSITY -> FEASIBILITY chain.

    Args:
        item: target-side handoff record; see the module docstring for the
            required shape.
        call_llm: callable(prompt: str) -> str, sends the prompt to an LLM
            endpoint and returns the raw text response.

    Returns:
        (verdict, trace) where verdict is "VULN" or "SAFE", and trace is a
        dict {condition_name: parsed_response} for every condition actually
        evaluated (the chain stops at the first failing or unparsable
        condition).
    """
    trace: Dict[str, Any] = {}
    for condition in CONDITION_ORDER:
        prompt = build_condition_prompt(item, condition)
        response_text = call_llm(prompt)
        parsed = parse_condition_response(response_text)
        trace[condition.upper()] = parsed
        if parsed is None or not parsed.get("applicable", False):
            return "SAFE", trace
    return "VULN", trace
