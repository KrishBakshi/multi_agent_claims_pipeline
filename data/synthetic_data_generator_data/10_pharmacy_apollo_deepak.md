# Synthetic Invoice 10

Second pharmacy bill variant for medicine-oriented OCR testing.

```invoice_spec
{
  "document_id": "10_pharmacy_apollo_deepak",
  "document_type": "PHARMACY_BILL",
  "claim_category": "PHARMACY",
  "policy_context": {
    "policy_id": "PLUM_GHI_2024",
    "insurer": "ICICI Lombard General Insurance",
    "company_name": "TechCorp Solutions Pvt Ltd",
    "network_hospital": true,
    "category_sub_limit": 15000,
    "copay_percent": 0,
    "branded_drug_copay_percent": 30,
    "generic_mandatory": true,
    "requires_prescription": true
  },
  "provider": {
    "name": "Apollo Hospitals",
    "address": "154 Residency Road, Bengaluru - 560025",
    "meta_line": "Drug Lic. No: KA-BLR-55102 | Ph: 080-44112233 | Hospital Pharmacy"
  },
  "patient": {
    "member_id": "EMP010",
    "name": "Deepak Shah",
    "age": 45,
    "gender_display": "Male",
    "relationship": "SELF"
  },
  "doctor": {
    "name": "Dr. Kavya Rao",
    "registration": "TN/56789/2013",
    "specialization": "General Medicine"
  },
  "bill": {
    "title": "PHARMACY CASH MEMO",
    "bill_no": "APH/PH/2025/01590",
    "date": "2025-02-06"
  },
  "line_items": [
    {"description": "Pantoprazole 40 mg Tablets", "qty": 15, "rate": 6.5, "amount": 97.5},
    {"description": "Antacid Suspension 150 ml", "qty": 1, "rate": 135.0, "amount": 135.0},
    {"description": "Domperidone Tablets", "qty": 10, "rate": 5.5, "amount": 55.0},
    {"description": "ORS Sachets", "qty": 5, "rate": 12.5, "amount": 62.5}
  ],
  "totals": {
    "subtotal": 350.0,
    "discount": 20.0,
    "gst": 0.0,
    "total": 330.0
  },
  "payment": {
    "mode": "Cash",
    "received_by": "T. George",
    "stamp_text": "[PHARMACY DESK STAMP]"
  },
  "notes": "Generic-friendly pharmacy bill for GERD symptom treatment.",
  "layout": {
    "canvas": {"width": 1400, "height": 1800, "margin": 60},
    "table": {
      "top_y": 560,
      "row_height": 56,
      "columns": [
        {"key": "description", "label": "MEDICINE", "x": 95},
        {"key": "qty", "label": "QTY", "x": 860},
        {"key": "rate", "label": "MRP", "x": 980},
        {"key": "amount", "label": "AMOUNT", "x": 1140}
      ]
    }
  }
}
```

```distortion_presets
[
  {"name": "jpeg_low_quality", "reason": "compressed image submission"},
  {"name": "grayscale_scan", "reason": "black-and-white office scan"},
  {"name": "phone_photo", "reason": "mobile capture under uneven light"}
]
```
