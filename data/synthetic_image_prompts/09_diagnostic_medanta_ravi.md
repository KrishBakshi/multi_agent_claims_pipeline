# Image Prompt 09 — Medanta Diagnostic Report, Ravi Menon
# Edge Scenario: Scanned multi-page document — Page 1 of 3 from an ADF scanner

## Real-World Context

Medanta issued Ravi Menon a three-page diagnostic report for his diabetes screening and lipid panel. The hospital's administrative desk fed all three pages through an automatic document feeder (ADF) scanner to produce the digital submission. This image is Page 1 of 3: it contains the billing header, patient identification, and the full test results table with reference ranges. Pages 2 and 3 (not shown) contain the pathologist's interpretation, remarks, and sign-off. This is the "scanned PDF (multi-page)" scenario from the guide: each page must be processed separately and line items aggregated.

## Image Generation Prompt

Generate an ADF (automatic document feeder) scanner output of Page 1 of a 3-page Indian diagnostic services report on white A4 paper. ADF scans have a characteristic appearance: slight brightness variation from top to bottom as the paper moves through the scanner, a faint shadow on the left binding edge, and marginally sharper contrast in the upper third than the lower third. The "Page 1 of 3" indicator must be clearly printed in the footer.

Document type: diagnostic services bill and report, Page 1 of 3.
Provider name: Medanta.
Provider address: 12 Residency Extension, Bengaluru - 560071.
Header metadata line: GSTIN: 29MEDANTA4444X1ZX | Ph: 080-68002222 | Diagnostic Services | NABL Accredited.
Title text: DIAGNOSTIC SERVICES BILL.
Bill number: MED/DIAG/2025/01081.
Bill date: 2025-01-18.
Patient name: Ravi Menon.
Patient age and gender: 37 / Male.
Member ID: EMP008.
Relationship: SELF.
Doctor name: Dr. Rohan Iyer.
Doctor registration: MH/23456/2018.

Billing and test results table — column headers: TEST NAME, RESULT, UNIT, REFERENCE RANGE — exactly three rows:
- HbA1c | 7.2 | % | 4.0 – 5.6 (H)
- Fasting Blood Sugar | 118 | mg/dL | 70 – 100 (H)
- Lipid Profile — Total Cholesterol | 198 | mg/dL | < 200

Billing totals section (separate from the test results, below the table):
- Subtotal: 2180.00
- Discount: 180.00
- GST: 0.00
- Total Amount: 2000.00

Footer:
- Payment Mode: UPI
- Received By: C. Bose
- Stamp placeholder: [LAB BILLING STAMP]
- Page indicator (clearly printed): Page 1 of 3

ADF scanner artifact characteristics — render with precision:
- Brightness gradient: the top 15% of the page (provider header area) appears very slightly brighter/whiter than the bottom 15% (footer area) — a subtle but visible exposure variation characteristic of paper moving through a feeder.
- Left-edge shadow: a faint vertical shadow band approximately 8mm wide along the left margin, slightly darker than the rest of the page — from the ADF scanner's paper guide pressing against the edge.
- No camera angle, no perspective distortion — the document is straight and square.
- Slight scan line texture: barely perceptible horizontal banding at very high zoom, typical of a mid-range office ADF scanner.
- Overall the document is clearly legible with only subtle ADF artifacts.

Additional layout notes:
- The "NABL Accredited" text in the header meta-line signals laboratory accreditation — render it as a printed text badge, not a graphic logo.
- The "(H)" annotation after HbA1c and Fasting Blood Sugar results indicates "High" — this is printed in the RESULT column next to the value as a standard lab notation.
- "Page 1 of 3" appears centered in the footer below the billing totals.

Visual characteristics:
- ADF scan output — not a phone photo, not a flatbed scan.
- Black printed text throughout. No handwriting, no colored ink, no stamps on this page.
- All four page edges fully visible.
- All numeric values and reference ranges sharp and unambiguous.

Style: multi-page clinical diagnostic report processed through hospital document management. The pipeline must handle this as Page 1 of a set and aggregate or reference subsequent pages for full report context.
