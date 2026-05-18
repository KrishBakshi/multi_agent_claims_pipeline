"""DataValidatorAgent — LangGraph node.

Validates all structured claim fields before any document processing.
Halts the pipeline immediately on any failure so the member gets a
specific, actionable error message.

Checks (in order):
  1. policy_id matches loaded policy
  2. member_id exists in the roster
  3. treatment_date fell within the policy's active period
     (policy_start_date ≤ treatment_date ≤ policy_end_date)
  4. claim_category is a recognised value
  5. claimed_amount is above the policy minimum

Note on submission deadline: the policy specifies 30 days from treatment to
submission, but ClaimInput carries no submission_date field — only
treatment_date. Evaluating the deadline requires knowing when the claim was
actually filed, which is unavailable here. The check is intentionally
omitted; it should be enforced at the intake layer before this pipeline runs.
"""
from __future__ import annotations

from datetime import date

from src.core.logger import claim_logger
from src.core.policy_loader import PolicyLoader
from src.models.state import ClaimState

VALID_CATEGORIES = {
    "CONSULTATION", "DIAGNOSTIC", "PHARMACY",
    "DENTAL", "VISION", "ALTERNATIVE_MEDICINE",
}

CONFIDENCE_FAILURE_PENALTY = 0.20


def _t(agent: str, step: str, result: str, detail: str) -> dict:
    return {"agent": agent, "step": step, "result": result, "detail": detail}


def build_data_validator(policy: PolicyLoader):
    """Returns a LangGraph-compatible node function closed over `policy`."""

    def data_validator_node(state: ClaimState) -> dict:
        agent = "DataValidatorAgent"
        claim_id = state.get("claim_id", "--------")
        log = claim_logger("agents.data_validator", claim_id)

        inp = state["claim_input"]
        raw = policy.raw
        trace: list[dict] = []
        confidence: float = state.get("confidence", 1.0)

        log.info(
            "Starting — member=%s category=%s amount=₹%.2f docs=%d",
            inp["member_id"], inp["claim_category"],
            inp["claimed_amount"], len(inp.get("documents", [])),
        )

        # ── TC011 simulated failure ──────────────────────────────────────────
        if inp.get("simulate_component_failure"):
            log.warning("Simulated component failure triggered — continuing degraded")
            trace.append(_t(agent, "simulate_failure", "ERROR",
                            "Simulated component failure — continuing with degraded confidence"))
            confidence = max(0.0, confidence - CONFIDENCE_FAILURE_PENALTY)
            member = policy.get_member(inp["member_id"])
            return {
                "member": member,
                "policy": raw,
                "component_failures": [agent],
                "confidence": confidence,
                "trace": trace,
                "halted": False,
                "halt_message": None,
                "manual_review_recommended": True,
            }

        def halt(step: str, message: str) -> dict:
            log.warning("HALT [%s] — %s", step, message)
            trace.append(_t(agent, step, "FAIL", message))
            return {
                "member": None,
                "policy": raw,
                "halted": True,
                "halt_message": message,
                "confidence": max(0.0, confidence - CONFIDENCE_FAILURE_PENALTY),
                "trace": trace,
                "component_failures": [],
                "manual_review_recommended": False,
            }

        # 1. Policy ID
        if inp["policy_id"] != raw.get("policy_id"):
            return halt("policy_id_check",
                        f"Policy ID '{inp['policy_id']}' not found. "
                        f"Expected '{raw.get('policy_id')}'.")

        log.debug("PASS policy_id — %s", inp["policy_id"])

        # 2. Member exists
        member = policy.get_member(inp["member_id"])
        if member is None:
            return halt("member_lookup",
                        f"Member ID '{inp['member_id']}' is not registered under this policy.")
        log.info("PASS member_lookup — '%s' (joined %s)", member["name"], member["join_date"])
        trace.append(_t(agent, "member_lookup", "PASS",
                        f"Member '{member['name']}' found (joined {member['join_date']})"))

        # 3. Treatment date within the policy's active period
        holder = raw.get("policy_holder", {})
        try:
            policy_start = date.fromisoformat(holder["policy_start_date"])
            policy_end = date.fromisoformat(holder["policy_end_date"])
            treatment_date = date.fromisoformat(inp["treatment_date"])
        except (KeyError, ValueError) as exc:
            log.error("Date parsing failed: %s", exc, exc_info=True)
            return halt("date_parse", f"Date parsing error: {exc}")

        if treatment_date < policy_start:
            return halt(
                "policy_period",
                f"Treatment date {treatment_date} is before the policy start date "
                f"{policy_start}. This policy covers {policy_start} to {policy_end}.",
            )
        if treatment_date > policy_end:
            return halt(
                "policy_period",
                f"Treatment date {treatment_date} is after the policy end date "
                f"{policy_end}. This policy covers {policy_start} to {policy_end}.",
            )
        log.info("PASS policy_period — treatment %s within [%s, %s]",
                 treatment_date, policy_start, policy_end)
        trace.append(_t(agent, "policy_period", "PASS",
                        f"Treatment date {treatment_date} is within policy period "
                        f"({policy_start} → {policy_end})"))

        # 4. Claim category
        category = inp["claim_category"].upper()
        if category not in VALID_CATEGORIES:
            return halt("category_valid",
                        f"Invalid claim category '{inp['claim_category']}'. "
                        f"Valid categories: {', '.join(sorted(VALID_CATEGORIES))}.")
        log.debug("PASS category — %s", category)
        trace.append(_t(agent, "category_valid", "PASS", f"Category '{category}' is valid"))

        # 5. Minimum claim amount
        sub_rules = policy.get_submission_rules()
        min_amount = sub_rules.get("minimum_claim_amount", 500)
        claimed = inp["claimed_amount"]
        if claimed < min_amount:
            return halt("minimum_amount",
                        f"Claimed amount ₹{claimed} is below the policy minimum of ₹{min_amount}.")
        log.debug("PASS minimum_amount — ₹%.2f ≥ ₹%s", claimed, min_amount)
        trace.append(_t(agent, "minimum_amount", "PASS",
                        f"Claimed ₹{claimed} meets minimum ₹{min_amount}"))

        log.info("Complete — all checks passed")
        trace.append(_t(agent, "data_validation", "PASS",
                        "All claim fields validated successfully"))
        return {
            "member": member,
            "policy": raw,
            "halted": False,
            "halt_message": None,
            "confidence": confidence,
            "trace": trace,
            "component_failures": [],
            "manual_review_recommended": False,
        }

    return data_validator_node
