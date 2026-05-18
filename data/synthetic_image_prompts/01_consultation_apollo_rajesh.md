# Image Prompt 01 — Apollo OPD Bill, Rajesh Kumar
# Edge Scenario: Clean institutional flat-bed scan (baseline / control)

## Real-World Context

A billing cashier at Apollo Hospitals, Bengaluru placed this freshly printed OPD receipt flat on the hospital's departmental document scanner and pressed scan. No handling, no folding, no stamps added after printing. This is the cleanest version of a real hospital bill — it represents the ideal input the pipeline should handle perfectly before introducing any degradation.

## Image Generation Prompt

Generate a flat-bed institutional scanner output of an Indian outpatient hospital bill on a white A4 sheet. The paper is perfectly level, square, and centered on the scanner glass. Scanner lighting is even and cold-white with no gradient. A thin uniform gray border surrounds the page edge — the gap between paper and scanner lid.

Document type: outpatient hospital bill.
Provider name: Apollo Hospitals.
Provider address: 154 Residency Road, Bengaluru - 560025.
Header metadata line: GSTIN: 29APOLLO1234X1ZX | Ph: 080-44112233 | Network Hospital.
Title text: BILL / RECEIPT.
Bill number: APH/OPD/2024/04152.
Bill date: 2024-11-01.
Patient name: Rajesh Kumar.
Patient age and gender: 39 / Male.
Member ID: EMP001.
Relationship: SELF.
Referring doctor: Dr. Arun Sharma.
Doctor registration: KA/45678/2015.

Itemized table — column headers: DESCRIPTION, QTY, RATE, AMOUNT — exactly three rows:
- General Physician Consultation (OPD) | 1 | 1200.00 | 1200.00
- Temperature and Vitals Assessment | 1 | 250.00 | 250.00
- CBC Sample Collection Charge | 1 | 300.00 | 300.00

Totals:
- Subtotal: 1750.00
- Discount: 0.00
- GST: 0.00
- Total Amount: 1750.00

Footer:
- Payment Mode: UPI
- Received By: K. Nataraj
- Stamp placeholder: [CASHIER STAMP]

Visual characteristics:
- All text is machine-printed, black ink only. No handwriting anywhere.
- Horizontal section dividers are straight printed lines.
- Scanner introduces only the faintest pixel grain across the white background — almost imperceptible.
- No shadows, no perspective, no color shift, no lens distortion.
- No logo artwork, no watermarks, no torn edges.
- All four page edges fully visible within the frame.
- Every field legible and unambiguous.

Style: corporate hospital billing counter printout. The cleanest possible document for OCR benchmarking.
