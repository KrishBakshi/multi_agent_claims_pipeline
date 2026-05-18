# PRESCRIPTION – TC011: Component Failure - Graceful Degradation

Generated spec for `tc011_01_prescription_emp006` from `test_case_missing_artifacts_manifest.json`.
Template: `prescription_clean`  Quality: `GOOD`

Special constraints:
- Use an AYUSH or Ayurveda prescription layout with valid practitioner details.

```prescription_spec
{
  "document_id": "tc011_01_prescription_emp006",
  "document_type": "PRESCRIPTION",
  "quality": "GOOD",
  "clinic": {
    "name": "Dhanvantari Ayurveda Kendra",
    "address": "18 Jayanagar 4th Block, Bengaluru - 560041",
    "phone": "080-26548899"
  },
  "doctor": {
    "name": "Vaidya T. Krishnan",
    "registration": "AYUR/KL/2345/2019",
    "specialization": "Ayurveda"
  },
  "patient": {
    "name": "Ravi Sharma",
    "age": 36,
    "gender_display": "Male"
  },
  "date": "2024-11-15",
  "diagnosis": "Chronic Joint Pain",
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
  },
  "treatment": "Panchakarma Therapy"
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
