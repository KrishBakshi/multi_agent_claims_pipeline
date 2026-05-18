# Image Prompt 06 — Columbia Asia Vision Care Bill, Kavita Nair
# Edge Scenario: Duplicate stamp — "DUPLICATE" rubber stamp across the document

## Real-World Context

Kavita Nair submitted her original Columbia Asia vision care bill to her insurer. When the insurer's office lost track of the original, Kavita returned to the hospital's billing counter to request a reprint. The billing clerk reprinted the bill and applied the hospital's official "DUPLICATE" rubber stamp diagonally across the top portion before handing it over — a mandatory authentication step. This is the "duplicate stamp" scenario from the guide: multiple "ORIGINAL" / "DUPLICATE" stamps that should be noted in extraction and surfaced to fraud detection.

## Image Generation Prompt

Generate a flat scan of an Indian hospital vision-care billing document on white A4 paper. The document is printed in black text and is clean underneath the stamp. A large diagonal "DUPLICATE" rubber stamp in bold red ink is applied across the top third of the document, spanning from the upper-left area to the upper-right area, running at approximately 20 degrees upward from left to right.

Document type: vision care bill.
Provider name: Columbia Asia.
Provider address: 24 Hebbal Ring Road, Bengaluru - 560024.
Header metadata line: GSTIN: 29COLASIA8080X1ZX | Ph: 080-61656666 | Vision Care Unit.
Title text: VISION CARE BILL.
Bill number: CAH/VIS/2024/06720.
Bill date: 2024-09-17.
Patient name: Kavita Nair.
Patient age and gender: 41 / Female.
Member ID: EMP006.
Relationship: SELF.
Doctor name: Dr. Rohan Iyer.
Doctor registration: MH/23456/2018.

Itemized table — column headers: DESCRIPTION, QTY, RATE, AMOUNT — exactly three rows:
- Eye Examination | 1 | 750.00 | 750.00
- Prescription Glasses Frame | 1 | 1800.00 | 1800.00
- Single Vision Lenses | 1 | 1950.00 | 1950.00

Totals:
- Subtotal: 4500.00
- Discount: 300.00
- GST: 0.00
- Total Amount: 4200.00

Footer:
- Payment Mode: UPI
- Received By: S. Lobo
- Stamp placeholder: [OPTICAL STAMP]

DUPLICATE stamp details — render with precision:
- Stamp text: "DUPLICATE" in large, bold, block capital letters.
- Stamp color: red ink (not blue, not black — distinctly red).
- Stamp orientation: diagonal, running approximately 20 degrees upward from left to right across the top third of the page.
- Stamp position: the leftmost letter of "DUPLICATE" begins near the provider address line on the left margin; the rightmost letter ends near the bill date area on the right side.
- The stamp overlaps: the provider name "Columbia Asia", the GSTIN/phone metadata line, and the "VISION CARE BILL" title text — these printed elements remain visible underneath the red ink, partially obscured.
- The billing table (patient name, line items, totals, footer) sits entirely below the stamp and is completely unobscured and fully legible.
- Stamp ink is dense and uneven: one corner where the stamp first touched has a slight ink blotch; the opposite corner is slightly lighter.
- The rubber stamp frame edges are subtly visible as a faint rectangular boundary around the word.

Visual characteristics:
- Flat institutional scan. No perspective, no shadow.
- Printed document text is black ink; duplicate stamp is red ink only — no other colors.
- No eyewear photos, no colored backgrounds, no handwriting.
- All four page edges fully visible.
- All billing data below the stamp zone is sharp and unambiguous.

Style: reissued hospital billing copy with mandatory duplicate authentication stamp. The stamp must be clearly "DUPLICATE" and clearly red — distinguishable by both vision models and fraud-detection agents.
