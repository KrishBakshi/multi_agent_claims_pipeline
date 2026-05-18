# PRESCRIPTION – TC001: Wrong Document Uploaded

Generated spec for `dr_sharma_prescription` from `test_case_missing_artifacts_manifest.json`.
Template: `prescription_wrong_doc`  Quality: `GOOD`

Special constraints:
- Keep this as a valid prescription because the scenario depends on the member uploading the wrong document type.

```prescription_spec
{
  "document_id": "dr_sharma_prescription",
  "document_type": "PRESCRIPTION",
  "quality": "GOOD",
  "clinic": {
    "name": "City Medical Centre",
    "address": "12 MG Road, Bengaluru - 560001",
    "phone": "080-22334455"
  },
  "doctor": {
    "name": "Dr. Arun Sharma",
    "registration": "KA/45678/2015",
    "specialization": "Internal Medicine"
  },
  "patient": {
    "name": "Rajesh Kumar",
    "age": 36,
    "gender_display": "Male"
  },
  "date": "2024-11-15",
  "diagnosis": "Upper Respiratory Infection",
  "medicines": [
    "Amoxicillin 500mg",
    "Cetirizine 10mg",
    "Paracetamol 500mg"
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
