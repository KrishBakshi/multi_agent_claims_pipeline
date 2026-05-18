from __future__ import annotations

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class Decision(str, Enum):
    APPROVED = "APPROVED"
    PARTIAL = "PARTIAL"
    REJECTED = "REJECTED"
    MANUAL_REVIEW = "MANUAL_REVIEW"


class TraceEntry(BaseModel):
    agent: str
    step: str
    result: str   # PASS | FAIL | WARNING | ERROR | INFO
    detail: str


class LineItemDecision(BaseModel):
    description: str
    amount: float
    approved: bool
    reason: Optional[str] = None


class AmountBreakdown(BaseModel):
    claimed_amount: float
    network_discount_percent: Optional[float] = None
    network_discount_amount: Optional[float] = None
    amount_after_discount: Optional[float] = None
    copay_percent: Optional[float] = None
    copay_amount: Optional[float] = None
    sub_limit_applied: Optional[float] = None
    approved_amount: float


class DecisionOutput(BaseModel):
    claim_id: str
    decision: Optional[Decision]
    approved_amount: Optional[float] = None
    reason: str
    rejection_reasons: list[str] = Field(default_factory=list)
    confidence_score: float
    trace: list[TraceEntry] = Field(default_factory=list)
    component_failures: list[str] = Field(default_factory=list)
    manual_review_signals: list[str] = Field(default_factory=list)
    line_item_decisions: list[LineItemDecision] = Field(default_factory=list)
    breakdown: Optional[AmountBreakdown] = None
    manual_review_recommended: bool = False
    halt_message: Optional[str] = None
