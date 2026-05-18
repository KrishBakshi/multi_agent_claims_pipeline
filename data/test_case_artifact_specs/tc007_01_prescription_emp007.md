# PRESCRIPTION – TC007: MRI Without Pre-Authorization

Generated spec for `tc007_01_prescription_emp007` from `test_case_missing_artifacts_manifest.json`.
Template: `prescription_clean`  Quality: `GOOD`

```prescription_spec
{
  "document_id": "tc007_01_prescription_emp007",
  "document_type": "PRESCRIPTION",
  "quality": "GOOD",
  "clinic": {
    "name": "City Medical Centre",
    "address": "12 MG Road, Bengaluru - 560001",
    "phone": "080-22334455"
  },
  "doctor": {
    "name": "Dr. Venkat Rao",
    "registration": "AP/67890/2017",
    "specialization": "Orthopedics"
  },
  "patient": {
    "name": "Ravi Sharma",
    "age": 36,
    "gender_display": "Male"
  },
  "date": "2024-11-15",
  "diagnosis": "Suspected Lumbar Disc Herniation",
  "medicines": [
    "Paracetamol 500mg",
    "Cetirizine 10mg"
  ],
  "tests_ordered": [
    "MRI Lumbar Spine"
  ],
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
