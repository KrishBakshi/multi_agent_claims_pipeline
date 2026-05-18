# HOSPITAL_BILL – TC009: Fraud Signal - Multiple Same-Day Claims

Generated spec for `tc009_02_hospital_bill_emp008` from `test_case_missing_artifacts_manifest.json`.
Template: `hospital_bill_clean`  Quality: `GOOD`

Special constraints:
- Use a plausible consultation bill totaling exactly 4800.00.

```invoice_spec
{
  "document_id": "tc009_02_hospital_bill_emp008",
  "document_type": "HOSPITAL_BILL",
  "claim_category": "CONSULTATION",
  "quality": "GOOD",
  "policy_context": {
    "policy_id": "PLUM_GHI_2024"
  },
  "provider": {
    "name": "City Hospital",
    "address": "56 Rajajinagar, Bengaluru - 560010",
    "meta_line": "GSTIN: 29DEFHOSP1111X1ZX | Ph: 080-23456789"
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
    "title": "BILL / RECEIPT",
    "bill_no": "CONS/BLL/2024/70220",
    "date": "2024-11-15"
  },
  "line_items": [
    {
      "description": "Consultation Fee",
      "qty": 1,
      "rate": 4800.0,
      "amount": 4800.0
    }
  ],
  "totals": {
    "subtotal": 4800.0,
    "discount": 0.0,
    "gst": 0.0,
    "total": 4800.0
  },
  "payment": {
    "mode": "UPI",
    "received_by": "Cashier",
    "stamp_text": "[CASHIER STAMP]"
  },
  "notes": "Fraud Signal - Multiple Same-Day Claims",
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
