# Image Prompt 04 — Max Healthcare Dental Bill, Sneha Reddy
# Edge Scenario: Pre-printed template with handwritten fill-ins

## Real-World Context

Max Healthcare's dental unit uses a pre-printed stationery billing form. The paper arrives from the print shop with all borders, column headers, section labels, and the clinic header already printed. The billing clerk fills in all patient-specific values — name, date, procedure amounts, and the "Received By" line — by hand using a blue ballpoint pen. This is one of the most common real-world document types in Indian clinics: the pre-printed template with handwritten fill-ins.

## Image Generation Prompt

Generate a flat scan of an Indian dental clinic billing form. The document uses a pre-printed template on white A4 paper — borders, dividers, column headers (DESCRIPTION, QTY, RATE, AMOUNT), section labels, and the provider header are all printed in black ink. Patient-specific fields are filled in by hand in blue ballpoint pen.

Document type: dental bill / receipt.
Provider name: Max Healthcare. (printed)
Provider address: 31 Richmond Town, Bengaluru - 560025. (printed)
Header metadata line: GSTIN: 29MAXCARE2222X1ZX | Ph: 080-61112222 | Network Dental Unit. (printed)
Title text: DENTAL BILL / RECEIPT. (printed)
Bill number: MAX/DEN/2024/05477. (handwritten in blue pen in the blank after "Bill No:")
Bill date: 09-Aug-2024. (handwritten in blue pen in the blank after "Date:")
Patient name: Sneha Reddy. (handwritten in blue pen)
Patient age and gender: 32 / Female. (handwritten in blue pen)
Member ID: EMP004. (handwritten in blue pen)
Relationship: SELF. (handwritten in blue pen)
Doctor name: Dr. Neha Gupta. (handwritten in blue pen)
Doctor registration: DL/34567/2016. (handwritten in blue pen)

Billing table — headers DESCRIPTION, QTY, RATE, AMOUNT are printed. Procedure names are printed. QTY, RATE, and AMOUNT values are handwritten in blue pen:
- Dental Consultation | 1 | 500.00 | 500.00
- Scaling and Polishing | 1 | 1800.00 | 1800.00
- Dental X-Ray (Single View) | 1 | 450.00 | 450.00

Totals — labels printed, values handwritten in blue pen:
- Subtotal: 2750.00
- Discount: 0.00
- GST: 0.00
- Total Amount: 2750.00

Footer — "Payment Mode:", "Received By:", and "Notes:" labels are printed; values handwritten:
- Payment Mode: UPI (handwritten)
- Received By: M. Shetty (handwritten)
- Stamp placeholder: [DENTAL DESK STAMP] (printed placeholder text)

Handwriting characteristics — render authentically:
- Blue ballpoint pen ink throughout all handwritten fields.
- The handwriting is neat and practiced (a billing clerk who fills this form daily) but shows natural variability in letter size and pen pressure.
- One small ink smear near the Total Amount figure where the pen nib dragged slightly — the number is still legible.
- Pen pressure slightly heavier on the number "2750.00" total, producing a slightly bolder stroke there.
- No crossed-out corrections, no erasures — this bill was filled cleanly.
- The handwritten text sits visibly above the printed baseline guide rules of the template.

Visual characteristics:
- Flat scan. No perspective, no shadow.
- Pre-printed elements in black ink; handwritten fills in blue ink.
- No dental illustrations, no colored backgrounds, no logo artwork.
- All four page edges fully visible.
- Every figure legible.

Style: standard Indian clinic pre-printed billing stationery, partially completed by hand. OCR must distinguish printed fields from handwritten ones.
