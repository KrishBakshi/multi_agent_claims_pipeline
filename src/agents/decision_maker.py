"""DecisionMakerAgent — LangGraph node.

Applies all policy rules in a deterministic sequence and produces one of:
  APPROVED | PARTIAL | REJECTED | MANUAL_REVIEW

Rule evaluation order:
  1. Fraud / manual-review thresholds  (same-day claims, high-value amount)
  2. Exclusion check                   (uses Gemini for semantic matching)
  3. Waiting period check              (date arithmetic against policy rules)
  4. Pre-authorisation check
  5. Per-claim limit check
  6. Line-item level approval          (for DENTAL — covered vs excluded procedures)
  7. Amount calculation                (network discount → co-pay → sub-limit cap)

LLM (ChatGoogleGenerativeAI / gemini-3.1-flash-lite) is used only for:
  - Exclusion semantic matching  (is this diagnosis/treatment excluded?)
  - Waiting-period condition ID  (which specific condition does this diagnosis map to?)
All numeric calculations and threshold comparisons are deterministic Python.

LLM error policy: each call is retried once (with a short back-off). If both
attempts fail the claim is halted and routed to MANUAL_REVIEW with a clear
message stating the AI service is unavailable and a human reviewer is required.
"""
from __future__ import annotations

import os
import time
from datetime import date, timedelta
from typing import Optional, TypeVar

T = TypeVar("T")

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel

from src.core.logger import claim_logger
from src.core.policy_loader import PolicyLoader
from src.models.state import ClaimState

# ── LLM structured-output schemas ────────────────────────────────────────────


class ExclusionCheckResult(BaseModel):
    is_excluded: bool
    matched_exclusion: Optional[str] = None
    reasoning: str


class WaitingPeriodMatch(BaseModel):
    matched_condition: Optional[str] = None   # key in specific_conditions dict
    reasoning: str


# ── helpers ───────────────────────────────────────────────────────────────────

_RATE_LIMIT_PHRASES = ("quota", "resource exhausted", "429", "rate limit", "too many requests")


def _is_rate_limit(exc: Exception) -> bool:
    return any(p in str(exc).lower() for p in _RATE_LIMIT_PHRASES)


def _llm_invoke_with_retry(llm, messages: list, retry_delay: float = 2.0):
    """Invoke an LLM once, retry once on any error, raise on second failure."""
    try:
        return llm.invoke(messages)
    except Exception as first_exc:
        delay = retry_delay * 2 if _is_rate_limit(first_exc) else retry_delay
        time.sleep(delay)
        return llm.invoke(messages)  # raises if it fails again


def _t(agent: str, step: str, result: str, detail: str) -> dict:
    return {"agent": agent, "step": step, "result": result, "detail": detail}


def _get_diagnosis(extracted_docs: list[dict]) -> Optional[str]:
    for d in extracted_docs:
        if d.get("diagnosis"):
            return d["diagnosis"]
    return None


def _get_treatment(extracted_docs: list[dict]) -> Optional[str]:
    for d in extracted_docs:
        if d.get("treatment"):
            return d["treatment"]
    return None


def _get_tests_ordered(extracted_docs: list[dict]) -> list[str]:
    tests: list[str] = []
    for d in extracted_docs:
        tests.extend(d.get("tests_ordered") or [])
    return tests


def _get_hospital_name(inp: dict, extracted_docs: list[dict]) -> Optional[str]:
    if inp.get("hospital_name"):
        return inp["hospital_name"]
    for d in extracted_docs:
        if d.get("hospital_name"):
            return d["hospital_name"]
    return None


def _get_all_line_items(extracted_docs: list[dict]) -> list[dict]:
    items: list[dict] = []
    for d in extracted_docs:
        items.extend(d.get("line_items") or [])
    return items


# ── main builder ──────────────────────────────────────────────────────────────

def build_decision_maker(policy: PolicyLoader):
    """Returns a LangGraph-compatible node function closed over `policy`."""

    # Lazy — only instantiated on first actual LLM call so the pipeline
    # can be compiled and tested without an API key present.
    _llm_cache: dict = {}

    def _get_exclusion_llm():
        if "exclusion" not in _llm_cache:
            llm = ChatGoogleGenerativeAI(
                model="gemini-3.1-flash-lite",
                google_api_key=os.getenv("GOOGLE_API_KEY"),
                max_output_tokens=512,
            )
            _llm_cache["exclusion"] = llm.with_structured_output(ExclusionCheckResult)
        return _llm_cache["exclusion"]

    def _get_waiting_llm():
        if "waiting" not in _llm_cache:
            llm = ChatGoogleGenerativeAI(
                model="gemini-3.1-flash-lite",
                google_api_key=os.getenv("GOOGLE_API_KEY"),
                max_output_tokens=512,
            )
            _llm_cache["waiting"] = llm.with_structured_output(WaitingPeriodMatch)
        return _llm_cache["waiting"]

    def decision_maker_node(state: ClaimState) -> dict:  # noqa: C901 (complexity ok)
        if state.get("halted"):
            return {}

        agent = "DecisionMakerAgent"
        claim_id = state.get("claim_id", "--------")
        log = claim_logger("agents.decision_maker", claim_id)

        inp = state["claim_input"]
        extracted = state.get("extracted_docs", [])
        member = state.get("member") or {}
        trace: list[dict] = []
        rejection_reasons: list[str] = []
        manual_review_signals: list[str] = []
        confidence: float = state.get("confidence", 1.0)
        manual_review_recommended: bool = state.get("manual_review_recommended", False)

        category = inp["claim_category"].upper()
        claimed_amount: float = inp["claimed_amount"]
        treatment_date = date.fromisoformat(inp["treatment_date"])
        join_date = date.fromisoformat(member.get("join_date", "2020-01-01"))

        diagnosis = _get_diagnosis(extracted)
        treatment = _get_treatment(extracted)
        tests_ordered = _get_tests_ordered(extracted)
        hospital_name = _get_hospital_name(inp, extracted)
        all_line_items = _get_all_line_items(extracted)

        log.info(
            "Starting — category=%s amount=₹%.2f diagnosis=%s hospital=%s",
            category, claimed_amount, diagnosis or "—", hospital_name or "—",
        )

        fraud = policy.get_fraud_thresholds()
        coverage = policy.get_coverage()
        opd_cat = policy.get_opd_category(category)
        waiting = policy.get_waiting_periods()

        # ── 1. Fraud / manual-review thresholds ──────────────────────────────
        claims_history: list[dict] = inp.get("claims_history") or []
        same_day_limit: int = fraud.get("same_day_claims_limit", 2)
        monthly_limit: int = fraud.get("monthly_claims_limit", 6)
        high_value: float = fraud.get("auto_manual_review_above", 25000)

        same_day_count = sum(
            1 for c in claims_history if c.get("date") == inp["treatment_date"]
        )
        if same_day_count >= same_day_limit:
            signal = (
                f"Member has {same_day_count} prior claim(s) on {inp['treatment_date']} "
                f"(limit: {same_day_limit})"
            )
            log.warning("Fraud signal — same-day: %s", signal)
            manual_review_signals.append(signal)
            trace.append(_t(agent, "fraud_same_day", "WARNING", signal))

        month_prefix = inp["treatment_date"][:7]
        monthly_count = sum(
            1 for c in claims_history if c.get("date", "")[:7] == month_prefix
        )
        if monthly_count >= monthly_limit:
            signal = (
                f"Member has {monthly_count} claims this month (limit: {monthly_limit})"
            )
            log.warning("Fraud signal — monthly: %s", signal)
            manual_review_signals.append(signal)
            trace.append(_t(agent, "fraud_monthly", "WARNING", signal))

        if claimed_amount > high_value:
            signal = f"Claimed amount ₹{claimed_amount} exceeds auto-review threshold ₹{high_value}"
            log.warning("Fraud signal — high value: %s", signal)
            manual_review_signals.append(signal)
            trace.append(_t(agent, "fraud_high_value", "WARNING", signal))

        if manual_review_signals:
            log.warning("Routing to MANUAL_REVIEW — %d signal(s) triggered", len(manual_review_signals))
            trace.append(_t(agent, "manual_review_trigger", "INFO",
                            f"Routing to MANUAL_REVIEW: {'; '.join(manual_review_signals)}"))
            return _build_result(
                agent, "MANUAL_REVIEW", None, rejection_reasons,
                manual_review_signals, trace, confidence, True,
                "Claim flagged for manual review due to unusual activity patterns.",
                None, [],
            )

        # ── 2. Exclusion check (LLM) ─────────────────────────────────────────
        if diagnosis or treatment:
            exclusions = policy.get_exclusions()
            exclusion_list = (
                exclusions.get("conditions", [])
                + exclusions.get("dental_exclusions", [])
                + exclusions.get("vision_exclusions", [])
            )
            log.debug("Calling Gemini for exclusion check — diagnosis='%s' treatment='%s'",
                      diagnosis or "—", treatment or "—")
            try:
                excl_result: ExclusionCheckResult = _llm_invoke_with_retry(
                    _get_exclusion_llm(),
                    [
                        SystemMessage(
                            "You check whether a medical claim is excluded under a health insurance policy. "
                            "Answer only based on the exclusion list provided."
                        ),
                        HumanMessage(
                            f"Diagnosis: {diagnosis}\n"
                            f"Treatment: {treatment}\n"
                            f"Policy exclusions: {exclusion_list}\n\n"
                            "Is this claim excluded? If yes, which exclusion matches?"
                        ),
                    ],
                )
                if excl_result.is_excluded:
                    log.warning("EXCLUDED — matched: '%s'", excl_result.matched_exclusion)
                    rejection_reasons.append("EXCLUDED_CONDITION")
                    msg = (
                        f"Claim rejected: '{excl_result.matched_exclusion}' is excluded "
                        f"under the policy. Reason: {excl_result.reasoning}"
                    )
                    trace.append(_t(agent, "exclusion_check", "FAIL", msg))
                    return _build_result(
                        agent, "REJECTED", None, rejection_reasons,
                        manual_review_signals, trace, confidence, False, msg, None, [],
                    )
                log.debug("PASS exclusion_check — %s", excl_result.reasoning)
                trace.append(_t(agent, "exclusion_check", "PASS",
                                f"No exclusion matched. {excl_result.reasoning}"))
            except Exception as exc:
                hint = (
                    "AI decision service is over quota — please try again later."
                    if _is_rate_limit(exc)
                    else "AI decision service is unavailable."
                )
                msg = (
                    f"{hint} This claim cannot be processed automatically and requires "
                    f"a human reviewer to make a coverage decision."
                )
                log.error("Exclusion LLM failed after retry — routing to MANUAL_REVIEW: %s", exc)
                trace.append(_t(agent, "exclusion_check", "ERROR", msg))
                manual_review_signals.append("LLM_UNAVAILABLE")
                return _build_result(
                    agent, "MANUAL_REVIEW", None, rejection_reasons,
                    manual_review_signals, trace, confidence, True, msg, None, [],
                )

        # ── 3. Waiting period check ───────────────────────────────────────────
        initial_days: int = waiting.get("initial_waiting_period_days", 30)
        days_since_join = (treatment_date - join_date).days

        if days_since_join < initial_days:
            rejection_reasons.append("WAITING_PERIOD")
            eligible_from = join_date + timedelta(days=initial_days)
            msg = (
                f"Treatment date {treatment_date} is within the {initial_days}-day initial "
                f"waiting period. Member is eligible from {eligible_from}."
            )
            trace.append(_t(agent, "waiting_period_initial", "FAIL", msg))
            return _build_result(
                agent, "REJECTED", None, rejection_reasons,
                manual_review_signals, trace, confidence, False, msg, None, [],
            )
        trace.append(_t(agent, "waiting_period_initial", "PASS",
                        f"Initial waiting period satisfied ({days_since_join} days since join)"))

        # Specific-condition waiting period (LLM maps diagnosis → condition key)
        specific: dict = waiting.get("specific_conditions", {})
        if specific and (diagnosis or treatment):
            log.debug("Calling Gemini for waiting-period condition match — diagnosis='%s'", diagnosis or "—")
            try:
                wp_result: WaitingPeriodMatch = _llm_invoke_with_retry(
                    _get_waiting_llm(),
                    [
                        SystemMessage(
                            "Map the given medical diagnosis to one of the condition keys in the "
                            "waiting-period list, or null if it doesn't match any."
                        ),
                        HumanMessage(
                            f"Diagnosis: {diagnosis}\n"
                            f"Treatment: {treatment}\n"
                            f"Condition keys: {list(specific.keys())}"
                        ),
                    ],
                )
                cond_key = wp_result.matched_condition
                if cond_key and cond_key in specific:
                    cond_days: int = specific[cond_key]
                    log.debug("Waiting period match — condition='%s' days=%d days_since_join=%d",
                              cond_key, cond_days, days_since_join)
                    if days_since_join < cond_days:
                        rejection_reasons.append("WAITING_PERIOD")
                        eligible_from = join_date + timedelta(days=cond_days)
                        msg = (
                            f"Claim for '{cond_key}' is within the {cond_days}-day waiting period. "
                            f"Member joined {join_date}; eligible for {cond_key} claims from "
                            f"{eligible_from}."
                        )
                        log.warning("REJECTED — waiting period: %s", msg)
                        trace.append(_t(agent, "waiting_period_specific", "FAIL", msg))
                        return _build_result(
                            agent, "REJECTED", None, rejection_reasons,
                            manual_review_signals, trace, confidence, False, msg, None, [],
                        )
                    trace.append(_t(agent, "waiting_period_specific", "PASS",
                                    f"Specific waiting period for '{cond_key}' satisfied"))
                else:
                    log.debug("No specific waiting period matched — %s", wp_result.reasoning)
                    trace.append(_t(agent, "waiting_period_specific", "PASS",
                                    f"No specific waiting period matched. {wp_result.reasoning}"))
            except Exception as exc:
                hint = (
                    "AI decision service is over quota — please try again later."
                    if _is_rate_limit(exc)
                    else "AI decision service is unavailable."
                )
                msg = (
                    f"{hint} This claim cannot be processed automatically and requires "
                    f"a human reviewer to make a coverage decision."
                )
                log.error("Waiting-period LLM failed after retry — routing to MANUAL_REVIEW: %s", exc)
                trace.append(_t(agent, "waiting_period_specific", "ERROR", msg))
                manual_review_signals.append("LLM_UNAVAILABLE")
                return _build_result(
                    agent, "MANUAL_REVIEW", None, rejection_reasons,
                    manual_review_signals, trace, confidence, True, msg, None, [],
                )

        # ── 4. Pre-authorisation check ────────────────────────────────────────
        pre_auth = policy.get_pre_authorization()
        high_value_tests = {"MRI", "CT SCAN", "PET SCAN"}
        diagnostic_cat = policy.get_opd_category("diagnostic") or {}
        pre_auth_threshold = diagnostic_cat.get("pre_auth_threshold", 10000)

        needs_pre_auth = False
        if category == "DIAGNOSTIC":
            for test in tests_ordered:
                test_upper = test.upper()
                for hvt in high_value_tests:
                    if hvt in test_upper and claimed_amount > pre_auth_threshold:
                        needs_pre_auth = True
                        break

        if needs_pre_auth:
            log.warning("REJECTED — pre-auth required for %s ₹%.2f", tests_ordered, claimed_amount)
            rejection_reasons.append("PRE_AUTH_MISSING")
            msg = (
                f"Pre-authorisation is required for this procedure (amount ₹{claimed_amount} "
                f"exceeds the ₹{pre_auth_threshold} threshold for high-value diagnostic tests). "
                f"To resubmit: obtain pre-authorisation from your insurer, then re-file the claim "
                f"with the pre-auth reference number. Pre-auth is valid for "
                f"{pre_auth.get('validity_days', 30)} days."
            )
            trace.append(_t(agent, "pre_auth_check", "FAIL", msg))
            return _build_result(
                agent, "REJECTED", None, rejection_reasons,
                manual_review_signals, trace, confidence, False, msg, None, [],
            )
        trace.append(_t(agent, "pre_auth_check", "PASS",
                        "Pre-authorisation not required or already obtained"))

        # ── 5. Per-claim limit (non-dental only — dental uses its own sub-limit) ─
        per_claim_limit: float = coverage.get("per_claim_limit", 5000)
        if category != "DENTAL":
            if claimed_amount > per_claim_limit:
                log.warning("REJECTED — per-claim limit: ₹%.2f > ₹%.2f", claimed_amount, per_claim_limit)
                rejection_reasons.append("PER_CLAIM_EXCEEDED")
                msg = (
                    f"Claimed amount ₹{claimed_amount} exceeds the per-claim limit of "
                    f"₹{per_claim_limit}. Claims above this limit cannot be processed."
                )
                trace.append(_t(agent, "per_claim_limit", "FAIL", msg))
                return _build_result(
                    agent, "REJECTED", None, rejection_reasons,
                    manual_review_signals, trace, confidence, False, msg, None, [],
                )
            trace.append(_t(agent, "per_claim_limit", "PASS",
                            f"Claimed ₹{claimed_amount} within per-claim limit ₹{per_claim_limit}"))

        # ── 6. Line-item approval (DENTAL / category with exclusions) ─────────
        line_item_decisions: list[dict] = []
        approved_base: float = claimed_amount

        if category == "DENTAL" and all_line_items:
            dental_cat = policy.get_opd_category("dental") or {}
            covered_procs = {p.lower() for p in dental_cat.get("covered_procedures", [])}
            excluded_procs = {p.lower() for p in dental_cat.get("excluded_procedures", [])}

            approved_total = 0.0
            any_rejected = False
            for item in all_line_items:
                desc_lower = item["description"].lower()
                is_excluded = any(ep in desc_lower for ep in excluded_procs)
                is_covered = any(cp in desc_lower for cp in covered_procs)

                if is_excluded:
                    any_rejected = True
                    line_item_decisions.append({
                        "description": item["description"],
                        "amount": item["amount"],
                        "approved": False,
                        "reason": f"'{item['description']}' is a cosmetic/excluded procedure "
                                  f"under the dental policy.",
                    })
                    trace.append(_t(agent, "line_item", "FAIL",
                                    f"Rejected: {item['description']} ₹{item['amount']} — excluded"))
                elif is_covered:
                    approved_total += item["amount"]
                    line_item_decisions.append({
                        "description": item["description"],
                        "amount": item["amount"],
                        "approved": True,
                        "reason": None,
                    })
                    trace.append(_t(agent, "line_item", "PASS",
                                    f"Approved: {item['description']} ₹{item['amount']}"))
                else:
                    # Unknown procedure — approve with note
                    approved_total += item["amount"]
                    line_item_decisions.append({
                        "description": item["description"],
                        "amount": item["amount"],
                        "approved": True,
                        "reason": "Procedure not explicitly listed — approved as standard dental",
                    })
                    trace.append(_t(agent, "line_item", "INFO",
                                    f"Approved (unlisted): {item['description']} ₹{item['amount']}"))

            approved_base = approved_total
            final_decision_type = "PARTIAL" if any_rejected else "APPROVED"

            # Dental uses its own sub-limit as the per-claim ceiling
            dental_sub_limit = float((policy.get_opd_category("dental") or {}).get("sub_limit", 10000))
            if approved_base > dental_sub_limit:
                log.warning("REJECTED — dental sub-limit: ₹%.2f > ₹%.2f", approved_base, dental_sub_limit)
                rejection_reasons.append("PER_CLAIM_EXCEEDED")
                msg = (
                    f"Approved dental amount ₹{approved_base} exceeds the dental sub-limit of "
                    f"₹{dental_sub_limit}."
                )
                trace.append(_t(agent, "per_claim_limit", "FAIL", msg))
                return _build_result(
                    agent, "REJECTED", None, rejection_reasons,
                    manual_review_signals, trace, confidence, False, msg, None, line_item_decisions,
                )
            trace.append(_t(agent, "per_claim_limit", "PASS",
                            f"Approved dental amount ₹{approved_base} within sub-limit ₹{dental_sub_limit}"))
        else:
            final_decision_type = "APPROVED"

        # ── 7. Amount calculation ─────────────────────────────────────────────
        is_network = policy.is_network_hospital(hospital_name)
        net_discount_pct: float = 0.0
        copay_pct: float = 0.0
        sub_limit: Optional[float] = None

        if opd_cat:
            copay_pct = opd_cat.get("copay_percent", 0) / 100
            if is_network:
                net_discount_pct = opd_cat.get("network_discount_percent", 0) / 100
            sub_limit_val = opd_cat.get("sub_limit")
            if sub_limit_val:
                sub_limit = float(sub_limit_val)

        # Apply: network discount → copay
        net_discount_amount = round(approved_base * net_discount_pct, 2)
        after_discount = round(approved_base - net_discount_amount, 2)
        copay_amount = round(after_discount * copay_pct, 2)
        after_copay = round(after_discount - copay_amount, 2)

        if sub_limit:
            trace.append(_t(agent, "sub_limit", "INFO",
                            f"Annual sub-limit for {category}: ₹{sub_limit} (YTD tracking not applied per-claim)"))

        approved_amount = after_copay

        breakdown = {
            "claimed_amount": claimed_amount,
            "network_discount_percent": net_discount_pct * 100 if net_discount_pct else None,
            "network_discount_amount": net_discount_amount if net_discount_pct else None,
            "amount_after_discount": after_discount if net_discount_pct else None,
            "copay_percent": copay_pct * 100 if copay_pct else None,
            "copay_amount": copay_amount if copay_pct else None,
            "sub_limit_applied": None,
            "approved_amount": approved_amount,
        }

        if net_discount_pct:
            trace.append(_t(agent, "network_discount", "INFO",
                            f"Network discount {net_discount_pct*100:.0f}% applied: "
                            f"₹{approved_base} → ₹{after_discount}"))
        if copay_pct:
            trace.append(_t(agent, "copay", "INFO",
                            f"Co-pay {copay_pct*100:.0f}% applied: "
                            f"₹{after_discount} → ₹{after_discount - copay_amount} "
                            f"(deducted ₹{copay_amount})"))

        reason = _build_reason(final_decision_type, approved_amount, claimed_amount,
                               net_discount_pct, net_discount_amount,
                               copay_pct, copay_amount, manual_review_recommended)

        log.info(
            "Complete — decision=%s approved=₹%.2f confidence=%.2f network=%s",
            final_decision_type, approved_amount, confidence,
            "YES" if is_network else "NO",
        )
        trace.append(_t(agent, "final_decision", "INFO",
                        f"Decision: {final_decision_type} | Approved: ₹{approved_amount}"))

        return _build_result(
            agent, final_decision_type, approved_amount, rejection_reasons,
            manual_review_signals, trace, confidence, manual_review_recommended,
            reason, breakdown, line_item_decisions,
        )

    return decision_maker_node


# ── result builder ────────────────────────────────────────────────────────────

def _build_result(
    agent: str,
    decision: str,
    approved_amount: Optional[float],
    rejection_reasons: list[str],
    manual_review_signals: list[str],
    trace: list[dict],
    confidence: float,
    manual_review_recommended: bool,
    reason: str,
    breakdown: Optional[dict],
    line_item_decisions: list[dict],
) -> dict:
    return {
        "decision": decision,
        "approved_amount": approved_amount,
        "rejection_reasons": rejection_reasons,
        "manual_review_signals": manual_review_signals,
        "trace": trace,
        "confidence": confidence,
        "manual_review_recommended": manual_review_recommended,
        "reason": reason,
        "breakdown": breakdown,
        "line_item_decisions": line_item_decisions,
    }


def _build_reason(
    decision: str,
    approved: float,
    claimed: float,
    net_pct: float,
    net_amt: float,
    copay_pct: float,
    copay_amt: float,
    manual_review: bool,
) -> str:
    parts = []
    if decision == "APPROVED":
        parts.append(f"Claim approved for ₹{approved}.")
        if net_pct:
            parts.append(f"Network discount ({net_pct*100:.0f}%) of ₹{net_amt} applied.")
        if copay_pct:
            parts.append(f"Co-pay ({copay_pct*100:.0f}%) of ₹{copay_amt} deducted.")
        if manual_review:
            parts.append("Note: manual review recommended due to incomplete processing.")
    elif decision == "PARTIAL":
        parts.append(f"Claim partially approved for ₹{approved} of ₹{claimed} claimed.")
        parts.append("Some line items were excluded — see line-item breakdown for details.")
    return " ".join(parts) if parts else f"Decision: {decision}"
