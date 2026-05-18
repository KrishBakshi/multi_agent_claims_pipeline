# PRESCRIPTION – TC005: Waiting Period - Diabetes

Generated spec for `tc005_01_prescription_emp005` from `test_case_missing_artifacts_manifest.json`.
Template: `prescription_clean`  Quality: `GOOD`

```prescription_spec
{
  "document_id": "tc005_01_prescription_emp005",
  "document_type": "PRESCRIPTION",
  "quality": "GOOD",
  "clinic": {
    "name": "City Medical Centre",
    "address": "12 MG Road, Bengaluru - 560001",
    "phone": "080-22334455"
  },
  "doctor": {
    "name": "Dr. Sunil Mehta",
    "registration": "GJ/56789/2014",
    "specialization": "Endocrinology"
  },
  "patient": {
    "name": "Vikram Joshi",
    "age": 36,
    "gender_display": "Male"
  },
  "date": "2024-11-15",
  "diagnosis": "Type 2 Diabetes Mellitus",
  "medicines": [
    "Metformin 500mg",
    "Glimepiride 1mg"
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
