# Synthetic Invoice 02

Diagnostic invoice aligned with the guide's hospital bill structure and diagnostic coverage rules.

```invoice_spec
{
  "document_id": "02_diagnostic_manipal_priya",
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
    "pre_auth_required": false
  },
  "provider": {
    "name": "Manipal Hospitals",
    "address": "98 HAL Airport Road, Bengaluru - 560017",
    "meta_line": "GSTIN: 29MANIPAL5678X1ZX | Ph: 080-25024444 | Network Hospital"
  },
  "patient": {
    "member_id": "EMP002",
    "name": "Priya Singh",
    "age": 34,
    "gender_display": "Female",
    "relationship": "SELF"
  },
  "doctor": {
    "name": "Dr. Meena Pillai",
    "registration": "KA/89012/2018",
    "specialization": "Pathology"
  },
  "bill": {
    "title": "DIAGNOSTIC BILL / RECEIPT",
    "bill_no": "MNH/DIAG/2024/09311",
    "date": "2024-10-14"
  },
  "line_items": [
    {"description": "CBC (Complete Blood Count)", "qty": 1, "rate": 450.0, "amount": 450.0},
    {"description": "Dengue NS1 Antigen Test", "qty": 1, "rate": 850.0, "amount": 850.0},
    {"description": "Doctor Review and Report Dispatch", "qty": 1, "rate": 250.0, "amount": 250.0}
  ],
  "totals": {
    "subtotal": 1550.0,
    "discount": 155.0,
    "gst": 0.0,
    "total": 1395.0
  },
  "payment": {
    "mode": "Card",
    "received_by": "P. Fernandes",
    "stamp_text": "[LAB DESK STAMP]"
  },
  "notes": "Diagnostic claim references covered lab tests below pre-auth threshold.",
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
  {"name": "grayscale_scan", "reason": "office scanner output"},
  {"name": "noisy_scan", "reason": "grain in older scanner"},
  {"name": "phone_photo", "reason": "angled desk capture"}
]
```
