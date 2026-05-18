# Image Prompt 08 — Sakra World Hospital Bill, Anita Desai
# Edge Scenario: Multiple corrections — amounts crossed out and rewritten (DOCUMENT_ALTERATION)

## Real-World Context

The Sakra World Hospital billing clerk initially entered the "Administrative and File Charge" at Rs. 200.00 — the old rate before a recent rate card revision. A supervisor caught the error during review. The clerk crossed out 200.00 in both the RATE and AMOUNT columns with a horizontal pen stroke and wrote the correct value 150.00 immediately above each struck figure, initialing the correction. The Subtotal and Total Amount lines printed originally as 1550.00 were also struck through and corrected to 1500.00 by hand. This is the "multiple corrections" scenario from the guide: amounts crossed out and rewritten, which should trigger a DOCUMENT_ALTERATION flag in the fraud check stage.

## Image Generation Prompt

Generate a flat scan of an Indian outpatient hospital bill on white A4 paper. The document is machine-printed in black ink. One row in the billing table and both total lines have visible handwritten corrections in blue ballpoint pen — the original printed values are struck through with a single horizontal line and the correct values are handwritten just above each struck number. Initials appear beside one correction.

Document type: outpatient bill.
Provider name: Sakra World Hospital.
Provider address: 52 Outer Ring Road, Bengaluru - 560103.
Header metadata line: GSTIN: 29SAKRA3333X1ZX | Ph: 080-49694969 | Network Hospital.
Title text: OUTPATIENT BILL.
Bill number: SWH/OPD/2024/12048.
Bill date: 2024-12-11.
Patient name: Anita Desai.
Patient age and gender: 31 / Female.
Member ID: EMP009.
Relationship: SELF.
Doctor name: Dr. Kavya Rao.
Doctor registration: TN/56789/2013.

Billing table — column headers: DESCRIPTION, QTY, RATE, AMOUNT — three rows:
- Consultation Fee | 1 | 1000.00 | 1000.00 (printed, no correction)
- Urine Routine Test | 1 | 350.00 | 350.00 (printed, no correction)
- Administrative and File Charge | 1 | [correction — see below] | [correction — see below]

Correction details for "Administrative and File Charge" row — render with precision:
- RATE column: printed "200.00" with a single horizontal blue pen line struck through it; handwritten "150.00" written in blue pen directly above the struck figure.
- AMOUNT column: printed "200.00" with a single horizontal blue pen line struck through it; handwritten "150.00" written in blue pen directly above, with small initials "KM" written in blue pen to the right of the corrected amount.
- The struck-through "200.00" values remain legible beneath the strikethrough line.
- The handwritten "150.00" values are neat but clearly manual — slightly larger letter forms than the printed text.

Totals corrections — render with precision:
- Subtotal row: printed "1550.00" with a blue pen horizontal strikethrough; handwritten "1500.00" written above.
- Discount row: printed "0.00" — no correction.
- GST row: printed "0.00" — no correction.
- Total Amount row: printed "1550.00" with a blue pen horizontal strikethrough; handwritten "1500.00" written above, underlined once in pen for emphasis.

Footer (no corrections):
- Payment Mode: Card
- Received By: J. Mary
- Stamp placeholder: [FRONT OFFICE STAMP]

Visual characteristics:
- Flat scan. No perspective, no shadow.
- Background document text: black printed ink.
- All corrections: blue ballpoint pen — strikethroughs, replacement values, initials.
- The corrections are localized to the third table row and the subtotal/total lines; all other fields are clean printed text.
- No folding, no camera angle, no additional stamps beyond the footer placeholder.
- All fields — including the corrections — are legible.

Style: internally corrected hospital billing document. The alteration is clearly visible and authentic. The pipeline's fraud-check agent must detect and flag DOCUMENT_ALTERATION based on the visible crossed-out and rewritten amounts.
