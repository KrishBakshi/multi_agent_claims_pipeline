"""End-to-end pipeline tests against all 12 test cases.

Each test asserts the exact expected outcome described in test_cases.json.
Where the expected outcome is a decision enum, that is verified directly.
Where it is a set of system_must conditions, those are verified against the
output fields and trace content.
"""
from __future__ import annotations

import pytest

from src.pipeline.graph import run_pipeline
from tests.conftest import build_claim


# ── TC001 — Wrong Document Uploaded ──────────────────────────────────────────

def test_tc001_wrong_document(all_test_cases, policy):
    tc = next(t for t in all_test_cases if t["case_id"] == "TC001")
    claim = build_claim(tc["input"])
    result = run_pipeline(claim, policy)

    assert result.decision is None, "Pipeline must stop before making a decision"
    assert result.halt_message is not None
    assert "HOSPITAL_BILL" in result.halt_message, \
        "Error must name the required document type"
    assert "PRESCRIPTION" in result.halt_message, \
        "Error must name the uploaded document type"


# ── TC002 — Unreadable Document ───────────────────────────────────────────────

def test_tc002_unreadable_document(all_test_cases, policy):
    tc = next(t for t in all_test_cases if t["case_id"] == "TC002")
    claim = build_claim(tc["input"])
    result = run_pipeline(claim, policy)

    assert result.decision is None, "Should not produce a claim decision"
    assert result.halt_message is not None
    msg = result.halt_message.lower()
    assert "unreadable" in msg or "cannot be read" in msg or "re-upload" in msg, \
        "Message must ask member to re-upload"
    # Must NOT be a hard rejection
    assert result.rejection_reasons == [] or "UNREADABLE" not in result.rejection_reasons


# ── TC003 — Documents Belong to Different Patients ────────────────────────────

def test_tc003_patient_name_mismatch(all_test_cases, policy):
    tc = next(t for t in all_test_cases if t["case_id"] == "TC003")
    claim = build_claim(tc["input"])
    result = run_pipeline(claim, policy)

    assert result.decision is None
    assert result.halt_message is not None
    msg = result.halt_message
    assert "Rajesh Kumar" in msg, "Must name the patient on the prescription"
    assert "Arjun Mehta" in msg, "Must name the patient on the bill"


# ── TC004 — Clean Consultation Full Approval ──────────────────────────────────

def test_tc004_clean_approval(all_test_cases, policy):
    tc = next(t for t in all_test_cases if t["case_id"] == "TC004")
    claim = build_claim(tc["input"])
    result = run_pipeline(claim, policy)

    assert result.decision is not None
    assert result.decision.value == "APPROVED"
    assert result.approved_amount == pytest.approx(1350.0, abs=1.0), \
        "10% co-pay on ₹1500 = ₹1350"
    assert result.confidence_score >= 0.85


# ── TC005 — Waiting Period Diabetes ──────────────────────────────────────────

def test_tc005_waiting_period_diabetes(all_test_cases, policy):
    tc = next(t for t in all_test_cases if t["case_id"] == "TC005")
    claim = build_claim(tc["input"])
    result = run_pipeline(claim, policy)

    assert result.decision is not None
    assert result.decision.value == "REJECTED"
    assert "WAITING_PERIOD" in result.rejection_reasons
    # Must state when member becomes eligible
    assert "2024-11-30" in result.reason or "eligible" in result.reason.lower()


# ── TC006 — Dental Partial Approval ──────────────────────────────────────────

def test_tc006_dental_partial(all_test_cases, policy):
    tc = next(t for t in all_test_cases if t["case_id"] == "TC006")
    claim = build_claim(tc["input"])
    result = run_pipeline(claim, policy)

    assert result.decision is not None
    assert result.decision.value == "PARTIAL"
    assert result.approved_amount == pytest.approx(8000.0, abs=1.0)
    # Line-item decisions must exist
    assert len(result.line_item_decisions) > 0
    rejected_items = [li for li in result.line_item_decisions if not li.approved]
    assert any("whitening" in li.description.lower() for li in rejected_items), \
        "Teeth whitening must be in rejected items"


# ── TC007 — MRI Without Pre-Auth ─────────────────────────────────────────────

def test_tc007_pre_auth_missing(all_test_cases, policy):
    tc = next(t for t in all_test_cases if t["case_id"] == "TC007")
    claim = build_claim(tc["input"])
    result = run_pipeline(claim, policy)

    assert result.decision is not None
    assert result.decision.value == "REJECTED"
    assert "PRE_AUTH_MISSING" in result.rejection_reasons
    assert "pre-auth" in result.reason.lower() or "pre-authoris" in result.reason.lower()


# ── TC008 — Per-Claim Limit Exceeded ─────────────────────────────────────────

def test_tc008_per_claim_exceeded(all_test_cases, policy):
    tc = next(t for t in all_test_cases if t["case_id"] == "TC008")
    claim = build_claim(tc["input"])
    result = run_pipeline(claim, policy)

    assert result.decision is not None
    assert result.decision.value == "REJECTED"
    assert "PER_CLAIM_EXCEEDED" in result.rejection_reasons
    assert "5000" in result.reason or "5,000" in result.reason, \
        "Rejection message must state the per-claim limit"
    assert "7500" in result.reason or "7,500" in result.reason, \
        "Rejection message must state the claimed amount"


# ── TC009 — Fraud Signal Multiple Same-Day Claims ─────────────────────────────

def test_tc009_fraud_manual_review(all_test_cases, policy):
    tc = next(t for t in all_test_cases if t["case_id"] == "TC009")
    claim = build_claim(tc["input"])
    result = run_pipeline(claim, policy)

    assert result.decision is not None
    assert result.decision.value == "MANUAL_REVIEW"
    assert len(result.manual_review_signals) > 0
    signals_text = " ".join(result.manual_review_signals).lower()
    assert "same-day" in signals_text or "same day" in signals_text or "2024-10-30" in signals_text


# ── TC010 — Network Hospital Discount + Co-pay ───────────────────────────────

def test_tc010_network_discount(all_test_cases, policy):
    tc = next(t for t in all_test_cases if t["case_id"] == "TC010")
    claim = build_claim(tc["input"])
    result = run_pipeline(claim, policy)

    assert result.decision is not None
    assert result.decision.value == "APPROVED"
    assert result.approved_amount == pytest.approx(3240.0, abs=1.0), \
        "Network discount 20% then co-pay 10%: 4500 * 0.8 * 0.9 = 3240"
    assert result.breakdown is not None
    assert result.breakdown.network_discount_percent == pytest.approx(20.0)
    assert result.breakdown.copay_percent == pytest.approx(10.0)


# ── TC011 — Component Failure Graceful Degradation ───────────────────────────

def test_tc011_graceful_degradation(all_test_cases, policy):
    tc = next(t for t in all_test_cases if t["case_id"] == "TC011")
    claim = build_claim(tc["input"])
    result = run_pipeline(claim, policy)

    # Must not crash and must produce a decision
    assert result.decision is not None, "Pipeline must not crash"
    assert result.decision.value == "APPROVED"
    # Confidence must be reduced
    assert result.confidence_score < 1.0, "Confidence must be reduced after component failure"
    assert len(result.component_failures) > 0, "Must record the failed component"


# ── TC012 — Excluded Treatment ────────────────────────────────────────────────

def test_tc012_excluded_treatment(all_test_cases, policy):
    tc = next(t for t in all_test_cases if t["case_id"] == "TC012")
    claim = build_claim(tc["input"])
    result = run_pipeline(claim, policy)

    assert result.decision is not None
    assert result.decision.value == "REJECTED"
    assert "EXCLUDED_CONDITION" in result.rejection_reasons
    assert result.confidence_score >= 0.90
