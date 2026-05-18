# Synthetic Invoice 04

Dental bill for a covered procedure under the policy's dental section.

```invoice_spec
{
  "document_id": "04_dental_max_sneha",
  "document_type": "HOSPITAL_BILL",
  "claim_category": "DENTAL",
  "policy_context": {
    "policy_id": "PLUM_GHI_2024",
    "insurer": "ICICI Lombard General Insurance",
    "company_name": "TechCorp Solutions Pvt Ltd",
    "network_hospital": true,
    "category_sub_limit": 10000,
    "copay_percent": 0,
    "covered_procedure": "Scaling and Polishing",
    "requires_dental_report": true
  },
  "provider": {
    "name": "Max Healthcare",
    "address": "31 Richmond Town, Bengaluru - 560025",
    "meta_line": "GSTIN: 29MAXCARE2222X1ZX | Ph: 080-61112222 | Network Dental Unit"
  },
  "patient": {
    "member_id": "EMP004",
    "name": "Sneha Reddy",
    "age": 32,
    "gender_display": "Female",
    "relationship": "SELF"
  },
  "doctor": {
    "name": "Dr. Neha Gupta",
    "registration": "DL/34567/2016",
    "specialization": "Dental Surgery"
  },
  "bill": {
    "title": "DENTAL BILL / RECEIPT",
    "bill_no": "MAX/DEN/2024/05477",
    "date": "2024-08-09"
  },
  "line_items": [
    {"description": "Dental Consultation", "qty": 1, "rate": 500.0, "amount": 500.0},
    {"description": "Scaling and Polishing", "qty": 1, "rate": 1800.0, "amount": 1800.0},
    {"description": "Dental X-Ray (Single View)", "qty": 1, "rate": 450.0, "amount": 450.0}
  ],
  "totals": {
    "subtotal": 2750.0,
    "discount": 0.0,
    "gst": 0.0,
    "total": 2750.0
  },
  "payment": {
    "mode": "UPI",
    "received_by": "M. Shetty",
    "stamp_text": "[DENTAL DESK STAMP]"
  },
  "notes": "Covered dental cleaning workflow using an explicitly allowed procedure.",
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
  {"name": "phone_photo", "reason": "desk-captured dental receipt"},
  {"name": "mild_blur", "reason": "slight focus error"},
  {"name": "jpeg_low_quality", "reason": "messaging app upload"}
]
```
