# Synthetic Invoice 05

Dental root canal invoice within covered dental procedures and within claim limits.

```invoice_spec
{
  "document_id": "05_dental_narayana_vikram",
  "document_type": "HOSPITAL_BILL",
  "claim_category": "DENTAL",
  "policy_context": {
    "policy_id": "PLUM_GHI_2024",
    "insurer": "ICICI Lombard General Insurance",
    "company_name": "TechCorp Solutions Pvt Ltd",
    "network_hospital": true,
    "category_sub_limit": 10000,
    "copay_percent": 0,
    "covered_procedure": "Root Canal Treatment",
    "requires_dental_report": true
  },
  "provider": {
    "name": "Narayana Health",
    "address": "258 Hosur Road, Bengaluru - 560099",
    "meta_line": "GSTIN: 29NARAYANA9101X1ZX | Ph: 080-71222222 | Network Dental Unit"
  },
  "patient": {
    "member_id": "EMP005",
    "name": "Vikram Joshi",
    "age": 45,
    "gender_display": "Male",
    "relationship": "SELF"
  },
  "doctor": {
    "name": "Dr. Neha Gupta",
    "registration": "DL/34567/2016",
    "specialization": "Dental Surgery"
  },
  "bill": {
    "title": "DENTAL PROCEDURE BILL",
    "bill_no": "NH/DEN/2024/09110",
    "date": "2024-11-22"
  },
  "line_items": [
    {"description": "Dental Consultation", "qty": 1, "rate": 600.0, "amount": 600.0},
    {"description": "Root Canal Treatment", "qty": 1, "rate": 3600.0, "amount": 3600.0},
    {"description": "Temporary Crown Placement", "qty": 1, "rate": 700.0, "amount": 700.0}
  ],
  "totals": {
    "subtotal": 4900.0,
    "discount": 0.0,
    "gst": 0.0,
    "total": 4900.0
  },
  "payment": {
    "mode": "Card",
    "received_by": "A. Prakash",
    "stamp_text": "[BILLING SEAL]"
  },
  "notes": "All line items remain within the policy per-claim limit and use a covered dental procedure.",
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
  {"name": "grayscale_scan", "reason": "flatbed scan"},
  {"name": "phone_photo", "reason": "perspective warped mobile capture"},
  {"name": "strong_blur", "reason": "out-of-focus evidence photo"}
]
```
