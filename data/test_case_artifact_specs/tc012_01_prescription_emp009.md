# PRESCRIPTION – TC012: Excluded Treatment

Generated spec for `tc012_01_prescription_emp009` from `test_case_missing_artifacts_manifest.json`.
Template: `prescription_clean`  Quality: `GOOD`

```prescription_spec
{
  "document_id": "tc012_01_prescription_emp009",
  "document_type": "PRESCRIPTION",
  "quality": "GOOD",
  "clinic": {
    "name": "City Medical Centre",
    "address": "12 MG Road, Bengaluru - 560001",
    "phone": "080-22334455"
  },
  "doctor": {
    "name": "Dr. P. Banerjee",
    "registration": "WB/34567/2015",
    "specialization": "Bariatric Medicine"
  },
  "patient": {
    "name": "Ravi Sharma",
    "age": 36,
    "gender_display": "Male"
  },
  "date": "2024-11-15",
  "diagnosis": "Morbid Obesity - BMI 37",
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
  "treatment": "Bariatric Consultation and Customised Diet Plan"
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
