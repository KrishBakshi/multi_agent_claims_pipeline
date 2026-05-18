# Synthetic Invoice 06

Vision claim invoice using covered items from the policy.

```invoice_spec
{
  "document_id": "06_vision_columbia_kavita",
  "document_type": "HOSPITAL_BILL",
  "claim_category": "VISION",
  "policy_context": {
    "policy_id": "PLUM_GHI_2024",
    "insurer": "ICICI Lombard General Insurance",
    "company_name": "TechCorp Solutions Pvt Ltd",
    "network_hospital": true,
    "category_sub_limit": 5000,
    "copay_percent": 0,
    "requires_prescription": true,
    "covered_items": ["Glasses", "Eye Examination"]
  },
  "provider": {
    "name": "Columbia Asia",
    "address": "24 Hebbal Ring Road, Bengaluru - 560024",
    "meta_line": "GSTIN: 29COLASIA8080X1ZX | Ph: 080-61656666 | Vision Care Unit"
  },
  "patient": {
    "member_id": "EMP006",
    "name": "Kavita Nair",
    "age": 41,
    "gender_display": "Female",
    "relationship": "SELF"
  },
  "doctor": {
    "name": "Dr. Rohan Iyer",
    "registration": "MH/23456/2018",
    "specialization": "Ophthalmology"
  },
  "bill": {
    "title": "VISION CARE BILL",
    "bill_no": "CAH/VIS/2024/06720",
    "date": "2024-09-17"
  },
  "line_items": [
    {"description": "Eye Examination", "qty": 1, "rate": 750.0, "amount": 750.0},
    {"description": "Prescription Glasses Frame", "qty": 1, "rate": 1800.0, "amount": 1800.0},
    {"description": "Single Vision Lenses", "qty": 1, "rate": 1950.0, "amount": 1950.0}
  ],
  "totals": {
    "subtotal": 4500.0,
    "discount": 300.0,
    "gst": 0.0,
    "total": 4200.0
  },
  "payment": {
    "mode": "UPI",
    "received_by": "S. Lobo",
    "stamp_text": "[OPTICAL STAMP]"
  },
  "notes": "Vision bill constrained to covered items and category sub-limit.",
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
  {"name": "mild_blur", "reason": "slight motion blur"},
  {"name": "noisy_scan", "reason": "textured scanner artifact"},
  {"name": "jpeg_low_quality", "reason": "lossy image share"}
]
```
