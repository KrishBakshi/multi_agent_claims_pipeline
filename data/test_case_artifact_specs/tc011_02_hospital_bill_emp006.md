# HOSPITAL_BILL – TC011: Component Failure - Graceful Degradation

Generated spec for `tc011_02_hospital_bill_emp006` from `test_case_missing_artifacts_manifest.json`.
Template: `hospital_bill_clean`  Quality: `GOOD`

```invoice_spec
{
  "document_id": "tc011_02_hospital_bill_emp006",
  "document_type": "HOSPITAL_BILL",
  "claim_category": "AYUSH",
  "quality": "GOOD",
  "policy_context": {
    "policy_id": "PLUM_GHI_2024"
  },
  "provider": {
    "name": "Ayur Wellness Centre",
    "address": "31 Jayanagar, Bengaluru - 560041",
    "meta_line": "GSTIN: 29AYURWELL5678X1ZX | Ph: 080-26543322"
  },
  "patient": {
    "member_id": "EMP",
    "name": "Ravi Sharma",
    "age": 35,
    "gender_display": "Male",
    "relationship": "SELF"
  },
  "doctor": {
    "name": "Dr. A. Mehta",
    "registration": "KA/12345/2018",
    "specialization": "General Physician"
  },
  "bill": {
    "title": "AYUSH BILL / RECEIPT",
    "bill_no": "AYU/BLL/2024/32296",
    "date": "2024-11-15"
  },
  "line_items": [
    {
      "description": "Panchakarma Therapy (5 sessions)",
      "qty": 1,
      "rate": 3000.0,
      "amount": 3000.0
    },
    {
      "description": "Consultation",
      "qty": 1,
      "rate": 1000.0,
      "amount": 1000.0
    }
  ],
  "totals": {
    "subtotal": 4000.0,
    "discount": 0.0,
    "gst": 0.0,
    "total": 4000.0
  },
  "payment": {
    "mode": "UPI",
    "received_by": "Cashier",
    "stamp_text": "[CASHIER STAMP]"
  },
  "notes": "Component Failure - Graceful Degradation",
  "layout": {
    "canvas": {
      "width": 1400,
      "height": 1800,
      "margin": 60
    },
    "table": {
      "top_y": 560,
      "row_height": 56,
      "columns": [
        {
          "key": "description",
          "label": "DESCRIPTION",
          "x": 95
        },
        {
          "key": "qty",
          "label": "QTY",
          "x": 860
        },
        {
          "key": "rate",
          "label": "RATE",
          "x": 980
        },
        {
          "key": "amount",
          "label": "AMOUNT",
          "x": 1140
        }
      ]
    }
  }
}
```

```distortion_presets
[
  {
    "name": "mild_blur",
    "reason": "soft camera focus"
  },
  {
    "name": "grayscale_scan",
    "reason": "claim desk scan"
  },
  {
    "name": "phone_photo",
    "reason": "mobile capture"
  }
]
```
