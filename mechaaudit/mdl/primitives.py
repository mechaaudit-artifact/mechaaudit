"""
MDL (Mechanism Description Language) primitives.

MDL represents a vulnerability mechanism as a triple M = (pi_r, C_r, tau_r):
  - pi_r: Operation set drawn from OPERATION_VOCAB
  - C_r:  Condition set drawn from CONDITION_TEMPLATES
  - tau_r: Adversarial trigger description (natural language, not used in matching)

Both report-side (from audit findings) and contract-side (from PDG extraction)
representations use the same vocabulary, enabling semantic comparison.
"""

import re
from dataclasses import dataclass, field
from typing import Optional, Dict, Set


# ── Operation Vocabulary ──────────────────────────────────────────────────────
#
# Shared between report-side MDL extraction and contract-side PDG analysis.
# Induced from 394 audited findings across four mechanism families.
# Both sides project code semantics into this vocabulary for matching.

OPERATION_VOCAB: Dict[str, str] = {
    "outbound_asset_transfer":    "sending assets to external address (transfer, send, call{value})",
    "nft_safe_interaction":       "NFT mint/transfer triggering receiver callback (_safeMint, safeTransferFrom)",
    "cross_contract_state_read":  "reading state from another contract mid-update (read-only reentrancy)",
    "share_ratio_computation":    "computing shares/assets ratio where denominator can be near zero",
    "spot_price_read":            "reading price from manipulable source (AMM reserves, slot0, balanceOf)",
    "oracle_window_read":         "reading price from time-windowed oracle (TWAP, exchangeRateStored)",
    "direct_balance_dependency":  "contract accounting depends on balanceOf(this) directly (donation attack)",
    "reward_weight_computation":  "computing stake weight or reward base from manipulable input",
    "exchange_execution":         "swap/liquidity operation needing price-time boundary protection",
    "asset_value_operation":      "non-swap asset operation whose output depends on external price (vault deposit/mint/redeem)",
    "role_assignment":            "assigning admin/owner role during initialization",
    "privileged_state_mutation":  "modifying protocol parameters or critical state (setRate, pause, rescue)",
    "protocol_internal_call":     "function meant to be called only by specific protocol components (onlyRouter target)",
    "role_modification":          "changing role assignments or permission delegation",
    "delegated_action":           "operating on behalf of another user (transferFrom, withdraw-for, claim-for)",
    "asset_withdrawal":           "user withdrawing assets from protocol (withdraw, redeem, repay)",
    "asset_deposit":              "user depositing assets into protocol (deposit, supply, stake)",
    "reward_claim":               "claiming rewards or earnings (claim, distribute, harvest)",
    "asset_swap":                 "exchanging one asset for another (swap, trade)",
    "token_mint":                 "minting tokens or NFTs",
    "settlement":                 "settling/finalizing an order or auction",
    "governance_execute":         "governance or batch execution (DAO.execute, multisig)",
    "lending_operation":          "lending/borrowing operations (lend, borrow, repay)",
    "none_applicable":            "step describes attack behavior, not a code operation — skip",
}

VOCAB_OPS: Set[str] = set(OPERATION_VOCAB.keys()) - {"none_applicable"}


# Mechanism-essential operations per sub-direction.
# Matching requires that at least one CORE operation be present on both sides.
SUB_DIRECTION_CORE: Dict[str, Set[str]] = {
    "l1_callback_state_finalization":    {"outbound_asset_transfer"},
    "l1_nft_receiver_callback":          {"nft_safe_interaction"},
    "l1_read_only_reentrancy":           {"cross_contract_state_read"},
    "s1_1_bootstrap_share_inflation":    {"share_ratio_computation"},
    "s1_1_reserve_direct_manipulation":  {"spot_price_read"},
    "s1_1_market_derived_oracle_window": {"oracle_window_read"},
    "s1_1_share_total_assets_distortion": {"direct_balance_dependency"},
    "s1_1_stake_weight_reward_base":     {"reward_weight_computation"},
    "s1_2_disabled_price_time_boundary": {"exchange_execution"},
    "s1_2_hardcoded_slippage_threshold": {"exchange_execution"},
    "s1_2_missing_min_guard_on_asset_op": {"asset_value_operation"},
    "s5_3_initializer_admin_capture":    {"role_assignment"},
    "s5_3_missing_gate_on_privileged":   {"privileged_state_mutation"},
    "s5_3_missing_trusted_caller_auth":  {"protocol_internal_call"},
    "s5_3_role_self_escalation":         {"role_modification"},
    "s5_3_privileged_auth_bypass":       {"delegated_action"},
}


# ── Condition Templates ───────────────────────────────────────────────────────
#
# 17 templates induced from the 394-report corpus missing_what fields.
# Condition templates are orthogonal to mechanism families: the same
# template can appear across L1, S1-1, S1-2, and S5-3 findings.

CONDITION_TEMPLATES: Dict[str, Dict] = {
    "C-L1a": {"name": "reentrancy_guard",
               "desc": "Missing nonReentrant modifier or equivalent reentrancy protection",
               "predicates": ["guard(nonReentrant)"]},
    "C-L1b": {"name": "CEI_pattern",
               "desc": "Not following Checks-Effects-Interactions pattern (external call before state update)",
               "predicates": ["pattern(CEI)"]},
    "C-L1c": {"name": "state_update_before_call",
               "desc": "Specific state variable not updated before external call (concrete CEI instance)",
               "predicates": ["pattern(CEI)"]},
    "C-L1d": {"name": "cross_scope_reentrancy",
               "desc": "Missing cross-function or cross-contract reentrancy protection",
               "predicates": ["guard(nonReentrant)"]},
    "C-S11a": {"name": "manipulation_resistant_price",
                "desc": "Price/rate from manipulable source (AMM spot/reserves/balanceOf) without TWAP/oracle",
                "predicates": ["invariant(price_manipulation)", "check(oracle_freshness)"]},
    "C-S11b": {"name": "first_depositor_protection",
                "desc": "Missing minimum shares/liquidity check allowing inflation when totalSupply near zero",
                "predicates": ["check(totalSupply > minimum)", "pattern(virtual_offset)"]},
    "C-S11c": {"name": "flash_loan_protection",
                "desc": "Missing protection against flash-loan-induced price/state distortion",
                "predicates": ["invariant(price_manipulation)", "invariant(checkpoint_time_separation)"]},
    "C-S11d": {"name": "exchange_rate_validation",
                "desc": "Exchange rate or reserve ratio not validated for reasonable range",
                "predicates": ["invariant(price_manipulation)"]},
    "C-S12a": {"name": "slippage_protection",
                "desc": "Swap/liquidity operation missing minimum output amount check",
                "predicates": ["check(cost_bound)"]},
    "C-S12b": {"name": "deadline_protection",
                "desc": "Transaction missing validity time limit (deadline/timeout)",
                "predicates": ["check(deadline)"]},
    "C-S12c": {"name": "dynamic_slippage",
                "desc": "Slippage parameter hardcoded or improperly calculated (e.g. ignoring fees)",
                "predicates": ["check(cost_bound)"]},
    "C-S12d": {"name": "actual_amount_verification",
                "desc": "Missing balance before/after check to verify actual received amount",
                "predicates": ["check(balance_before_after)"]},
    "C-S53a": {"name": "admin_access_control",
                "desc": "Sensitive function missing admin/owner/role-based access control",
                "predicates": ["check(msg.sender == onlyOwner)", "check(msg.sender == protocol_role)"]},
    "C-S53b": {"name": "ownership_verification",
                "desc": "Operation not verifying caller is the asset owner",
                "predicates": ["check(msg.sender == onlyOwner)"]},
    "C-S53c": {"name": "role_specific_gate",
                "desc": "Missing role-specific modifier (onlyRouter/onlyBorrower/onlyLender etc.)",
                "predicates": ["check(msg.sender == protocol_role)"]},
    "C-S53d": {"name": "approval_delegation_check",
                "desc": "Not verifying caller has approval/delegation for the operation",
                "predicates": ["check(msg.sender == protocol_role)"]},
    "C-S53e": {"name": "initializer_guard",
                "desc": "Initialize function missing re-initialization protection",
                "predicates": ["guard(initializer)", "check(msg.sender == trusted_deployer)"]},
}

TEMPLATE_IDS: Set[str] = set(CONDITION_TEMPLATES.keys())
TEMPLATE_BY_NAME: Dict[str, str] = {v["name"]: k for k, v in CONDITION_TEMPLATES.items()}


# ── MDL predicates (full vocabulary for condition expressions) ────────────────

CONDITION_PREDICATES: Dict[str, str] = {
    "guard(nonReentrant)":               "reentrancy protection modifier",
    "guard(initializer)":                "initialization protection modifier",
    "guard(whenNotPaused)":              "pause protection modifier",
    "check(msg.sender == trusted_deployer)": "deployer/factory permission check",
    "check(msg.sender == onlyOwner)":        "admin/governance permission check",
    "check(msg.sender == protocol_role)":    "protocol-internal role check",
    "check(deadline)":                       "transaction deadline check",
    "check(cost_bound)":                     "slippage/min-output/max-cost check",
    "check(totalSupply > minimum)":          "supply minimum check (anti first-depositor)",
    "check(shares_minted > 0)":             "minted amount > 0 check",
    "check(balance_before_after)":           "balance before/after check (anti fee-on-transfer)",
    "check(oracle_freshness)":               "oracle price freshness check",
    "check(return_value)":                   "external call return value check",
    "pattern(CEI)":                      "Checks-Effects-Interactions pattern",
    "pattern(virtual_offset)":           "ERC4626 virtual offset (anti first-depositor)",
    "pattern(pull_payment)":             "pull payment pattern",
    "invariant(checkpoint_time_separation)": "time separation between operations",
    "invariant(balance_accounting)":         "accounting consistency",
    "invariant(unique_elements)":            "input array element uniqueness",
    "invariant(supply_nonzero)":             "supply non-zero (anti division-by-zero)",
    "invariant(price_manipulation)":         "price not manipulable by single operation",
}

VALID_PREDICATES: Set[str] = set(CONDITION_PREDICATES.keys())
VALID_STATES: Set[str] = {"absent", "weak"}
VALID_DEFICIENCIES: Set[str] = {
    "hardcoded_value",
    "insufficient_granularity",
    "trivial_value",
    "single_source",
    "partial_coverage",
}


# ── Grounded operation dataclasses ────────────────────────────────────────────

@dataclass
class GroundedOperation:
    """An MDL operation anchored to a concrete function name from the PDG."""
    name: str
    grounding_type: str = "direct"  # direct / semantic / internal / ungrounded
    weight: str = "AUX"             # CORE / AUX (report-side only)
    step_text: str = ""

    def to_dict(self) -> dict:
        return {"name": self.name, "grounding_type": self.grounding_type,
                "weight": self.weight, "step_text": self.step_text}

    @staticmethod
    def from_dict(d: dict) -> "GroundedOperation":
        return GroundedOperation(**{k: d[k] for k in d if k in GroundedOperation.__dataclass_fields__})


@dataclass
class OperationRelation:
    """Directed causal relation between two grounded operations."""
    op_a: str
    op_b: str
    weight: str = "AUX"  # CORE / AUX

    def to_dict(self) -> dict:
        return {"op_a": self.op_a, "op_b": self.op_b, "weight": self.weight}

    @staticmethod
    def from_dict(d: dict) -> "OperationRelation":
        return OperationRelation(**{k: d[k] for k in d if k in OperationRelation.__dataclass_fields__})


# ── MDL condition expression parser ──────────────────────────────────────────
#
# Parses MDL condition expressions such as:
#   "¬check(msg.sender == trusted_deployer)"
#   "weak(guard(initializer), insufficient_granularity)"

_PREDICATE_RE = re.compile(r"(guard|check|pattern|invariant)\(([^)]+)\)")
_MISSING_RE = re.compile(
    r"(?:"
    r"¬(guard|check|pattern|invariant)\(([^)]+)\)"
    r"|"
    r"weak\((guard|check|pattern|invariant)\(([^)]+)\),\s*(\w+)\)"
    r")"
)


class MDLCondition:
    """A parsed MDL condition (absent or weak predicate)."""
    __slots__ = ("state", "predicate", "deficiency")

    def __init__(self, state: str, predicate: str, deficiency: Optional[str] = None):
        self.state = state
        self.predicate = predicate
        self.deficiency = deficiency

    def __repr__(self):
        if self.state == "absent":
            return f"¬{self.predicate}"
        return f"weak({self.predicate}, {self.deficiency})"

    def is_valid(self) -> bool:
        return (self.state in VALID_STATES
                and self.predicate in VALID_PREDICATES
                and (self.state == "absent" or self.deficiency in VALID_DEFICIENCIES))

    def to_dict(self) -> dict:
        d = {"state": self.state, "predicate": self.predicate}
        if self.deficiency:
            d["deficiency"] = self.deficiency
        return d


def parse_mdl_condition(cond_text: str) -> Optional[MDLCondition]:
    """Parse a single MDL condition expression string."""
    m = _MISSING_RE.search(cond_text.strip())
    if not m:
        return None
    if m.group(1):
        return MDLCondition("absent", f"{m.group(1)}({m.group(2)})")
    elif m.group(3):
        return MDLCondition("weak", f"{m.group(3)}({m.group(4)})", m.group(5))
    return None


def parse_condition_list(raw: list) -> list[MDLCondition]:
    """Parse a list of raw condition dicts or strings into MDLCondition objects."""
    result = []
    for item in raw or []:
        if isinstance(item, MDLCondition):
            result.append(item)
            continue
        if isinstance(item, dict):
            state = item.get("state") or item.get("type") or "absent"
            pred = item.get("predicate") or item.get("condition", "")
            deficiency = item.get("deficiency")
            if pred:
                result.append(MDLCondition(state, pred, deficiency))
            continue
        if isinstance(item, str):
            cond = parse_mdl_condition(item)
            if cond:
                result.append(cond)
    return result
