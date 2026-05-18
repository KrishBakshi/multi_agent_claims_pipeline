"""Gemini Vision OCR experiment — single hardcoded document.

Passes data/experiemnts_output_data/clean_pdf/01_consultation_apollo_rajesh.pdf
to Gemini Flash via the Google Generative AI API and returns a JSON object
whose schema matches exactly what DocParserAgent produces and DecisionMakerAgent
consumes from extracted_docs.

Pipeline
--------
  1. PDF first page → PNG at 150 DPI via pymupdf
  2. Letterbox to 640×640 (single Gemini Vision tile → fewer tokens)
  3. Encode as base64 and POST to Gemini with response_mime_type=application/json
  4. Parse and pretty-print the ExtractedDocument JSON

Requires: GOOGLE_API_KEY in environment or .env file.
"""
from __future__ import annotations

import base64
import io
import json
from pathlib import Path

import pymupdf
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai
import os

_LETTERBOX_SIZE = 640

load_dotenv()

# ── Hardcoded input ───────────────────────────────────────────────────────────

DOCUMENT_PATH = (
    Path(__file__).parent.parent
    / "data/experiemnts_output_data/clean_pdf/01_consultation_apollo_rajesh.pdf"
)

MODEL_NAME = "gemini-3.1-flash-lite"

# Schema mirrors the ExtractedDocument dict produced by DocParserAgent
# (_from_glm_ocr / _from_content in src/agents/doc_parser.py) and consumed
# by DecisionMakerAgent via state["extracted_docs"].
EXTRACTION_PROMPT = """\
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

# ── PDF → PNG ─────────────────────────────────────────────────────────────────

def pdf_first_page_to_png(file_data: bytes, dpi: int = 150) -> bytes:
    with pymupdf.open(stream=file_data, filetype="pdf") as doc:
        page = doc.load_page(0)
        pix = page.get_pixmap(dpi=dpi)
        return pix.tobytes("png")


# ── Letterbox ─────────────────────────────────────────────────────────────────

def _letterbox(image_bytes: bytes) -> bytes:
    """Fit image into a _LETTERBOX_SIZE square with white padding.

    Keeps the image within a single Gemini Vision tile, minimising token usage
    while preserving the full document in one shot.
    """
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


# ── PNG → base64 ──────────────────────────────────────────────────────────────

def png_to_base64(png_bytes: bytes) -> str:
    return base64.b64encode(png_bytes).decode("utf-8")


# ── Gemini Vision call ────────────────────────────────────────────────────────

def extract_with_gemini(png_bytes: bytes) -> dict:
    """Send the letterboxed PNG to Gemini and return a parsed ExtractedDocument dict."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError("GOOGLE_API_KEY not set — add it to your .env file.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(MODEL_NAME)

    lb_bytes = _letterbox(png_bytes)
    image_part = {
        "inline_data": {
            "mime_type": "image/png",
            "data": png_to_base64(lb_bytes),
        }
    }

    response = model.generate_content(
        [EXTRACTION_PROMPT, image_part],
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json",
        ),
    )
    return json.loads(response.text)


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    print("=" * 70)
    print("Gemini Vision OCR Experiment")
    print(f"Document : {DOCUMENT_PATH.name}")
    print(f"Model    : {MODEL_NAME}")
    print("=" * 70)

    file_data = DOCUMENT_PATH.read_bytes()

    print("\n[1/3] Converting PDF first page to PNG and letterboxing to 640×640…")
    png_bytes = pdf_first_page_to_png(file_data)
    lb_size = len(_letterbox(png_bytes))
    print(f"      Raw PNG: {len(png_bytes):,} bytes  →  letterboxed: {lb_size:,} bytes")

    print("\n[2/3] Sending to Gemini Vision API (JSON mode)…")
    extracted_doc = extract_with_gemini(png_bytes)

    print("\n[3/3] Extracted document (ExtractedDocument schema):\n")
    print("── extracted_docs[0] ────────────────────────────────────────────────")
    print(json.dumps(extracted_doc, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
