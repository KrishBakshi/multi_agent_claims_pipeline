# Synthetic Invoice 01

Consultation invoice grounded in the sample hospital-bill layout and the active policy roster.

```invoice_spec
{
  "document_id": "01_consultation_apollo_rajesh",
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
    "name": "Apollo Hospitals",
    "address": "154 Residency Road, Bengaluru - 560025",
    "meta_line": "GSTIN: 29APOLLO1234X1ZX | Ph: 080-44112233 | Network Hospital"
  },
  "patient": {
    "member_id": "EMP001",
    "name": "Rajesh Kumar",
    "age": 39,
    "gender_display": "Male",
    "relationship": "SELF"
  },
  "doctor": {
    "name": "Dr. Arun Sharma",
    "registration": "KA/45678/2015",
    "specialization": "Internal Medicine"
  },
  "bill": {
    "title": "BILL / RECEIPT",
    "bill_no": "APH/OPD/2024/04152",
    "date": "2024-11-01"
  },
  "line_items": [
    {"description": "General Physician Consultation (OPD)", "qty": 1, "rate": 1200.0, "amount": 1200.0},
    {"description": "Temperature and Vitals Assessment", "qty": 1, "rate": 250.0, "amount": 250.0},
    {"description": "CBC Sample Collection Charge", "qty": 1, "rate": 300.0, "amount": 300.0}
  ],
  "totals": {
    "subtotal": 1750.0,
    "discount": 0.0,
    "gst": 0.0,
    "total": 1750.0
  },
  "payment": {
    "mode": "UPI",
    "received_by": "K. Nataraj",
    "stamp_text": "[CASHIER STAMP]"
  },
  "notes": "Diagnosis context: Viral Fever. Policy-compliant consultation bill within OPD category limit.",
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
  {"name": "mild_blur", "reason": "soft mobile camera focus loss"},
  {"name": "phone_photo", "reason": "perspective skew plus shadow"},
  {"name": "jpeg_low_quality", "reason": "compressed WhatsApp forward"}
]
```
