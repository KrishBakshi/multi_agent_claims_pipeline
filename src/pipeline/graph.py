"""LangGraph pipeline graph.

Nodes (in execution order):
  data_validator  →  doc_parser  →  doc_validator  →  decision_maker

Conditional edges:
  - After data_validator : if halted → END, else → doc_parser
  - After doc_validator  : if halted → END, else → decision_maker

Any node can set halted=True to short-circuit the remaining pipeline.
The orchestrator wraps each node in a safe executor so exceptions degrade
confidence rather than crashing the graph.
"""
from __future__ import annotations

import uuid
from typing import Any

from langgraph.graph import END, StateGraph

from src.agents.data_validator import build_data_validator
from src.agents.decision_maker import build_decision_maker
from src.agents.doc_parser import build_doc_parser
from src.agents.doc_validator import build_doc_validator
from src.core.logger import claim_logger, get_logger
from src.core.policy_loader import PolicyLoader, get_policy_loader
from src.models.claim import ClaimInput
from src.models.decision import (
    AmountBreakdown,
    DecisionOutput,
    LineItemDecision,
    TraceEntry,
)
from src.models.state import ClaimState

_log = get_logger("pipeline.graph")


# ── safe node wrapper ─────────────────────────────────────────────────────────

def _safe(node_name: str, fn):
    """Wraps a node function so unhandled exceptions degrade confidence
    instead of crashing the LangGraph execution."""

    def wrapper(state: ClaimState) -> dict:
        claim_id = state.get("claim_id", "--------")
        log = claim_logger("pipeline.graph", claim_id)
        log.debug("→ entering node: %s", node_name)
        try:
            result = fn(state)
            log.debug("← exiting node: %s", node_name)
            return result or {}
        except Exception as exc:
            log.error(
                "Node '%s' raised unhandled exception: %s",
                node_name, exc, exc_info=True,
            )
            penalty = 0.20
            current_conf = state.get("confidence", 1.0)
            return {
                "component_failures": [node_name],
                "confidence": max(0.0, current_conf - penalty),
                "manual_review_recommended": True,
                "trace": [
                    {
                        "agent": node_name,
                        "step": "execution",
                        "result": "ERROR",
                        "detail": f"Unhandled exception: {exc}",
                    }
                ],
            }

    wrapper.__name__ = node_name
    return wrapper


# ── routing helpers ───────────────────────────────────────────────────────────

def _route_after_data_validator(state: ClaimState) -> str:
    return END if state.get("halted") else "doc_parser"


def _route_after_doc_validator(state: ClaimState) -> str:
    return END if state.get("halted") else "decision_maker"


# ── graph factory ─────────────────────────────────────────────────────────────

def build_pipeline(policy: PolicyLoader | None = None):
    """Compiles and returns the LangGraph pipeline.

    Args:
        policy: Optional PolicyLoader. Defaults to the module-level singleton.

    Returns:
        A compiled LangGraph runnable.
    """
    if policy is None:
        policy = get_policy_loader()

    data_validator_fn = build_data_validator(policy)
    doc_parser_fn = build_doc_parser()
    doc_validator_fn = build_doc_validator(policy)
    decision_maker_fn = build_decision_maker(policy)

    builder: StateGraph = StateGraph(ClaimState)

    builder.add_node("data_validator", _safe("DataValidatorAgent", data_validator_fn))
    builder.add_node("doc_parser", _safe("DocParserAgent", doc_parser_fn))
    builder.add_node("doc_validator", _safe("DocValidatorAgent", doc_validator_fn))
    builder.add_node("decision_maker", _safe("DecisionMakerAgent", decision_maker_fn))

    builder.set_entry_point("data_validator")

    builder.add_conditional_edges(
        "data_validator",
        _route_after_data_validator,
        {"doc_parser": "doc_parser", END: END},
    )
    builder.add_edge("doc_parser", "doc_validator")
    builder.add_conditional_edges(
        "doc_validator",
        _route_after_doc_validator,
        {"decision_maker": "decision_maker", END: END},
    )
    builder.add_edge("decision_maker", END)

    return builder.compile()


# ── public run interface ──────────────────────────────────────────────────────

def run_pipeline(claim: ClaimInput, policy: PolicyLoader | None = None) -> DecisionOutput:
    """Entry point for running a claim through the full pipeline.

    Args:
        claim:  Validated ClaimInput Pydantic model.
        policy: Optional PolicyLoader override (useful for testing).

    Returns:
        DecisionOutput with decision, amounts, trace, and confidence.
    """
    pipeline = build_pipeline(policy)
    claim_id = str(uuid.uuid4())[:8].upper()
    log = claim_logger("pipeline.graph", claim_id)

    log.info(
        "Pipeline started — member=%s category=%s amount=₹%.2f docs=%d simulate_failure=%s",
        claim.member_id,
        claim.claim_category,
        claim.claimed_amount,
        len(claim.documents),
        claim.simulate_component_failure,
    )

    initial_state: ClaimState = {
        "claim_id": claim_id,
        "claim_input": claim.model_dump(),
        "member": None,
        "policy": None,
        "extracted_docs": [],
        "halted": False,
        "halt_message": None,
        "decision": None,
        "approved_amount": None,
        "breakdown": None,
        "line_item_decisions": [],
        "reason": "",
        "trace": [],
        "component_failures": [],
        "rejection_reasons": [],
        "manual_review_signals": [],
        "confidence": 1.0,
        "manual_review_recommended": False,
    }

    final_state: ClaimState = pipeline.invoke(initial_state)
    output = _state_to_output(claim_id, final_state)

    if final_state.get("halted"):
        log.warning(
            "Pipeline halted early — reason: %s",
            final_state.get("halt_message", "unknown"),
        )
    else:
        log.info(
            "Pipeline complete — decision=%s approved=₹%s confidence=%.4f failures=%s",
            output.decision.value if output.decision else "None",
            f"{output.approved_amount:.2f}" if output.approved_amount is not None else "—",
            output.confidence_score,
            output.component_failures or "none",
        )

    return output


def _state_to_output(claim_id: str, state: ClaimState) -> DecisionOutput:
    from src.models.decision import Decision

    # Halted early (doc / data validation failure)
    if state.get("halted"):
        return DecisionOutput(
            claim_id=claim_id,
            decision=None,
            approved_amount=None,
            reason=state.get("halt_message") or "Claim stopped during validation.",
            rejection_reasons=state.get("rejection_reasons") or [],
            confidence_score=round(state.get("confidence", 0.5), 4),
            trace=[TraceEntry(**t) for t in (state.get("trace") or [])],
            component_failures=state.get("component_failures") or [],
            manual_review_signals=state.get("manual_review_signals") or [],
            line_item_decisions=[],
            breakdown=None,
            manual_review_recommended=False,
            halt_message=state.get("halt_message"),
        )

    decision_str = state.get("decision")
    decision = Decision(decision_str) if decision_str else None

    breakdown = None
    if state.get("breakdown"):
        breakdown = AmountBreakdown(**state["breakdown"])

    line_items = [LineItemDecision(**li) for li in (state.get("line_item_decisions") or [])]
    trace = [TraceEntry(**t) for t in (state.get("trace") or [])]

    return DecisionOutput(
        claim_id=claim_id,
        decision=decision,
        approved_amount=state.get("approved_amount"),
        reason=state.get("reason") or "",
        rejection_reasons=state.get("rejection_reasons") or [],
        confidence_score=round(state.get("confidence", 1.0), 4),
        trace=trace,
        component_failures=state.get("component_failures") or [],
        manual_review_signals=state.get("manual_review_signals") or [],
        line_item_decisions=line_items,
        breakdown=breakdown,
        manual_review_recommended=state.get("manual_review_recommended", False),
        halt_message=None,
    )
