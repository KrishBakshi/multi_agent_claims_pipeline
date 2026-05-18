# PRESCRIPTION – TC008: Per-Claim Limit Exceeded

Generated spec for `tc008_01_prescription_emp003` from `test_case_missing_artifacts_manifest.json`.
Template: `prescription_clean`  Quality: `GOOD`

```prescription_spec
{
  "document_id": "tc008_01_prescription_emp003",
  "document_type": "PRESCRIPTION",
  "quality": "GOOD",
  "clinic": {
    "name": "City Medical Centre",
    "address": "12 MG Road, Bengaluru - 560001",
    "phone": "080-22334455"
  },
  "doctor": {
    "name": "Dr. R. Gupta",
    "registration": "DL/34567/2016",
    "specialization": "General Medicine"
  },
  "patient": {
    "name": "Ravi Sharma",
    "age": 36,
    "gender_display": "Male"
  },
  "date": "2024-11-15",
  "diagnosis": "Gastroenteritis",
  "medicines": [
    "Antibiotics",
    "Probiotics",
    "ORS"
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
