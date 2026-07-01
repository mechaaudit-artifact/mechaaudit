"""
MDL mechanism matching.

match(P(f), R(r)) = pi_match(S_f, R_f, S_r, R_r) AND condition_match(T_f, C_r)

  - pi_match:         grounded operation set + relation pair matching
  - condition_match:  condition template matching (17 templates)

Both sides are label-blind: no ground-truth label is consulted.
"""

from typing import Optional, Set, Tuple, List
from .primitives import (
    MDLCondition,
    CONDITION_TEMPLATES,
    TEMPLATE_IDS,
    SUB_DIRECTION_CORE,
    parse_condition_list,
)


# ── Helper functions ──────────────────────────────────────────────────────────

def _extract_op_names(s_list: list) -> Set[str]:
    return {op["name"] for op in s_list if isinstance(op, dict) and op.get("name")}


def _extract_relation_pairs(r_list: list) -> Set[Tuple[str, str]]:
    return {(r["op_a"], r["op_b"]) for r in r_list
            if isinstance(r, dict) and r.get("op_a") and r.get("op_b")}


def _get_core_ops_for_report(report_mdl: dict) -> List[Set[str]]:
    """Determine candidate CORE operation sets for a report.

    Returns a list of CORE sets, one per candidate sub-direction.
    Matching succeeds if ANY one CORE set is fully present in S_f.
    """
    sub_dir = report_mdl.get("sub_direction", "")
    if sub_dir and sub_dir in SUB_DIRECTION_CORE:
        return [SUB_DIRECTION_CORE[sub_dir]]

    template_ids = set(report_mdl.get("template_ids", []))
    if not template_ids:
        return [set()]

    template_to_subdirs = {
        "C-L1a": ["l1_callback_state_finalization", "l1_nft_receiver_callback"],
        "C-L1b": ["l1_callback_state_finalization"],
        "C-L1d": ["l1_callback_state_finalization"],
        "C-S11a": ["s1_1_reserve_direct_manipulation", "s1_1_market_derived_oracle_window"],
        "C-S11b": ["s1_1_bootstrap_share_inflation"],
        "C-S11c": ["s1_1_reserve_direct_manipulation"],
        "C-S11d": ["s1_1_share_total_assets_distortion", "s1_1_reserve_direct_manipulation"],
        "C-S12a": ["s1_2_disabled_price_time_boundary"],
        "C-S12b": ["s1_2_disabled_price_time_boundary"],
        "C-S12c": ["s1_2_hardcoded_slippage_threshold"],
        "C-S12d": ["s1_2_missing_min_guard_on_asset_op"],
        "C-S53a": ["s5_3_missing_gate_on_privileged"],
        "C-S53b": ["s5_3_privileged_auth_bypass"],
        "C-S53c": ["s5_3_missing_trusted_caller_auth"],
        "C-S53d": ["s5_3_privileged_auth_bypass"],
        "C-S53e": ["s5_3_initializer_admin_capture"],
    }

    candidates = []
    for tid in template_ids:
        for sd in template_to_subdirs.get(tid, []):
            sd_core = SUB_DIRECTION_CORE.get(sd, set())
            if sd_core:
                candidates.append(sd_core)
    return candidates if candidates else [set()]


def _templates_from_ids(template_ids: list) -> Set[str]:
    return {t for t in template_ids if t in TEMPLATE_IDS}


def _predicates_to_templates(predicates: list) -> Set[str]:
    templates = set()
    for tid, info in CONDITION_TEMPLATES.items():
        for pred in info.get("predicates", []):
            if pred in predicates:
                templates.add(tid)
    return templates


# ── pi_match ──────────────────────────────────────────────────────────────────

def pi_match(
    s_f: list, r_f: list,
    s_r: list, r_r: list,
    report_mdl: dict = None,
) -> Optional[dict]:
    """Match operation sets (S) and relation pairs (R).

    Logic:
      1. All CORE ops from the report's mechanism direction must be present in S_f.
      2. At least one vocabulary op must overlap between S_f and S_r.
      3. Relation pair overlap provides additional evidence (not required).
    """
    ops_f = _extract_op_names(s_f)
    ops_r = _extract_op_names(s_r)

    if not ops_r:
        return None

    s_inter = ops_f & ops_r

    core_candidates = _get_core_ops_for_report(report_mdl) if report_mdl else [set()]

    best_core: Set[str] = set()
    core_satisfied = False
    for core_set in core_candidates:
        if not core_set:
            core_satisfied = True
            break
        if core_set <= ops_f:
            core_satisfied = True
            best_core = core_set
            break

    if not core_satisfied:
        return None

    if not s_inter:
        return None

    rels_f = _extract_relation_pairs(r_f)
    rels_r = _extract_relation_pairs(r_r)
    r_inter = rels_f & rels_r

    return {
        "s_f": sorted(ops_f),
        "s_r": sorted(ops_r),
        "s_intersection": sorted(s_inter),
        "core_satisfied": sorted(best_core),
        "r_intersection": sorted([list(p) for p in r_inter]),
        "s_overlap_ratio": len(s_inter) / len(ops_r) if ops_r else 0,
    }


# ── condition_match ────────────────────────────────────────────────────────────

def condition_match(
    t_f_templates: Set[str],
    c_r_templates: Set[str],
    t_f_conds: list = None,
    c_r_conds: list = None,
) -> Optional[dict]:
    """Match condition templates (at least one template must overlap)."""
    if not c_r_templates:
        return None

    template_inter = t_f_templates & c_r_templates
    if not template_inter:
        return None

    predicate_matches = []
    if t_f_conds and c_r_conds:
        for cr in c_r_conds:
            for tf in t_f_conds:
                if tf.predicate == cr.predicate:
                    predicate_matches.append({
                        "func": repr(tf), "report": repr(cr),
                        "exact_state": tf.state == cr.state,
                    })

    return {
        "template_intersection": sorted(template_inter),
        "template_names": [CONDITION_TEMPLATES[t]["name"] for t in sorted(template_inter)],
        "predicate_matches": predicate_matches,
    }


# ── Combined match ─────────────────────────────────────────────────────────────

def match_function_report(func_mdl: dict, report_mdl: dict) -> Optional[dict]:
    """Full mechanism match: pi_match AND condition_match.

    Returns a match evidence dict on success, None on failure.
    Checks all function traces; succeeds if any trace matches.
    """
    traces = func_mdl.get("traces", [{
        "s_f": func_mdl.get("s_f", []),
        "r_f": func_mdl.get("r_f", []),
        "t_f_templates": func_mdl.get("template_ids", []),
        "t_f": func_mdl.get("c_f", []),
    }])

    s_r = report_mdl.get("s_r", [])
    r_r = report_mdl.get("r_r", [])
    c_r_templates = _templates_from_ids(report_mdl.get("template_ids", []))
    c_r_conds = parse_condition_list(report_mdl.get("c_r", []))

    if not c_r_templates and c_r_conds:
        c_r_templates = _predicates_to_templates([c.predicate for c in c_r_conds])

    if not s_r and report_mdl.get("pi_r"):
        pi_r = report_mdl["pi_r"]
        s_r = [{"name": op.get("op", "")} for op in pi_r
               if isinstance(op, dict) and op.get("op")]

    for trace in traces:
        s_f = trace.get("s_f", [])
        r_f = trace.get("r_f", [])

        t_f_templates = _templates_from_ids(trace.get("t_f_templates", []))
        t_f_conds = parse_condition_list(trace.get("t_f", []))

        if not t_f_templates and t_f_conds:
            t_f_templates = _predicates_to_templates([c.predicate for c in t_f_conds])

        if not s_f and trace.get("pi_f"):
            pi_f = trace["pi_f"]
            s_f = [{"name": op.get("op", "")} for op in pi_f
                   if isinstance(op, dict) and op.get("op")]

        pi_ev = pi_match(s_f, r_f, s_r, r_r, report_mdl=report_mdl)
        if pi_ev is None:
            continue

        cond_ev = condition_match(t_f_templates, c_r_templates, t_f_conds, c_r_conds)
        if cond_ev is None:
            continue

        return {
            "matched": True,
            "pi_evidence": pi_ev,
            "condition_evidence": cond_ev,
        }

    return None
