# LAB_REPORT – TC007: MRI Without Pre-Authorization

Generated spec for `tc007_02_lab_report_emp007` from `test_case_missing_artifacts_manifest.json`.
Template: `lab_report_clean`  Quality: `GOOD`

Special constraints:
- The report should clearly show MRI Lumbar Spine as the named test or study.

```lab_report_spec
{
  "document_id": "tc007_02_lab_report_emp007",
  "document_type": "LAB_REPORT",
  "quality": "GOOD",
  "lab": {
    "name": "Apollo Diagnostics",
    "address": "88 Residency Road, Bengaluru - 560025",
    "phone": "080-55667788",
    "license_no": "KA-BLR-LAB-22145"
  },
  "patient": {
    "name": "Ravi Sharma",
    "age": 35,
    "gender_display": "Male",
    "ref_doctor": "Dr. Venkat Rao"
  },
  "date": "2024-11-20",
  "test_name": "MRI Lumbar Spine",
  "report_no": "LAB/RPT/2024/30086",
  "findings": "MRI Lumbar Spine study performed and analysed. Report reviewed by the reporting doctor and dispatched to the referring physician.",
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
