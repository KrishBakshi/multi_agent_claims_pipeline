# HOSPITAL_BILL – TC006: Dental Partial Approval - Cosmetic Exclusion

Generated spec for `tc006_01_hospital_bill_emp002` from `test_case_missing_artifacts_manifest.json`.
Template: `hospital_bill_clean`  Quality: `GOOD`

Special constraints:
- Keep both line items clearly itemized because the scenario depends on line-item adjudication.

```invoice_spec
{
  "document_id": "tc006_01_hospital_bill_emp002",
  "document_type": "HOSPITAL_BILL",
  "claim_category": "DENTAL",
  "quality": "GOOD",
  "policy_context": {
    "policy_id": "PLUM_GHI_2024"
  },
  "provider": {
    "name": "Smile Dental Clinic",
    "address": "5 Cunningham Road, Bengaluru - 560052",
    "meta_line": "GSTIN: 29SMILEDENT33X1ZX | Ph: 080-23456789 | Network Dental Unit"
  },
  "patient": {
    "member_id": "EMP",
    "name": "Priya Singh",
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
    "title": "DENTAL BILL / RECEIPT",
    "bill_no": "DEN/BLL/2024/86319",
    "date": "2024-11-15"
  },
  "line_items": [
    {
      "description": "Root Canal Treatment",
      "qty": 1,
      "rate": 8000.0,
      "amount": 8000.0
    },
    {
      "description": "Teeth Whitening",
      "qty": 1,
      "rate": 4000.0,
      "amount": 4000.0
    }
  ],
  "totals": {
    "subtotal": 12000.0,
    "discount": 0.0,
    "gst": 0.0,
    "total": 12000.0
  },
  "payment": {
    "mode": "UPI",
    "received_by": "Cashier",
    "stamp_text": "[CASHIER STAMP]"
  },
  "notes": "Dental Partial Approval - Cosmetic Exclusion",
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
