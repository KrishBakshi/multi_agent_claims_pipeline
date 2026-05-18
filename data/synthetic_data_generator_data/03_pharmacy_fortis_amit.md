# Synthetic Invoice 03

Pharmacy bill using covered medicines and the pharmacy layout from the guide.

```invoice_spec
{
  "document_id": "03_pharmacy_fortis_amit",
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
    "name": "Fortis Healthcare",
    "address": "77 Bannerghatta Main Road, Bengaluru - 560076",
    "meta_line": "Drug Lic. No: KA-BLR-48291 | Ph: 080-66214444 | Network Pharmacy Desk"
  },
  "patient": {
    "member_id": "EMP003",
    "name": "Amit Verma",
    "age": 35,
    "gender_display": "Male",
    "relationship": "SELF"
  },
  "doctor": {
    "name": "Dr. Arun Sharma",
    "registration": "KA/45678/2015",
    "specialization": "Internal Medicine"
  },
  "bill": {
    "title": "PHARMACY BILL",
    "bill_no": "FOR/PH/2024/11803",
    "date": "2024-12-03"
  },
  "line_items": [
    {"description": "Azithromycin 500 mg Tablets", "qty": 3, "rate": 62.0, "amount": 186.0},
    {"description": "Levocetirizine Tablets", "qty": 10, "rate": 4.5, "amount": 45.0},
    {"description": "Pantoprazole 40 mg Tablets", "qty": 10, "rate": 6.5, "amount": 65.0},
    {"description": "Cough Syrup 100 ml", "qty": 1, "rate": 118.0, "amount": 118.0}
  ],
  "totals": {
    "subtotal": 414.0,
    "discount": 14.0,
    "gst": 0.0,
    "total": 400.0
  },
  "payment": {
    "mode": "Cash",
    "received_by": "R. D'Souza",
    "stamp_text": "[PHARMACIST STAMP]"
  },
  "notes": "Generic-focused pharmacy bill for acute bronchitis symptom management.",
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
  {"name": "mild_blur", "reason": "receipt photographed in hand"},
  {"name": "jpeg_low_quality", "reason": "compressed upload"},
  {"name": "grayscale_scan", "reason": "claim desk scan"}
]
```
