from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.core.policy_loader import PolicyLoader
from src.models.claim import ClaimInput, Document, DocumentContent, LineItem, ClaimsHistory

TEST_CASES_PATH = Path(__file__).parent / "test_cases.json"
POLICY_PATH = Path(__file__).parent.parent / "config" / "policy_terms.json"


@pytest.fixture(scope="session")
def policy() -> PolicyLoader:
    return PolicyLoader(POLICY_PATH)


@pytest.fixture(scope="session")
def all_test_cases() -> list[dict]:
    with open(TEST_CASES_PATH) as f:
        return json.load(f)["test_cases"]


def build_claim(tc_input: dict) -> ClaimInput:
    docs = []
    for d in tc_input.get("documents", []):
        content_raw = d.get("content")
        content = None
        if content_raw:
            raw = dict(content_raw)
            if raw.get("line_items"):
                raw["line_items"] = [LineItem(**li) for li in raw["line_items"]]
            content = DocumentContent(**raw)
        docs.append(Document(
            file_id=d.get("file_id", ""),
            file_name=d.get("file_name"),
            actual_type=d.get("actual_type", ""),
            quality=d.get("quality", "GOOD"),
            patient_name_on_doc=d.get("patient_name_on_doc"),
            content=content,
        ))

    history = [ClaimsHistory(**h) for h in tc_input.get("claims_history", [])]

    return ClaimInput(
        member_id=tc_input["member_id"],
        policy_id=tc_input["policy_id"],
        claim_category=tc_input["claim_category"],
        treatment_date=tc_input["treatment_date"],
        claimed_amount=tc_input["claimed_amount"],
        documents=docs,
        hospital_name=tc_input.get("hospital_name"),
        ytd_claims_amount=tc_input.get("ytd_claims_amount", 0.0),
        claims_history=history,
        simulate_component_failure=tc_input.get("simulate_component_failure", False),
    )
