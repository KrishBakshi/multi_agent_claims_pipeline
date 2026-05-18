# Image Prompt 10 — Apollo Pharmacy Cash Memo, Deepak Shah
# Edge Scenario: Amounts written in words and figures — handwritten confirmation below printed total

## Real-World Context

Apollo Hospitals pharmacy uses a printed cash memo for all transactions. For amounts above Rs. 300, the pharmacist's standard practice is to handwrite a confirmation of the total in words at the bottom of the printed bill — a common Indian accounting convention to prevent tampering (if the printed figure is altered, the handwritten words remain as evidence). Deepak Shah's memo shows the printed Total Amount of Rs. 330.00 followed by the pharmacist's handwritten confirmation: "Rupees Three Hundred and Thirty Only /-". This is the "amounts written in words and figures" variation from the guide: a discrepancy between printed and written totals is possible and must be surfaced.

## Image Generation Prompt

Generate a flat scan of an Indian hospital pharmacy cash memo on white A4 paper. The bulk of the document is machine-printed in black ink. Below the printed "Total Amount: 330.00" line, a single line of neat handwriting in blue ballpoint pen has been added by the pharmacist — the total amount spelled out in words. This handwritten line is the key feature of this document.

Document type: pharmacy cash memo.
Provider name: Apollo Hospitals.
Provider address: 154 Residency Road, Bengaluru - 560025.
Header metadata line: Drug Lic. No: KA-BLR-55102 | Ph: 080-44112233 | Hospital Pharmacy.
Title text: PHARMACY CASH MEMO.
Bill number: APH/PH/2025/01590.
Bill date: 2025-02-06.
Patient name: Deepak Shah.
Patient age and gender: 45 / Male.
Member ID: EMP010.
Relationship: SELF.
Prescribing doctor: Dr. Kavya Rao.
Doctor registration: TN/56789/2013.

Medicine table — column headers: MEDICINE, QTY, MRP, AMOUNT — exactly four rows:
- Pantoprazole 40 mg Tablets | 15 | 6.50 | 97.50
- Antacid Suspension 150 ml | 1 | 135.00 | 135.00
- Domperidone Tablets | 10 | 5.50 | 55.00
- ORS Sachets | 5 | 12.50 | 62.50

Totals (printed):
- Subtotal: 350.00
- Discount: 20.00
- GST: 0.00
- Total Amount: 330.00

Handwritten amount-in-words line — render with precision:
- Position: immediately below the printed "Total Amount: 330.00" line, before the footer section divider.
- Text (handwritten in blue ballpoint pen): "Rupees Three Hundred and Thirty Only /-"
- Handwriting style: neat, practiced, upright strokes — a pharmacist who writes this line many times per day. Letter forms are consistent but not mechanical.
- The slash-dash "/-" at the end is a standard Indian accounting notation for "no paise" and is rendered in the same blue ink.
- Pen pressure is moderate — no smearing, no excess ink blobs.
- The handwritten line is clearly distinguishable from the printed text above and below it: different ink color (blue vs. black), different character style (cursive-adjacent vs. machine font).

Footer (printed):
- Payment Mode: Cash
- Received By: T. George
- Stamp placeholder: [PHARMACY DESK STAMP]

Visual characteristics:
- Flat institutional scan. No perspective, no shadow.
- Printed elements: black ink. Handwritten amount-in-words: blue ballpoint ink.
- No product images, no thermal-paper black background, no colored branding panels.
- No cropped receipt format — standard A4 page, all edges visible.
- No duplicate medicine rows, no quantity edits in the table.
- All printed fields sharp and unambiguous.

Style: hospital pharmacy cash memo with handwritten total-in-words confirmation. The pipeline must capture both the printed numeric total and the handwritten words total, and check them for consistency as a fraud-detection signal.
