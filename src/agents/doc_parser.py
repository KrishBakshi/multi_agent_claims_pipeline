"""DocParserAgent — LangGraph node.

Extracts structured fields from each uploaded document.

Dual-mode operation:
  - Test / demo mode : document.content is already populated → use directly.
  - Production mode  : document.file_data is present → run Gemini Vision OCR
                       which returns a structured ExtractedDocument JSON in one
                       API call (no separate regex parsing step).

Gemini Vision pipeline (production):
  1. _pdf_first_page_to_png() — PDF bytes → PNG at 150 DPI (if needed)
  2. _letterbox()             — resize to 640×640 square (single Vision tile,
                                 fewer tokens)
  3. _from_gemini_ocr()       — base64 PNG + prompt → Gemini API →
                                 ExtractedDocument JSON

If a document is marked UNREADABLE the agent records it in the trace,
degrades confidence, and adds a stub so downstream agents know the doc
exists but could not be read.
"""
from __future__ import annotations

import base64
import io
import json
import os

import pymupdf
from PIL import Image
import google.generativeai as genai

from src.core.logger import claim_logger
from src.models.state import ClaimState

CONFIDENCE_PENALTY_UNREADABLE = 0.15
CONFIDENCE_PENALTY_PARSE_ERROR = 0.10

_LETTERBOX_SIZE = 640

# Schema mirrors the ExtractedDocument dict consumed by DecisionMakerAgent
# via state["extracted_docs"].
_EXTRACTION_PROMPT = """\
You are a medical document extraction assistant specialised in Indian healthcare documents.

Extract all information from this document image and return it as a single JSON object
with exactly these fields:

{
  "file_id": "doc_001",
  "doc_type": "<HOSPITAL_BILL | PRESCRIPTION | LAB_REPORT | PHARMACY_BILL | DISCHARGE_SUMMARY>",
  "patient_name": "<full patient name or null>",
  "doctor_name": "<doctor full name with Dr. prefix or null>",
  "doctor_registration": "<registration number e.g. KA/45678/2015 or null>",
  "hospital_name": "<hospital or clinic name or null>",
  "diagnosis": "<diagnosis text or null>",
  "treatment": "<treatment or procedure description or null>",
  "date": "<date as found on the document, e.g. 2024-11-01 or null>",
  "medicines": ["<medicine name>"],
  "tests_ordered": ["<test name>"],
  "line_items": [
    {"description": "<item description>", "amount": <number>}
  ],
  "total_amount": <number or null>,
  "quality": "GOOD",
  "confidence": <number between 0.0 and 1.0>,
  "extraction_notes": ["<note about any field that could not be reliably read>"]
}

Rules:
- Return ONLY the JSON object — no markdown fences, no extra prose.
- Use JSON null (not the string "N/A") for any missing field.
- medicines: populate only when doc_type is PHARMACY_BILL or PRESCRIPTION; otherwise [].
- tests_ordered: populate only when doc_type is LAB_REPORT or DIAGNOSTIC; otherwise [].
- line_items: include every row from the bill/receipt table with its amount as a number.
- total_amount: the final payable total as a number; null if not present.
- confidence: 0.95 if all key fields found; reduce by 0.1 for each key field missing.
- extraction_notes: list any fields that were missing, ambiguous, or partially readable.
"""


# ── PDF → image conversion ────────────────────────────────────────────────────

def _pdf_first_page_to_png(file_data: bytes) -> bytes:
    with pymupdf.open(stream=file_data, filetype="pdf") as doc:
        page = doc.load_page(0)
        pix = page.get_pixmap(dpi=150)
        return pix.tobytes("png")


# ── Image size guard ──────────────────────────────────────────────────────────

def _letterbox(image_bytes: bytes) -> bytes:
    """Fit image into a _LETTERBOX_SIZE square with white padding, aspect-ratio-safe."""
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    w, h = img.size
    scale = _LETTERBOX_SIZE / max(w, h)
    new_w, new_h = int(w * scale), int(h * scale)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    canvas = Image.new("RGB", (_LETTERBOX_SIZE, _LETTERBOX_SIZE), (255, 255, 255))
    canvas.paste(img, ((_LETTERBOX_SIZE - new_w) // 2, (_LETTERBOX_SIZE - new_h) // 2))
    buf = io.BytesIO()
    canvas.save(buf, format="PNG")
    return buf.getvalue()


# ── per-document extraction modes ────────────────────────────────────────────

def _t(agent: str, step: str, result: str, detail: str) -> dict:
    return {"agent": agent, "step": step, "result": result, "detail": detail}


def _from_content(doc: dict) -> dict:
    """Build an extracted-doc dict from test-case pre-supplied content."""
    c = doc.get("content") or {}
    patient_name = doc.get("patient_name_on_doc") or c.get("patient_name")
    line_items = [
        {"description": li["description"], "amount": li["amount"]}
        for li in (c.get("line_items") or [])
    ]
    return {
        "file_id": doc["file_id"],
        "doc_type": doc["actual_type"],
        "patient_name": patient_name,
        "doctor_name": c.get("doctor_name"),
        "doctor_registration": c.get("doctor_registration"),
        "hospital_name": c.get("hospital_name"),
        "diagnosis": c.get("diagnosis"),
        "treatment": c.get("treatment"),
        "date": c.get("date"),
        "medicines": c.get("medicines") or [],
        "tests_ordered": c.get("tests_ordered") or [],
        "line_items": line_items,
        "total_amount": c.get("total"),
        "quality": doc.get("quality", "GOOD"),
        "confidence": 1.0,
        "extraction_notes": [],
    }


def _from_gemini_ocr(doc: dict) -> dict:
    """Gemini Vision production path: image → structured ExtractedDocument JSON.

    Step 1 — PDF → PNG (if needed) + letterbox to 640×640.
    Step 2 — POST to Gemini with response_mime_type=application/json.
    Step 3 — Inject file_id (not visible in the image) and honour the declared
             doc type, noting any mismatch with what Gemini inferred.
    """
    file_data: bytes = doc["file_data"]
    media_type: str = doc.get("media_type") or "image/jpeg"

    if "pdf" in media_type.lower():
        file_data = _pdf_first_page_to_png(file_data)

    lb_bytes = _letterbox(file_data)
    b64 = base64.b64encode(lb_bytes).decode("utf-8")

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError("GOOGLE_API_KEY not set")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-3.1-flash-lite")

    response = model.generate_content(
        [
            _EXTRACTION_PROMPT,
            {"inline_data": {"mime_type": "image/png", "data": b64}},
        ],
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json",
        ),
    )
    fields: dict = json.loads(response.text)

    # file_id is pipeline metadata, not visible in the image — always override.
    fields["file_id"] = doc["file_id"]

    # Doc-type: honour declared type if provided; note if Gemini disagrees.
    declared = (doc.get("actual_type") or "UNKNOWN").upper()
    inferred = (fields.get("doc_type") or "HOSPITAL_BILL").upper()
    classifier_notes: list[str] = []

    if declared in ("", "UNKNOWN"):
        fields["doc_type"] = inferred
        classifier_notes.append(f"Doc type inferred by Gemini Vision: {inferred}")
    else:
        fields["doc_type"] = declared
        if inferred != declared:
            classifier_notes.append(
                f"Gemini inferred {inferred} but document is declared {declared} — "
                "verify the correct document was uploaded"
            )

    fields.setdefault("medicines", [])
    fields.setdefault("tests_ordered", [])
    fields.setdefault("line_items", [])
    fields.setdefault("quality", doc.get("quality", "GOOD"))

    existing_notes: list[str] = fields.get("extraction_notes") or []
    fields["extraction_notes"] = classifier_notes + existing_notes

    if fields["extraction_notes"]:
        fields["confidence"] = min(fields.get("confidence", 0.95), 0.60)

    return fields


# ── LangGraph node ────────────────────────────────────────────────────────────

def build_doc_parser():
    """Returns a LangGraph-compatible node function."""

    def doc_parser_node(state: ClaimState) -> dict:
        if state.get("halted"):
            return {}

        agent = "DocParserAgent"
        claim_id = state.get("claim_id", "--------")
        log = claim_logger("agents.doc_parser", claim_id)

        inp = state["claim_input"]
        docs = inp["documents"]
        trace: list[dict] = []
        extracted: list[dict] = []
        failures: list[str] = []
        confidence: float = state.get("confidence", 1.0)

        log.info("Starting — parsing %d document(s)", len(docs))

        for doc in docs:
            fid = doc["file_id"]
            doc_type = doc["actual_type"]

            # UNREADABLE — record and degrade, do not attempt parse
            if doc.get("quality") == "UNREADABLE":
                log.warning("UNREADABLE %s (file_id=%s) — member must re-upload", doc_type, fid)
                confidence = max(0.0, confidence - CONFIDENCE_PENALTY_UNREADABLE)
                trace.append(_t(agent, f"quality_{fid}", "WARNING",
                                f"{doc_type} (file_id={fid}) is unreadable — "
                                f"member must re-upload a clear copy"))
                extracted.append({
                    "file_id": fid,
                    "doc_type": doc_type,
                    "patient_name": None,
                    "quality": "UNREADABLE",
                    "confidence": 0.0,
                    "extraction_notes": ["Document is unreadable — please re-upload a clear copy"],
                    "line_items": [],
                    "medicines": [],
                    "tests_ordered": [],
                })
                continue

            try:
                if doc.get("content") is not None:
                    log.debug("Parsing %s (file_id=%s) from pre-supplied content", doc_type, fid)
                    result = _from_content(doc)
                    log.debug(
                        "Extracted %s — patient=%s diagnosis=%s items=%d",
                        doc_type,
                        result.get("patient_name") or "—",
                        result.get("diagnosis") or "—",
                        len(result.get("line_items") or []),
                    )
                elif doc.get("file_data"):
                    log.info("Running Gemini Vision OCR for %s (file_id=%s)", doc_type, fid)
                    result = _from_gemini_ocr(doc)
                    if result.get("extraction_notes"):
                        log.warning(
                            "OCR extraction notes for %s: %s",
                            fid, "; ".join(result["extraction_notes"]),
                        )
                    log.info(
                        "Gemini Vision OCR complete — confidence=%.2f patient=%s",
                        result["confidence"],
                        result.get("patient_name") or "—",
                    )
                else:
                    log.warning("No content or file_data for %s (file_id=%s) — skipping", doc_type, fid)
                    confidence = max(0.0, confidence - CONFIDENCE_PENALTY_PARSE_ERROR)
                    trace.append(_t(agent, f"parse_{fid}", "WARNING",
                                    f"No content or file data for {fid} — skipping"))
                    extracted.append({
                        "file_id": fid,
                        "doc_type": doc_type,
                        "patient_name": None,
                        "quality": "UNKNOWN",
                        "confidence": 0.3,
                        "extraction_notes": ["No content or file data provided"],
                        "line_items": [],
                        "medicines": [],
                        "tests_ordered": [],
                    })
                    continue

                extracted.append(result)
                trace.append(_t(agent, f"parse_{fid}", "PASS",
                                f"Parsed {doc_type} "
                                f"(quality={doc.get('quality', 'GOOD')}, "
                                f"confidence={result['confidence']:.2f})"))

            except Exception as exc:
                log.error(
                    "Extraction failed for %s (file_id=%s): %s",
                    doc_type, fid, exc, exc_info=True,
                )
                failures.append(f"{agent}:{fid}")
                confidence = max(0.0, confidence - CONFIDENCE_PENALTY_PARSE_ERROR)
                trace.append(_t(agent, f"parse_{fid}", "ERROR",
                                f"Extraction failed for {fid}: {exc}"))
                extracted.append({
                    "file_id": fid,
                    "doc_type": doc_type,
                    "patient_name": None,
                    "quality": "ERROR",
                    "confidence": 0.0,
                    "extraction_notes": [f"Extraction failed: {exc}"],
                    "line_items": [],
                    "medicines": [],
                    "tests_ordered": [],
                })

        log.info(
            "Complete — %d extracted, %d failed, confidence=%.2f",
            len(extracted), len(failures), confidence,
        )
        return {
            "extracted_docs": extracted,
            "confidence": confidence,
            "trace": trace,
            "component_failures": failures,
        }

    return doc_parser_node
