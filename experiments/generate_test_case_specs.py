"""
generate_test_case_specs.py

Reads data/test_case_missing_artifacts_manifest.json and converts each
artifact entry (which was originally a GPT image-generation prompt) into
an OpenCV-renderable markdown spec file.

Output goes to test_case_artifact_specs/ (sibling of data/).
Each file uses the same fenced-block format as data/synthetic_data_generator_data/
and can be processed by render_document_from_spec.py.

Usage:
    python experiments/generate_test_case_specs.py
    python experiments/generate_test_case_specs.py --manifest <path> --output-dir <dir>
"""
from __future__ import annotations

import argparse
import json
import random
import string
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "data" / "test_case_missing_artifacts_manifest.json"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "data" / "test_case_artifact_specs"

random.seed(42)

# ─── static provider tables ───────────────────────────────────────────────────

_CLINICS = [
    {"name": "City Medical Centre", "address": "12 MG Road, Bengaluru - 560001", "phone": "080-22334455"},
    {"name": "Nirmala Clinic", "address": "45 Indiranagar, Bengaluru - 560038", "phone": "080-25678901"},
    {"name": "Sunrise Hospital OPD", "address": "77 Koramangala, Bengaluru - 560034", "phone": "080-41223344"},
]

_AYUSH_CLINICS = [
    {"name": "Dhanvantari Ayurveda Kendra", "address": "18 Jayanagar 4th Block, Bengaluru - 560041", "phone": "080-26548899"},
]

_LABS = [
    {
        "name": "Apollo Diagnostics",
        "address": "88 Residency Road, Bengaluru - 560025",
        "phone": "080-55667788",
        "license_no": "KA-BLR-LAB-22145",
    },
    {
        "name": "Manipal Labs",
        "address": "14 HAL Airport Road, Bengaluru - 560017",
        "phone": "080-25024455",
        "license_no": "KA-BLR-LAB-33211",
    },
]

_HOSPITALS: dict[str, dict] = {
    "Apollo Hospitals": {
        "address": "154 Residency Road, Bengaluru - 560025",
        "meta_line": "GSTIN: 29APOLLO1234X1ZX | Ph: 080-44112233 | Network Hospital",
    },
    "City Clinic, Bengaluru": {
        "address": "22 Brigade Road, Bengaluru - 560025",
        "meta_line": "GSTIN: 29CITYHOS9999X1ZX | Ph: 080-33445566",
    },
    "Smile Dental Clinic": {
        "address": "5 Cunningham Road, Bengaluru - 560052",
        "meta_line": "GSTIN: 29SMILEDENT33X1ZX | Ph: 080-23456789 | Network Dental Unit",
    },
    "Ayur Wellness Centre": {
        "address": "31 Jayanagar, Bengaluru - 560041",
        "meta_line": "GSTIN: 29AYURWELL5678X1ZX | Ph: 080-26543322",
    },
    "_default": {
        "address": "56 Rajajinagar, Bengaluru - 560010",
        "meta_line": "GSTIN: 29DEFHOSP1111X1ZX | Ph: 080-23456789",
    },
}

_DOCTOR_REGISTRY: dict[str, dict] = {
    "KA/45678/2015": {"name": "Dr. Arun Sharma", "specialization": "Internal Medicine"},
    "GJ/56789/2014": {"name": "Dr. Sunil Mehta", "specialization": "Endocrinology"},
    "AP/67890/2017": {"name": "Dr. Venkat Rao", "specialization": "Orthopedics"},
    "DL/34567/2016": {"name": "Dr. R. Gupta", "specialization": "General Medicine"},
    "TN/56789/2013": {"name": "Dr. S. Iyer", "specialization": "Pulmonology"},
    "AYUR/KL/2345/2019": {"name": "Vaidya T. Krishnan", "specialization": "Ayurveda"},
    "WB/34567/2015": {"name": "Dr. P. Banerjee", "specialization": "Bariatric Medicine"},
}

# Inferred context for artifacts whose seed_fields are empty
_DOC_ID_OVERRIDES: dict[str, dict] = {
    # TC001 — EMP001 = Rajesh Kumar. Both docs are prescriptions (wrong doc type scenario).
    # Both must show Rajesh as patient so member-identity checks pass; type-check catches the missing bill.
    "dr_sharma_prescription": {
        "doctor": {"name": "Dr. Arun Sharma", "registration": "KA/45678/2015", "specialization": "Internal Medicine"},
        "patient_name": "Rajesh Kumar",
        "diagnosis": "Upper Respiratory Infection",
        "medicines": ["Amoxicillin 500mg", "Cetirizine 10mg", "Paracetamol 500mg"],
    },
    "another_prescription": {
        "doctor": {"name": "Dr. M. Krishnan", "registration": "KA/78901/2020", "specialization": "General Physician"},
        "patient_name": "Rajesh Kumar",
        "diagnosis": "Hypertension Follow-up",
        "medicines": ["Amlodipine 5mg", "Telmisartan 40mg"],
    },
    # TC002 — EMP004 = Sneha Reddy. Prescription is GOOD; pharmacy bill is UNREADABLE.
    "prescription": {
        "doctor": {"name": "Dr. R. Nair", "registration": "KA/34521/2017", "specialization": "General Physician"},
        "patient_name": "Sneha Reddy",
        "diagnosis": "Migraine",
        "medicines": ["Sumatriptan 50mg", "Domperidone 10mg"],
    },
    "blurry_bill": {
        "patient_name": "Sneha Reddy",
        "medicines_desc": [
            {"description": "Sumatriptan 50mg Tablets x 4", "qty": 4, "rate": 38.0, "amount": 152.0},
            {"description": "Domperidone 10mg Tablets x 10", "qty": 10, "rate": 5.5, "amount": 55.0},
            {"description": "Multivitamin Syrup 100ml", "qty": 1, "rate": 95.0, "amount": 95.0},
        ],
        "total": 302.0,
    },
}

# ─── helpers ──────────────────────────────────────────────────────────────────


def _bill_no(prefix: str) -> str:
    suffix = "".join(random.choices(string.digits, k=5))
    return f"{prefix}/2024/{suffix}"


def _resolve_doctor(seed: dict, doc_id: str | None = None) -> dict:
    override = _DOC_ID_OVERRIDES.get(doc_id or "", {})
    if "doctor" in override:
        return override["doctor"]
    name = seed.get("doctor_name", "")
    reg = seed.get("doctor_registration", "")
    if reg in _DOCTOR_REGISTRY:
        d = _DOCTOR_REGISTRY[reg]
        return {"name": name or d["name"], "registration": reg, "specialization": d["specialization"]}
    if name:
        return {"name": name, "registration": reg or "KA/99999/2020", "specialization": "General Physician"}
    return {"name": "Dr. A. Mehta", "registration": "KA/12345/2018", "specialization": "General Physician"}


def _resolve_hospital(hospital_name: str) -> dict:
    h = _HOSPITALS.get(hospital_name) or _HOSPITALS["_default"]
    return {"name": hospital_name or "City Hospital", "address": h["address"], "meta_line": h["meta_line"]}


def _claim_category(artifact: dict) -> str:
    case = artifact["case_name"].lower()
    seed_str = json.dumps(artifact.get("seed_fields", {})).lower()
    if "dental" in case or "dental" in seed_str:
        return "DENTAL"
    if "mri" in seed_str or "diagnostic" in case or "radiology" in seed_str:
        return "DIAGNOSTIC"
    if "ayurveda" in case or "ayush" in case or "panchakarma" in seed_str:
        return "AYUSH"
    return "CONSULTATION"


def _distortion_presets(quality: str, template_id: str) -> list[dict]:
    if quality == "UNREADABLE" or template_id == "pharmacy_bill_unreadable":
        return [
            {"name": "strong_blur", "reason": "severe defocus - medically unreadable"},
            {"name": "jpeg_low_quality", "reason": "heavily compressed bad capture"},
        ]
    return [
        {"name": "mild_blur", "reason": "soft camera focus"},
        {"name": "grayscale_scan", "reason": "claim desk scan"},
        {"name": "phone_photo", "reason": "mobile capture"},
    ]


def _normalize_line_items(raw: list[dict]) -> list[dict]:
    out = []
    for item in raw:
        amt = float(item.get("amount", item.get("rate", 0)))
        out.append(
            {
                "description": item["description"],
                "qty": item.get("qty", 1),
                "rate": float(item.get("rate", amt)),
                "amount": amt,
            }
        )
    return out


# ─── spec builders ────────────────────────────────────────────────────────────


def _make_prescription_spec(artifact: dict) -> dict:
    seed = artifact.get("seed_fields", {})
    doc_id = Path(artifact["target_path"]).stem
    override = _DOC_ID_OVERRIDES.get(doc_id, {})

    doctor = _resolve_doctor(seed, doc_id)
    is_ayush = (
        "ayush" in " ".join(artifact.get("special_constraints", [])).lower()
        or "ayurveda" in artifact["case_name"].lower()
        or "vaidya" in doctor["name"].lower()
    )
    clinic = _AYUSH_CLINICS[0] if is_ayush else _CLINICS[0]

    patient_name = seed.get("patient_name") or override.get("patient_name", "Ravi Sharma")
    diagnosis = seed.get("diagnosis") or override.get("diagnosis", "Acute Viral Infection")
    medicines = seed.get("medicines") or override.get("medicines", ["Paracetamol 500mg", "Cetirizine 10mg"])
    tests_ordered = seed.get("tests_ordered") or []
    treatment = seed.get("treatment") or None

    spec: dict = {
        "document_id": doc_id,
        "document_type": "PRESCRIPTION",
        "quality": artifact.get("quality", "GOOD"),
        "clinic": clinic,
        "doctor": doctor,
        "patient": {"name": patient_name, "age": 36, "gender_display": "Male"},
        "date": seed.get("date", "2024-11-15"),
        "diagnosis": diagnosis,
        "medicines": medicines,
        "tests_ordered": tests_ordered,
        "layout": {"canvas": {"width": 1400, "height": 1800, "margin": 60}},
    }
    if treatment:
        spec["treatment"] = treatment
    return spec


def _make_hospital_bill_spec(artifact: dict) -> dict:
    seed = artifact.get("seed_fields", {})
    doc_id = Path(artifact["target_path"]).stem

    hospital_name = seed.get("hospital_name", "")
    provider = _resolve_hospital(hospital_name)
    patient_name = seed.get("patient_name", "Ravi Sharma")
    date = seed.get("date", "2024-11-15")

    raw_items: list[dict] = seed.get("line_items") or [
        {"description": "Consultation Fee", "amount": float(seed.get("total", 1000))}
    ]
    line_items = _normalize_line_items(raw_items)
    total = float(seed.get("total") or sum(i["amount"] for i in line_items))
    subtotal = sum(i["amount"] for i in line_items)
    discount = round(subtotal - total, 2) if subtotal > total else 0.0

    category = _claim_category(artifact)
    _bill_titles = {
        "DENTAL": ("DENTAL BILL / RECEIPT", "DEN/BLL"),
        "DIAGNOSTIC": ("DIAGNOSTIC BILL / RECEIPT", "DIAG/BLL"),
        "AYUSH": ("AYUSH BILL / RECEIPT", "AYU/BLL"),
        "CONSULTATION": ("BILL / RECEIPT", "CONS/BLL"),
    }
    bill_title, bill_pfx = _bill_titles[category]
    doctor = _resolve_doctor(seed, doc_id)

    return {
        "document_id": doc_id,
        "document_type": "HOSPITAL_BILL",
        "claim_category": category,
        "quality": artifact.get("quality", "GOOD"),
        "policy_context": {"policy_id": "PLUM_GHI_2024"},
        "provider": provider,
        "patient": {"member_id": "EMP", "name": patient_name, "age": 35, "gender_display": "Male", "relationship": "SELF"},
        "doctor": doctor,
        "bill": {"title": bill_title, "bill_no": _bill_no(bill_pfx), "date": date},
        "line_items": line_items,
        "totals": {"subtotal": subtotal, "discount": discount, "gst": 0.0, "total": total},
        "payment": {"mode": "UPI", "received_by": "Cashier", "stamp_text": "[CASHIER STAMP]"},
        "notes": artifact["case_name"],
        "layout": {
            "canvas": {"width": 1400, "height": 1800, "margin": 60},
            "table": {
                "top_y": 560,
                "row_height": 56,
                "columns": [
                    {"key": "description", "label": "DESCRIPTION", "x": 95},
                    {"key": "qty", "label": "QTY", "x": 860},
                    {"key": "rate", "label": "RATE", "x": 980},
                    {"key": "amount", "label": "AMOUNT", "x": 1140},
                ],
            },
        },
    }


def _make_pharmacy_bill_spec(artifact: dict) -> dict:
    seed = artifact.get("seed_fields", {})
    doc_id = Path(artifact["target_path"]).stem
    override = _DOC_ID_OVERRIDES.get(doc_id, {})

    raw_items: list[dict] = seed.get("line_items") or override.get(
        "medicines_desc",
        [{"description": "Medicines", "qty": 1, "rate": 500.0, "amount": 500.0}],
    )
    line_items = _normalize_line_items(raw_items)
    total = float(seed.get("total") or override.get("total") or sum(i["amount"] for i in line_items))
    subtotal = sum(i["amount"] for i in line_items)
    discount = round(subtotal - total, 2) if subtotal > total else 0.0
    patient_name = seed.get("patient_name") or override.get("patient_name", "Ravi Sharma")

    return {
        "document_id": doc_id,
        "document_type": "PHARMACY_BILL",
        "claim_category": "PHARMACY",
        "quality": artifact.get("quality", "GOOD"),
        "policy_context": {"policy_id": "PLUM_GHI_2024"},
        "provider": {
            "name": "MedCare Pharmacy",
            "address": "7 Commercial Street, Bengaluru - 560001",
            "meta_line": "Drug Lic. No: KA-BLR-PH-12345 | Ph: 080-12341234 | Network Pharmacy",
        },
        "patient": {"member_id": "EMP", "name": patient_name, "age": 35, "gender_display": "Male", "relationship": "SELF"},
        "doctor": _resolve_doctor(seed, doc_id),
        "bill": {"title": "PHARMACY BILL", "bill_no": _bill_no("PH/BLL"), "date": seed.get("date", "2024-11-15")},
        "line_items": line_items,
        "totals": {"subtotal": subtotal, "discount": discount, "gst": 0.0, "total": total},
        "payment": {"mode": "Cash", "received_by": "Pharmacist", "stamp_text": "[PHARMACIST STAMP]"},
        "notes": artifact["case_name"],
        "layout": {
            "canvas": {"width": 1400, "height": 1800, "margin": 60},
            "table": {
                "top_y": 560,
                "row_height": 56,
                "columns": [
                    {"key": "description", "label": "MEDICINE", "x": 95},
                    {"key": "qty", "label": "QTY", "x": 860},
                    {"key": "rate", "label": "MRP", "x": 980},
                    {"key": "amount", "label": "AMOUNT", "x": 1140},
                ],
            },
        },
    }


def _make_lab_report_spec(artifact: dict) -> dict:
    seed = artifact.get("seed_fields", {})
    doc_id = Path(artifact["target_path"]).stem
    lab = _LABS[0]
    test_name = seed.get("test_name", "Blood Panel")

    return {
        "document_id": doc_id,
        "document_type": "LAB_REPORT",
        "quality": artifact.get("quality", "GOOD"),
        "lab": lab,
        "patient": {
            "name": seed.get("patient_name", "Ravi Sharma"),
            "age": 35,
            "gender_display": "Male",
            "ref_doctor": seed.get("doctor_name", "Dr. Venkat Rao"),
        },
        "date": seed.get("date", "2024-11-20"),
        "test_name": test_name,
        "report_no": _bill_no("LAB/RPT"),
        "findings": (
            f"{test_name} study performed and analysed. "
            "Report reviewed by the reporting doctor and dispatched to the referring physician."
        ),
        "layout": {"canvas": {"width": 1400, "height": 1800, "margin": 60}},
    }


# ─── dispatch ─────────────────────────────────────────────────────────────────


def _build_spec(artifact: dict) -> tuple[str, dict]:
    """Return (fenced_block_label, spec_dict)."""
    actual_type = artifact["actual_type"]
    if actual_type == "PRESCRIPTION":
        return "prescription_spec", _make_prescription_spec(artifact)
    if actual_type == "LAB_REPORT":
        return "lab_report_spec", _make_lab_report_spec(artifact)
    if actual_type == "PHARMACY_BILL":
        return "invoice_spec", _make_pharmacy_bill_spec(artifact)
    if actual_type == "HOSPITAL_BILL":
        return "invoice_spec", _make_hospital_bill_spec(artifact)
    raise ValueError(f"Unknown actual_type: {actual_type!r}")


def _render_markdown(artifact: dict) -> str:
    block_label, spec = _build_spec(artifact)
    presets = _distortion_presets(artifact.get("quality", "GOOD"), artifact["prompt_template_id"])

    doc_id = spec["document_id"]
    case_id = artifact["case_id"]
    case_name = artifact["case_name"]
    actual_type = artifact["actual_type"]

    constraints = artifact.get("special_constraints", [])
    constraints_lines = ""
    if constraints:
        constraints_lines = "\nSpecial constraints:\n" + "\n".join(f"- {c}" for c in constraints) + "\n"

    spec_json = json.dumps(spec, indent=2)
    presets_json = json.dumps(presets, indent=2)

    # Template must be at column 0 so the fenced-block markers are not indented.
    # dedent() cannot be used here because spec_json already has its own mixed indentation.
    parts = [
        f"# {actual_type} – {case_id}: {case_name}",
        "",
        f"Generated spec for `{doc_id}` from `test_case_missing_artifacts_manifest.json`.",
        f"Template: `{artifact['prompt_template_id']}`  Quality: `{artifact.get('quality', 'GOOD')}`",
        constraints_lines,
        f"```{block_label}",
        spec_json,
        "```",
        "",
        "```distortion_presets",
        presets_json,
        "```",
        "",
    ]
    return "\n".join(parts)


# ─── main ─────────────────────────────────────────────────────────────────────


def generate(manifest_path: Path, output_dir: Path) -> None:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    output_dir.mkdir(parents=True, exist_ok=True)

    for artifact in manifest["artifacts"]:
        doc_id = Path(artifact["target_path"]).stem
        content = _render_markdown(artifact)
        out_path = output_dir / f"{doc_id}.md"
        out_path.write_text(content, encoding="utf-8")
        print(f"  {out_path.relative_to(REPO_ROOT)}")

    print(f"\n{len(manifest['artifacts'])} spec files written to {output_dir.relative_to(REPO_ROOT)}/")


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Convert manifest + prompt templates into OpenCV spec markdown files.")
    p.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    p.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return p


def main() -> None:
    args = _build_parser().parse_args()
    generate(args.manifest, args.output_dir)


if __name__ == "__main__":
    main()
