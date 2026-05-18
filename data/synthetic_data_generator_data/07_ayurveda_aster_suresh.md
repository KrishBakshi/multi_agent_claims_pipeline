# Synthetic Invoice 07

Alternative medicine bill using a covered system and a registered-practitioner context.

```invoice_spec
{
  "document_id": "07_ayurveda_aster_suresh",
  "document_type": "HOSPITAL_BILL",
  "claim_category": "ALTERNATIVE_MEDICINE",
  "policy_context": {
    "policy_id": "PLUM_GHI_2024",
    "insurer": "ICICI Lombard General Insurance",
    "company_name": "TechCorp Solutions Pvt Ltd",
    "network_hospital": true,
    "category_sub_limit": 8000,
    "copay_percent": 0,
    "covered_system": "Ayurveda",
    "requires_prescription": true,
    "requires_registered_practitioner": true
  },
  "provider": {
    "name": "Aster CMI Hospital",
    "address": "43 New Airport Road, Bengaluru - 560092",
    "meta_line": "GSTIN: 29ASTER1111X1ZX | Ph: 080-43420100 | Ayurveda OPD"
  },
  "patient": {
    "member_id": "EMP007",
    "name": "Suresh Patil",
    "age": 48,
    "gender_display": "Male",
    "relationship": "SELF"
  },
  "doctor": {
    "name": "Dr. Anjali Menon",
    "registration": "AYUR/KL/2345/2019",
    "specialization": "Ayurveda"
  },
  "bill": {
    "title": "AYURVEDA OPD BILL",
    "bill_no": "ASTER/AY/2024/02814",
    "date": "2024-07-12"
  },
  "line_items": [
    {"description": "Ayurveda Physician Consultation", "qty": 1, "rate": 900.0, "amount": 900.0},
    {"description": "Abhyanga Therapy Session", "qty": 1, "rate": 1500.0, "amount": 1500.0},
    {"description": "Prescribed Kashayam Pack", "qty": 1, "rate": 650.0, "amount": 650.0}
  ],
  "totals": {
    "subtotal": 3050.0,
    "discount": 150.0,
    "gst": 0.0,
    "total": 2900.0
  },
  "payment": {
    "mode": "Cash",
    "received_by": "L. Haridas",
    "stamp_text": "[AYURVEDA BILLING STAMP]"
  },
  "notes": "Covered alternative medicine example using a registered Ayurveda practitioner.",
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
  {"name": "phone_photo", "reason": "captured under room light"},
  {"name": "grayscale_scan", "reason": "low-end scanner"},
  {"name": "mild_blur", "reason": "slight camera softness"}
]
```
