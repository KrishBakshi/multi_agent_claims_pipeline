from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path


class PolicyLoader:
    """Reads policy_terms.json once and exposes typed accessors.

    All agents receive a PolicyLoader instance at construction time so
    they can be tested with a mock policy without touching the filesystem.
    """

    def __init__(self, path: str | Path | None = None) -> None:
        if path is None:
            path = Path(__file__).parent.parent.parent / "config" / "policy_terms.json"
        with open(path) as f:
            self._data: dict = json.load(f)

    # ── raw access ────────────────────────────────────────────────────────────

    @property
    def raw(self) -> dict:
        return self._data

    # ── member ────────────────────────────────────────────────────────────────

    def get_member(self, member_id: str) -> dict | None:
        return next(
            (m for m in self._data["members"] if m["member_id"] == member_id),
            None,
        )

    # ── document requirements ─────────────────────────────────────────────────

    def get_document_requirements(self, claim_category: str) -> dict | None:
        return self._data.get("document_requirements", {}).get(claim_category.upper())

    # ── coverage & limits ─────────────────────────────────────────────────────

    def get_coverage(self) -> dict:
        return self._data.get("coverage", {})

    def get_opd_category(self, claim_category: str) -> dict | None:
        return self._data.get("opd_categories", {}).get(claim_category.lower())

    # ── policy rules ──────────────────────────────────────────────────────────

    def get_waiting_periods(self) -> dict:
        return self._data.get("waiting_periods", {})

    def get_exclusions(self) -> dict:
        return self._data.get("exclusions", {})

    def get_pre_authorization(self) -> dict:
        return self._data.get("pre_authorization", {})

    def get_submission_rules(self) -> dict:
        return self._data.get("submission_rules", {})

    # ── network hospitals ─────────────────────────────────────────────────────

    def get_network_hospitals(self) -> list[str]:
        return self._data.get("network_hospitals", [])

    def is_network_hospital(self, hospital_name: str | None) -> bool:
        if not hospital_name:
            return False
        h = hospital_name.lower()
        return any(n.lower() in h or h in n.lower() for n in self.get_network_hospitals())

    # ── fraud / manual-review thresholds ─────────────────────────────────────

    def get_fraud_thresholds(self) -> dict:
        return self._data.get("fraud_thresholds", {})


@lru_cache(maxsize=1)
def get_policy_loader() -> PolicyLoader:
    """Module-level singleton — loaded once, reused everywhere."""
    return PolicyLoader()
