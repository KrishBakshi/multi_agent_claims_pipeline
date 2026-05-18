"""
render_document_from_spec.py

Extended renderer that handles all document types produced by generate_test_case_specs.py:
  - invoice_spec     → HOSPITAL_BILL / PHARMACY_BILL  (delegates to render_invoice_from_markdown)
  - prescription_spec → PRESCRIPTION
  - lab_report_spec  → LAB_REPORT

Usage:
    python experiments/render_document_from_spec.py --input-file <spec.md> --output-dir <dir>
    python experiments/render_document_from_spec.py --input-dir <specs_dir> --output-dir <dir>

Run from repo root so that sibling experiment imports resolve correctly, or add
the experiments/ directory to PYTHONPATH.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import cv2
import numpy as np

# Allow running from repo root: add experiments/ to path so the existing
# render_invoice_from_markdown module can be imported.
_EXPERIMENTS = Path(__file__).resolve().parent
if str(_EXPERIMENTS) not in sys.path:
    sys.path.insert(0, str(_EXPERIMENTS))

from render_invoice_from_markdown import render_invoice  # noqa: E402

_BLOCK_PATTERN = r"```{label}\n(.*?)\n```"
_KNOWN_BLOCKS = ["invoice_spec", "prescription_spec", "lab_report_spec"]


# ─── shared drawing helper ────────────────────────────────────────────────────


def _put(
    img: np.ndarray,
    text: str,
    x: int,
    y: int,
    scale: float = 0.75,
    thickness: int = 1,
) -> None:
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, scale, (0, 0, 0), thickness, cv2.LINE_AA)


def _hline(img: np.ndarray, y: int, x0: int, x1: int, color: tuple[int, int, int] = (0, 0, 0), t: int = 1) -> None:
    cv2.line(img, (x0, y), (x1, y), color, t)


# ─── prescription renderer ────────────────────────────────────────────────────


def render_prescription(spec: dict) -> np.ndarray:
    canvas = spec.get("layout", {}).get("canvas", {"width": 1400, "height": 1800, "margin": 60})
    w, h, m = canvas["width"], canvas["height"], canvas["margin"]
    img = np.full((h, w, 3), 255, dtype=np.uint8)
    cv2.rectangle(img, (m, m), (w - m, h - m), (0, 0, 0), 2)

    clinic = spec.get("clinic", {})
    doctor = spec.get("doctor", {})
    patient = spec.get("patient", {})

    # ── Doctor / clinic header ─────────────────────────────────────────────
    _put(img, doctor.get("name", "").upper(), m + 20, m + 52, scale=1.0, thickness=2)
    _put(img, f"{doctor.get('specialization', '')}  |  Reg. No: {doctor.get('registration', '')}", m + 20, m + 92, scale=0.65)
    _put(img, clinic.get("name", ""), m + 20, m + 128, scale=0.65)
    _put(img, clinic.get("address", ""), m + 20, m + 162, scale=0.60)
    _put(img, f"Ph: {clinic.get('phone', '')}", m + 20, m + 194, scale=0.60)
    _hline(img, m + 215, m, w - m)

    # ── Patient block ──────────────────────────────────────────────────────
    y = m + 258
    _put(img, f"Patient: {patient.get('name', '')}", m + 20, y, scale=0.72)
    _put(img, f"Date: {spec.get('date', '')}", w - 400, y, scale=0.70)
    y += 42
    _put(img, f"Age: {patient.get('age', '')} yrs   Gender: {patient.get('gender_display', '')}", m + 20, y, scale=0.65)
    _hline(img, y + 28, m, w - m)

    # ── Diagnosis ─────────────────────────────────────────────────────────
    y += 75
    _put(img, "Diagnosis:", m + 20, y, scale=0.72, thickness=2)
    y += 42
    _put(img, spec.get("diagnosis", ""), m + 40, y, scale=0.68)
    y += 50
    _hline(img, y, m, w - m, color=(220, 220, 220))

    # ── Rx ────────────────────────────────────────────────────────────────
    y += 40
    _put(img, "Rx", m + 20, y, scale=0.90, thickness=2)
    y += 44
    medicines = spec.get("medicines") or []
    treatment = spec.get("treatment")
    if medicines:
        for i, med in enumerate(medicines, 1):
            _put(img, f"{i}. {med}", m + 48, y, scale=0.66)
            y += 42
    elif treatment:
        _put(img, str(treatment), m + 48, y, scale=0.66)
        y += 42
    else:
        _put(img, "—", m + 48, y, scale=0.66)
        y += 42

    # ── Investigations ────────────────────────────────────────────────────
    tests = spec.get("tests_ordered") or []
    if tests:
        y += 18
        _hline(img, y, m, w - m, color=(220, 220, 220))
        y += 38
        _put(img, "Investigations:", m + 20, y, scale=0.68, thickness=2)
        y += 40
        for t in tests:
            _put(img, f"  • {t}", m + 44, y, scale=0.63)
            y += 38

    # ── Signature / stamp ─────────────────────────────────────────────────
    foot = h - m - 145
    _hline(img, foot, m, w - m)
    _put(img, "Follow-up: As clinically required", m + 20, foot + 32, scale=0.60)
    _put(img, "[Doctor's Signature]", w - 420, foot + 32, scale=0.65)
    _put(img, "[Registration Stamp]", w - 420, foot + 72, scale=0.65)

    return img


# ─── lab report renderer ──────────────────────────────────────────────────────


def render_lab_report(spec: dict) -> np.ndarray:
    canvas = spec.get("layout", {}).get("canvas", {"width": 1400, "height": 1800, "margin": 60})
    w, h, m = canvas["width"], canvas["height"], canvas["margin"]
    img = np.full((h, w, 3), 255, dtype=np.uint8)
    cv2.rectangle(img, (m, m), (w - m, h - m), (0, 0, 0), 2)

    lab = spec.get("lab", {})
    patient = spec.get("patient", {})

    # ── Lab header ────────────────────────────────────────────────────────
    _put(img, lab.get("name", "").upper(), m + 20, m + 52, scale=1.0, thickness=2)
    _put(img, f"Lic. No: {lab.get('license_no', '')}", m + 20, m + 90, scale=0.65)
    _put(img, lab.get("address", ""), m + 20, m + 126, scale=0.62)
    _put(img, f"Ph: {lab.get('phone', '')}", m + 20, m + 160, scale=0.60)
    _hline(img, m + 182, m, w - m, t=2)

    # ── Report title ──────────────────────────────────────────────────────
    _put(img, "DIAGNOSTIC / RADIOLOGY REPORT", m + 20, m + 232, scale=0.85, thickness=2)
    _put(img, f"Report No: {spec.get('report_no', '')}", m + 20, m + 272, scale=0.68)
    _put(img, f"Date: {spec.get('date', '')}", w - 380, m + 272, scale=0.68)
    _hline(img, m + 298, m, w - m)

    # ── Patient block ─────────────────────────────────────────────────────
    y = m + 342
    _put(img, f"Patient: {patient.get('name', '')}", m + 20, y, scale=0.72)
    _put(img, f"Ref. Doctor: {patient.get('ref_doctor', '')}", w - 520, y, scale=0.65)
    y += 42
    _put(img, f"Age / Gender: {patient.get('age', '')} / {patient.get('gender_display', '')}", m + 20, y, scale=0.65)
    _hline(img, y + 30, m, w - m)

    # ── Test / study name ─────────────────────────────────────────────────
    y += 78
    _put(img, "Test / Study:", m + 20, y, scale=0.72, thickness=2)
    y += 48
    _put(img, spec.get("test_name", ""), m + 40, y, scale=0.78, thickness=2)
    y += 62
    _hline(img, y, m, w - m, color=(220, 220, 220))

    # ── Findings ──────────────────────────────────────────────────────────
    y += 42
    _put(img, "Findings / Report:", m + 20, y, scale=0.70, thickness=2)
    y += 44
    findings = spec.get("findings", "")
    words = findings.split()
    line_buf: list[str] = []
    wrapped: list[str] = []
    for word in words:
        candidate = " ".join(line_buf + [word])
        if len(candidate) > 82:
            wrapped.append(" ".join(line_buf))
            line_buf = [word]
        else:
            line_buf.append(word)
    if line_buf:
        wrapped.append(" ".join(line_buf))
    for ln in wrapped:
        _put(img, ln, m + 40, y, scale=0.63)
        y += 38

    # ── Footer ────────────────────────────────────────────────────────────
    foot = h - m - 145
    _hline(img, foot, m, w - m)
    _put(img, "[Reporting Pathologist / Radiologist]", m + 20, foot + 36, scale=0.65)
    _put(img, "[Signature & Stamp]", w - 400, foot + 36, scale=0.65)

    return img


# ─── block extraction ─────────────────────────────────────────────────────────


def _extract_spec(text: str) -> tuple[str, dict]:
    """Return (block_label, spec_dict) for the first recognised spec block."""
    for label in _KNOWN_BLOCKS:
        pattern = _BLOCK_PATTERN.format(label=re.escape(label))
        m = re.search(pattern, text, re.DOTALL)
        if m:
            return label, json.loads(m.group(1))
    raise ValueError(f"No recognised spec block found. Expected one of: {_KNOWN_BLOCKS}")


# ─── public API ───────────────────────────────────────────────────────────────


def render_from_markdown(markdown_path: Path, output_dir: Path) -> Path:
    text = markdown_path.read_text(encoding="utf-8")
    block_label, spec = _extract_spec(text)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{spec['document_id']}.png"

    if block_label == "invoice_spec":
        image = render_invoice(spec)
    elif block_label == "prescription_spec":
        image = render_prescription(spec)
    elif block_label == "lab_report_spec":
        image = render_lab_report(spec)
    else:
        raise ValueError(f"Unhandled block label: {block_label!r}")

    cv2.imwrite(str(output_path), image)
    return output_path


# ─── CLI ─────────────────────────────────────────────────────────────────────


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Render PRESCRIPTION, LAB_REPORT, HOSPITAL_BILL, and PHARMACY_BILL specs to PNG."
    )
    p.add_argument("--input-file", type=Path, help="Single markdown spec file.")
    p.add_argument("--input-dir", type=Path, help="Directory of markdown spec files.")
    p.add_argument("--output-dir", type=Path, required=True, help="Output directory for PNG files.")
    return p


def main() -> None:
    args = _build_parser().parse_args()
    if not args.input_file and not args.input_dir:
        _build_parser().error("Provide --input-file or --input-dir")

    files: list[Path] = []
    if args.input_file:
        files.append(args.input_file)
    if args.input_dir:
        files.extend(sorted(args.input_dir.glob("*.md")))

    for md_path in files:
        try:
            out = render_from_markdown(md_path, args.output_dir)
            print(f"  Rendered {md_path.name}  ->  {out.name}")
        except Exception as exc:
            print(f"  ERROR {md_path.name}: {exc}")


if __name__ == "__main__":
    main()
