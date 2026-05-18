"""LangGraph pipeline state.

List fields annotated with operator.add are append-only — each node's
returned list is appended to the existing one rather than overwriting it.
Scalar fields (confidence, halted, decision, etc.) are simply overwritten
by whichever node last touched them.
"""
from __future__ import annotations

import operator
from typing import Annotated, Optional, TypedDict


class ClaimState(TypedDict):
    # ── set at pipeline entry ────────────────────────────────────────────────
    claim_id: str
    claim_input: dict          # ClaimInput.model_dump()

    # ── set by DataValidatorAgent ────────────────────────────────────────────
    member: Optional[dict]
    policy: Optional[dict]

    # ── set by DocParserAgent ────────────────────────────────────────────────
    extracted_docs: list[dict]  # list of ExtractedDocument dicts

    # ── pipeline control (overwritten per node) ──────────────────────────────
    halted: bool
    halt_message: Optional[str]

    # ── set by DecisionMakerAgent ────────────────────────────────────────────
    decision: Optional[str]
    approved_amount: Optional[float]
    breakdown: Optional[dict]
    line_item_decisions: list[dict]
    reason: str

    # ── accumulating lists (append-only across nodes) ────────────────────────
    trace: Annotated[list[dict], operator.add]
    component_failures: Annotated[list[str], operator.add]
    rejection_reasons: Annotated[list[str], operator.add]
    manual_review_signals: Annotated[list[str], operator.add]

    # ── scalars overwritten per node ─────────────────────────────────────────
    confidence: float
    manual_review_recommended: bool
