# Synthetic Invoice 09

Diagnostic invoice for a chronic-condition follow-up after the waiting period.

```invoice_spec
{
  "document_id": "09_diagnostic_medanta_ravi",
  "document_type": "HOSPITAL_BILL",
  "claim_category": "DIAGNOSTIC",
  "policy_context": {
    "policy_id": "PLUM_GHI_2024",
    "insurer": "ICICI Lombard General Insurance",
    "company_name": "TechCorp Solutions Pvt Ltd",
    "network_hospital": true,
    "category_sub_limit": 10000,
    "copay_percent": 0,
    "requires_prescription": true,
    "pre_existing_waiting_days_reference": 90
  },
  "provider": {
    "name": "Medanta",
    "address": "12 Residency Extension, Bengaluru - 560071",
    "meta_line": "GSTIN: 29MEDANTA4444X1ZX | Ph: 080-68002222 | Diagnostic Services"
  },
  "patient": {
    "member_id": "EMP008",
    "name": "Ravi Menon",
    "age": 37,
    "gender_display": "Male",
    "relationship": "SELF"
  },
  "doctor": {
    "name": "Dr. Rohan Iyer",
    "registration": "MH/23456/2018",
    "specialization": "Internal Medicine"
  },
  "bill": {
    "title": "DIAGNOSTIC SERVICES BILL",
    "bill_no": "MED/DIAG/2025/01081",
    "date": "2025-01-18"
  },
  "line_items": [
    {"description": "HbA1c Test", "qty": 1, "rate": 900.0, "amount": 900.0},
    {"description": "Fasting Blood Sugar", "qty": 1, "rate": 180.0, "amount": 180.0},
    {"description": "Lipid Profile", "qty": 1, "rate": 1100.0, "amount": 1100.0}
  ],
  "totals": {
    "subtotal": 2180.0,
    "discount": 180.0,
    "gst": 0.0,
    "total": 2000.0
  },
  "payment": {
    "mode": "UPI",
    "received_by": "C. Bose",
    "stamp_text": "[LAB BILLING STAMP]"
  },
  "notes": "Diagnostic follow-up dated well after the 90-day specific-condition waiting period.",
  "layout": {
    "canvas": {"width": 1400, "height": 1800, "margin": 60},
    "table": {
      "top_y": 560,
      "row_height": 56,
      "columns": [
        {"key": "description", "label": "DESCRIPTION", "x": 95},
        {"key": "qty", "label": "QTY", "x": 860},
        {"key": "rate", "label": "RATE", "x": 980},
        {"key": "amount", "label": "AMOUNT", "x": 1140}
      ]
    }
  }
}
```

```distortion_presets
[
  {"name": "grayscale_scan", "reason": "PDF print and rescan"},
  {"name": "mild_blur", "reason": "minor blur in recapture"},
  {"name": "phone_photo", "reason": "angled photo with shadow"}
]
```
