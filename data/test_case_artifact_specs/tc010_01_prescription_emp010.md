# PRESCRIPTION – TC010: Network Hospital - Discount Applied

Generated spec for `tc010_01_prescription_emp010` from `test_case_missing_artifacts_manifest.json`.
Template: `prescription_clean`  Quality: `GOOD`

```prescription_spec
{
  "document_id": "tc010_01_prescription_emp010",
  "document_type": "PRESCRIPTION",
  "quality": "GOOD",
  "clinic": {
    "name": "City Medical Centre",
    "address": "12 MG Road, Bengaluru - 560001",
    "phone": "080-22334455"
  },
  "doctor": {
    "name": "Dr. S. Iyer",
    "registration": "TN/56789/2013",
    "specialization": "Pulmonology"
  },
  "patient": {
    "name": "Deepak Shah",
    "age": 36,
    "gender_display": "Male"
  },
  "date": "2024-11-15",
  "diagnosis": "Acute Bronchitis",
  "medicines": [
    "Amoxicillin 500mg",
    "Salbutamol Inhaler"
  ],
  "tests_ordered": [],
  "layout": {
    "canvas": {
      "width": 1400,
      "height": 1800,
      "margin": 60
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
