"""DocValidatorAgent — LangGraph node.

Runs three checks against extracted documents BEFORE any policy-rule logic:

  1. Required document types present for the claim category (per policy doc_requirements)
  2. UNREADABLE documents — halt and ask member to re-upload the specific file
  3. Patient name consistency — all named documents must reference the same patient

Any failure produces a specific, actionable halt message so the member knows
exactly what to fix. Generic errors are not acceptable per the assignment brief.
"""
from __future__ import annotations

from collections import Counter
from typing import Optional

from src.core.logger import claim_logger
from src.core.policy_loader import PolicyLoader
from src.models.state import ClaimState

CONFIDENCE_PENALTY = 0.15


def _t(agent: str, step: str, result: str, detail: str) -> dict:
    return {"agent": agent, "step": step, "result": result, "detail": detail}


def build_doc_validator(policy: PolicyLoader):
    """Returns a LangGraph-compatible node function closed over `policy`."""

    def doc_validator_node(state: ClaimState) -> dict:
        if state.get("halted"):
            return {}

        agent = "DocValidatorAgent"
        claim_id = state.get("claim_id", "--------")
        log = claim_logger("agents.doc_validator", claim_id)

        inp = state["claim_input"]
        category = inp["claim_category"].upper()
        docs = inp["documents"]
        extracted = state.get("extracted_docs", [])
        trace: list[dict] = []
        confidence: float = state.get("confidence", 1.0)

        log.info("Starting — category=%s docs=%d", category, len(docs))

        # ── TC011 simulated failure ──────────────────────────────────────────
        if inp.get("simulate_component_failure"):
            log.warning("Simulated component failure triggered — skipping doc validation")
            trace.append(_t(agent, "simulate_failure", "ERROR",
                            "Simulated component failure in DocValidatorAgent — skipping doc validation"))
            confidence = max(0.0, confidence - CONFIDENCE_PENALTY)
            return {
                "halted": False,
                "halt_message": None,
                "confidence": confidence,
                "trace": trace,
                "component_failures": [agent],
                "manual_review_recommended": True,
            }

        def halt(step: str, message: str) -> dict:
            log.warning("HALT [%s] — %s", step, message)
            trace.append(_t(agent, step, "FAIL", message))
            return {
                "halted": True,
                "halt_message": message,
                "confidence": max(0.0, confidence - CONFIDENCE_PENALTY),
                "trace": trace,
                "component_failures": [],
                "manual_review_recommended": False,
            }

        # ── Check 1: UNREADABLE documents ────────────────────────────────────
        unreadable = [d for d in docs if d.get("quality") == "UNREADABLE"]
        if unreadable:
            names = ", ".join(
                f"{d['actual_type']} (file: {d.get('file_name') or d['file_id']})"
                for d in unreadable
            )
            log.warning("Unreadable documents detected: %s", names)
            return halt(
                "doc_quality",
                f"The following document(s) could not be read: {names}. "
                f"Please re-upload a clear, well-lit photo or scan of each.",
            )

        # ── Check 2: Required document types ─────────────────────────────────
        req = policy.get_document_requirements(category)
        if req is None:
            log.warning("No document requirements configured for category '%s' — skipping type check", category)
            trace.append(_t(agent, "doc_requirements", "WARNING",
                            f"No document requirements found for category '{category}' — skipping type check"))
        else:
            required_types: list[str] = req.get("required", [])
            uploaded_types = [d["actual_type"].upper() for d in docs]
            type_counts = Counter(uploaded_types)

            log.debug(
                "Required types: %s | Uploaded: %s",
                required_types,
                dict(type_counts),
            )

            missing = [rt for rt in required_types if rt not in type_counts]
            if missing:
                uploaded_summary = ", ".join(
                    f"{count}× {dt}" for dt, count in type_counts.items()
                )
                missing_summary = ", ".join(missing)
                log.warning(
                    "Missing required documents: %s (uploaded: %s)",
                    missing_summary, uploaded_summary,
                )
                return halt(
                    "doc_types",
                    f"Missing required document(s) for a {category} claim: {missing_summary}. "
                    f"You uploaded: {uploaded_summary}. "
                    f"Please provide the missing document(s) and resubmit.",
                )
            log.info("PASS doc_types — all required docs present: %s", ", ".join(required_types))
            trace.append(_t(agent, "doc_types", "PASS",
                            f"All required documents present for {category}: "
                            f"{', '.join(required_types)}"))

        # ── Check 3: Patient name consistency ─────────────────────────────────
        named: list[tuple[str, str, str]] = []
        for doc in docs:
            extracted_doc = next(
                (e for e in extracted if e["file_id"] == doc["file_id"]), None
            )
            name: Optional[str] = None
            if extracted_doc:
                name = extracted_doc.get("patient_name")
            if not name:
                name = doc.get("patient_name_on_doc")
            if name:
                named.append((doc["file_id"], doc["actual_type"], _normalise_name(name)))

        if len(named) >= 2:
            unique_names = {n for _, _, n in named}
            if len(unique_names) > 1:
                name_report = "; ".join(
                    f"{doc_type} ({fid}): '{name}'" for fid, doc_type, name in named
                )
                log.warning("Patient name mismatch across documents: %s", name_report)
                return halt(
                    "patient_name_consistency",
                    f"Documents appear to belong to different patients: {name_report}. "
                    f"All documents in a single claim must be for the same patient. "
                    f"Please review and resubmit with matching documents.",
                )
            matched_name = next(iter(unique_names))
            log.info("PASS patient_name_consistency — all docs reference '%s'", matched_name)
            trace.append(_t(agent, "patient_name_consistency", "PASS",
                            f"All named documents reference the same patient: '{matched_name}'"))

        log.info("Complete — all document checks passed")
        trace.append(_t(agent, "doc_validation", "PASS",
                        "Document validation passed all checks"))
        return {
            "halted": False,
            "halt_message": None,
            "confidence": confidence,
            "trace": trace,
            "component_failures": [],
            "manual_review_recommended": False,
        }

    return doc_validator_node


def _normalise_name(name: str) -> str:
    return " ".join(name.lower().split())
