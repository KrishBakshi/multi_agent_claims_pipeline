# PRESCRIPTION – TC003: Documents Belong to Different Patients

Generated spec for `prescription_rajesh` from `test_case_missing_artifacts_manifest.json`.
Template: `prescription_mismatch_name`  Quality: `GOOD`

Special constraints:
- Patient name must remain Rajesh Kumar.

```prescription_spec
{
  "document_id": "prescription_rajesh",
  "document_type": "PRESCRIPTION",
  "quality": "GOOD",
  "clinic": {
    "name": "City Medical Centre",
    "address": "12 MG Road, Bengaluru - 560001",
    "phone": "080-22334455"
  },
  "doctor": {
    "name": "Dr. A. Mehta",
    "registration": "KA/12345/2018",
    "specialization": "General Physician"
  },
  "patient": {
    "name": "Rajesh Kumar",
    "age": 36,
    "gender_display": "Male"
  },
  "date": "2024-11-15",
  "diagnosis": "Acute Viral Infection",
  "medicines": [
    "Paracetamol 500mg",
    "Cetirizine 10mg"
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
