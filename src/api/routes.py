from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter, HTTPException

from src.core.logger import get_logger
from src.models.claim import ClaimInput
from src.models.decision import DecisionOutput
from src.pipeline.graph import run_pipeline

router = APIRouter()
log = get_logger("api.routes")

_TEST_CASES_PATH = Path(__file__).parent.parent.parent / "tests" / "test_cases.json"


@router.get("/health")
def health():
    log.debug("Health check")
    return {"status": "ok"}


@router.get("/test-cases")
def get_test_cases():
    """Returns all test cases for the Streamlit UI test-case loader."""
    log.debug("Serving test cases list")
    with open(_TEST_CASES_PATH) as f:
        data = json.load(f)
    return data["test_cases"]


@router.post("/claims/submit", response_model=DecisionOutput)
def submit_claim(claim: ClaimInput) -> DecisionOutput:
    log.info(
        "Received claim submission — member=%s category=%s amount=₹%.2f",
        claim.member_id, claim.claim_category, claim.claimed_amount,
    )
    try:
        result = run_pipeline(claim)
        log.info(
            "Returning decision — claim_id=%s decision=%s confidence=%.4f",
            result.claim_id,
            result.decision.value if result.decision else "None",
            result.confidence_score,
        )
        return result
    except Exception as exc:
        log.error("Pipeline error for member=%s: %s", claim.member_id, exc, exc_info=True)
        raise HTTPException(status_code=500, detail=str(exc))
