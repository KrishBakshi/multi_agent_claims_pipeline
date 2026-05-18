# PHARMACY_BILL – TC002: Unreadable Document

Generated spec for `blurry_bill` from `test_case_missing_artifacts_manifest.json`.
Template: `pharmacy_bill_unreadable`  Quality: `UNREADABLE`

Special constraints:
- The bill should still be identifiable as a pharmacy bill, but medically relevant text must be unreadable.

```invoice_spec
{
  "document_id": "blurry_bill",
  "document_type": "PHARMACY_BILL",
  "claim_category": "PHARMACY",
  "quality": "UNREADABLE",
  "policy_context": {
    "policy_id": "PLUM_GHI_2024"
  },
  "provider": {
    "name": "MedCare Pharmacy",
    "address": "7 Commercial Street, Bengaluru - 560001",
    "meta_line": "Drug Lic. No: KA-BLR-PH-12345 | Ph: 080-12341234 | Network Pharmacy"
  },
  "patient": {
    "member_id": "EMP",
    "name": "Sneha Reddy",
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
    "title": "PHARMACY BILL",
    "bill_no": "PH/BLL/2024/60227",
    "date": "2024-11-15"
  },
  "line_items": [
    {
      "description": "Sumatriptan 50mg Tablets x 4",
      "qty": 4,
      "rate": 38.0,
      "amount": 152.0
    },
    {
      "description": "Domperidone 10mg Tablets x 10",
      "qty": 10,
      "rate": 5.5,
      "amount": 55.0
    },
    {
      "description": "Multivitamin Syrup 100ml",
      "qty": 1,
      "rate": 95.0,
      "amount": 95.0
    }
  ],
  "totals": {
    "subtotal": 302.0,
    "discount": 0.0,
    "gst": 0.0,
    "total": 302.0
  },
  "payment": {
    "mode": "Cash",
    "received_by": "Pharmacist",
    "stamp_text": "[PHARMACIST STAMP]"
  },
  "notes": "Unreadable Document",
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
          "label": "MEDICINE",
          "x": 95
        },
        {
          "key": "qty",
          "label": "QTY",
          "x": 860
        },
        {
          "key": "rate",
          "label": "MRP",
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
    "name": "strong_blur",
    "reason": "severe defocus - medically unreadable"
  },
  {
    "name": "jpeg_low_quality",
    "reason": "heavily compressed bad capture"
  }
]
```
