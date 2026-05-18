# Test Case Prompt Templates

Use this file together with `data/test_case_missing_artifacts_manifest.json`.

Workflow:
- Pick one artefact entry from the manifest.
- Start with the prompt template whose `prompt_template_id` matches the entry.
- Replace bracketed placeholders with the `seed_fields` from the manifest entry.
- Apply every listed `special_constraints` line verbatim.
- Save the generated image or PDF at the manifest `target_path`.

## Template: `prescription_clean`

Generate a realistic Indian medical prescription on a white A4 sheet. Keep the page flat, fully visible, and easy to OCR. Use black machine-printed text with a standard clinic or hospital prescription layout.

Required fields:
- Doctor name: `[doctor_name]`
- Doctor registration: `[doctor_registration]`
- Patient name: `[patient_name]`
- Visit date: `[date]`
- Diagnosis: `[diagnosis]`
- Medicines or treatment: `[medicines_or_treatment]`
- Tests ordered if provided: `[tests_ordered]`

Rendering rules:
- Include clinic or hospital header, patient block, diagnosis section, Rx or treatment section, and doctor signature or stamp area.
- Use Indian registration-number formatting.
- Keep the document medically plausible and internally consistent.
- If a field is not supplied, infer a realistic value from the case context without changing the supplied facts.
- No decorative graphics, logos, or unrelated objects.

## Template: `prescription_wrong_doc`

Generate a realistic Indian prescription that is fully valid and clearly legible. The document must look authentic enough to be accepted as a real prescription, because this scenario tests wrong document type upload rather than bad quality.

Required elements:
- Doctor header with name, credentials, and registration number
- Patient block
- Date
- Diagnosis
- Medicine list
- Signature or stamp area

Rendering rules:
- Keep the document clean, sharp, and complete.
- Do not include billing or invoice elements.
- Use black printed text on white paper.

## Template: `prescription_mismatch_name`

Generate a clean Indian prescription with the patient name shown exactly as `[patient_name]`.

Required elements:
- Prominent patient name field
- Doctor header, registration number, diagnosis, date, and prescription body

Rendering rules:
- The patient name must be unambiguous and easy to read.
- Keep all other fields plausible for a consultation claim.
- Do not introduce another patient name anywhere else on the page.

## Template: `hospital_bill_clean`

Generate a realistic Indian hospital or clinic bill on a white A4 sheet, fully visible and easy to OCR. Use a standard billing-counter or hospital-receipt layout with machine-printed black text.

Required fields:
- Hospital or clinic name: `[hospital_name]`
- Patient name: `[patient_name]`
- Bill date: `[date]`
- Itemized line items: `[line_items]`
- Total amount: `[total]`

Rendering rules:
- Include provider header, bill title, bill number, patient block, itemized table, subtotal or total block, and payment footer.
- If `line_items` are not supplied, create a plausible itemized structure consistent with the total and claim category.
- Amounts must add up correctly to the total.
- No handwriting unless a case explicitly requires distortion or damage.
- No decorative graphics or unrelated objects.

## Template: `hospital_bill_mismatch_name`

Generate a clean Indian hospital bill with the patient name shown exactly as `[patient_name]`.

Required elements:
- Provider header
- Bill title and bill number
- Patient name field that is prominent and unambiguous
- Itemized charges and total

Rendering rules:
- The patient name must remain exactly `[patient_name]`.
- Keep the bill fully legible.
- Do not include any second patient name anywhere on the bill.

## Template: `pharmacy_bill_unreadable`

Generate an Indian pharmacy bill that is visually identifiable as a pharmacy bill but medically unreadable. The document should appear to be a patient-submitted photo or scan with severe blur or defocus.

Required elements:
- Pharmacy header and drug-license style metadata
- Bill number and date
- Patient or doctor reference line
- Medicine table structure
- Totals area

Rendering rules:
- Preserve the overall pharmacy-bill layout so the document type is recognizable.
- Make medicine names, amounts, and small text unreadable due to heavy blur or motion softness.
- Avoid artistic effects; this should look like a genuine bad capture.
- Keep the page boundaries visible enough to infer it is a real receipt or bill.

## Template: `lab_report_clean`

Generate a realistic Indian diagnostic or radiology report on a white A4 sheet with a clean lab-report layout.

Required fields:
- Test name: `[test_name]`
- Patient name if provided: `[patient_name]`
- Referring doctor if provided: `[doctor_name]`
- Sample or report date if provided: `[date]`

Rendering rules:
- Include lab header, patient block, report identifiers, test section, and reporting doctor or pathologist area.
- If the test is imaging-oriented, it may be phrased as a study or examination, but the exact supplied test name must appear.
- Keep the report fully legible and machine printed.
- No decorative graphics.
