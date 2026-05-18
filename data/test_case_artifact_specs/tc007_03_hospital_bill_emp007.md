# HOSPITAL_BILL – TC007: MRI Without Pre-Authorization

Generated spec for `tc007_03_hospital_bill_emp007` from `test_case_missing_artifacts_manifest.json`.
Template: `hospital_bill_clean`  Quality: `GOOD`

```invoice_spec
{
  "document_id": "tc007_03_hospital_bill_emp007",
  "document_type": "HOSPITAL_BILL",
  "claim_category": "DIAGNOSTIC",
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
    "title": "DIAGNOSTIC BILL / RECEIPT",
    "bill_no": "DIAG/BLL/2024/87593",
    "date": "2024-11-15"
  },
  "line_items": [
    {
      "description": "MRI Lumbar Spine",
      "qty": 1,
      "rate": 15000.0,
      "amount": 15000.0
    }
  ],
  "totals": {
    "subtotal": 15000.0,
    "discount": 0.0,
    "gst": 0.0,
    "total": 15000.0
  },
  "payment": {
    "mode": "UPI",
    "received_by": "Cashier",
    "stamp_text": "[CASHIER STAMP]"
  },
  "notes": "MRI Without Pre-Authorization",
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
