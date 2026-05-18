from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field


class LineItem(BaseModel):
    description: str
    amount: float


class DocumentContent(BaseModel):
    """Pre-extracted content — provided by test cases or after vision extraction."""
    patient_name: Optional[str] = None
    doctor_name: Optional[str] = None
    doctor_registration: Optional[str] = None
    hospital_name: Optional[str] = None
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    date: Optional[str] = None
    medicines: Optional[list[str]] = None
    tests_ordered: Optional[list[str]] = None
    line_items: Optional[list[LineItem]] = None
    total: Optional[float] = None
    test_name: Optional[str] = None

    model_config = {"extra": "allow"}


class Document(BaseModel):
    file_id: str
    file_name: Optional[str] = None
    # PRESCRIPTION | HOSPITAL_BILL | LAB_REPORT | PHARMACY_BILL | DENTAL_REPORT | DISCHARGE_SUMMARY
    actual_type: str
    quality: str = "GOOD"          # GOOD | UNREADABLE | LOW
    patient_name_on_doc: Optional[str] = None
    content: Optional[DocumentContent] = None
    # Populated for real file uploads; None for test-case submissions
    file_data: Optional[bytes] = None
    media_type: Optional[str] = None


class ClaimsHistory(BaseModel):
    claim_id: str
    date: str
    amount: float
    provider: Optional[str] = None


class ClaimInput(BaseModel):
    member_id: str
    policy_id: str
    # CONSULTATION | DIAGNOSTIC | PHARMACY | DENTAL | VISION | ALTERNATIVE_MEDICINE
    claim_category: str
    treatment_date: str            # YYYY-MM-DD
    claimed_amount: float
    documents: list[Document]
    hospital_name: Optional[str] = None
    ytd_claims_amount: float = 0.0
    claims_history: list[ClaimsHistory] = Field(default_factory=list)
    simulate_component_failure: bool = False
