# Synthetic Invoice 08

Second consultation-style bill with a different provider and clinical context.

```invoice_spec
{
  "document_id": "08_consultation_sakra_anita",
  "document_type": "HOSPITAL_BILL",
  "claim_category": "CONSULTATION",
  "policy_context": {
    "policy_id": "PLUM_GHI_2024",
    "insurer": "ICICI Lombard General Insurance",
    "company_name": "TechCorp Solutions Pvt Ltd",
    "network_hospital": true,
    "category_sub_limit": 2000,
    "copay_percent": 10,
    "requires_prescription": true
  },
  "provider": {
    "name": "Sakra World Hospital",
    "address": "52 Outer Ring Road, Bengaluru - 560103",
    "meta_line": "GSTIN: 29SAKRA3333X1ZX | Ph: 080-49694969 | Network Hospital"
  },
  "patient": {
    "member_id": "EMP009",
    "name": "Anita Desai",
    "age": 31,
    "gender_display": "Female",
    "relationship": "SELF"
  },
  "doctor": {
    "name": "Dr. Kavya Rao",
    "registration": "TN/56789/2013",
    "specialization": "General Medicine"
  },
  "bill": {
    "title": "OUTPATIENT BILL",
    "bill_no": "SWH/OPD/2024/12048",
    "date": "2024-12-11"
  },
  "line_items": [
    {"description": "Consultation Fee", "qty": 1, "rate": 1000.0, "amount": 1000.0},
    {"description": "Urine Routine Test", "qty": 1, "rate": 350.0, "amount": 350.0},
    {"description": "Administrative and File Charge", "qty": 1, "rate": 150.0, "amount": 150.0}
  ],
  "totals": {
    "subtotal": 1500.0,
    "discount": 0.0,
    "gst": 0.0,
    "total": 1500.0
  },
  "payment": {
    "mode": "Card",
    "received_by": "J. Mary",
    "stamp_text": "[FRONT OFFICE STAMP]"
  },
  "notes": "UTI follow-up consultation within covered outpatient limit.",
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
  {"name": "phone_photo", "reason": "mobile photo with perspective"},
  {"name": "jpeg_low_quality", "reason": "lossy upload"},
  {"name": "noisy_scan", "reason": "scanner noise"}
]
```
