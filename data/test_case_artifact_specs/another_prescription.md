# PRESCRIPTION – TC001: Wrong Document Uploaded

Generated spec for `another_prescription` from `test_case_missing_artifacts_manifest.json`.
Template: `prescription_wrong_doc`  Quality: `GOOD`

Special constraints:
- Keep this as a second valid prescription from a different consultation context so the upload contains two prescriptions and no bill.

```prescription_spec
{
  "document_id": "another_prescription",
  "document_type": "PRESCRIPTION",
  "quality": "GOOD",
  "clinic": {
    "name": "City Medical Centre",
    "address": "12 MG Road, Bengaluru - 560001",
    "phone": "080-22334455"
  },
  "doctor": {
    "name": "Dr. M. Krishnan",
    "registration": "KA/78901/2020",
    "specialization": "General Physician"
  },
  "patient": {
    "name": "Rajesh Kumar",
    "age": 36,
    "gender_display": "Male"
  },
  "date": "2024-11-15",
  "diagnosis": "Hypertension Follow-up",
  "medicines": [
    "Amlodipine 5mg",
    "Telmisartan 40mg"
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
