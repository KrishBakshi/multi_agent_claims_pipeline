# PRESCRIPTION – TC002: Unreadable Document

Generated spec for `prescription` from `test_case_missing_artifacts_manifest.json`.
Template: `prescription_clean`  Quality: `GOOD`

```prescription_spec
{
  "document_id": "prescription",
  "document_type": "PRESCRIPTION",
  "quality": "GOOD",
  "clinic": {
    "name": "City Medical Centre",
    "address": "12 MG Road, Bengaluru - 560001",
    "phone": "080-22334455"
  },
  "doctor": {
    "name": "Dr. R. Nair",
    "registration": "KA/34521/2017",
    "specialization": "General Physician"
  },
  "patient": {
    "name": "Sneha Reddy",
    "age": 36,
    "gender_display": "Male"
  },
  "date": "2024-11-15",
  "diagnosis": "Migraine",
  "medicines": [
    "Sumatriptan 50mg",
    "Domperidone 10mg"
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
