# Image Prompt 07 — Aster CMI Ayurveda Bill, Suresh Patil
# Edge Scenario: Partial document — folded paper, bottom corner obscured

## Real-World Context

Suresh Patil tucked his Aster CMI Hospital Ayurveda bill into his shirt pocket after the visit. By the time he retrieved it for his insurance claim, the bill had been folded in half horizontally and the bottom-right corner had been bent inward from the tight pocket. The document was placed flat on a desk and photographed, but the fold crease runs visibly across the middle and the bent corner partially hides the "Received By" line and the stamp placeholder. This is the "partial document" scenario from the guide: page folded, with available fields extracted and missing fields explicitly flagged.

## Image Generation Prompt

Generate a photo of an Indian Ayurveda hospital bill lying on a flat desk surface, taken from directly above with a smartphone or camera. The document has been folded horizontally in half and then unfolded — a clear horizontal crease runs across the center of the page. The bottom-right corner of the paper has been bent inward, partially hiding content in that area.

Document type: Ayurveda OPD bill.
Provider name: Aster CMI Hospital.
Provider address: 43 New Airport Road, Bengaluru - 560092.
Header metadata line: GSTIN: 29ASTER1111X1ZX | Ph: 080-43420100 | Ayurveda OPD.
Title text: AYURVEDA OPD BILL.
Bill number: ASTER/AY/2024/02814.
Bill date: 2024-07-12.
Patient name: Suresh Patil.
Patient age and gender: 48 / Male.
Member ID: EMP007.
Relationship: SELF.
Doctor name: Dr. Anjali Menon.
Doctor registration: AYUR/KL/2345/2019.

Billing table — column headers: DESCRIPTION, QTY, RATE, AMOUNT — exactly three rows:
- Ayurveda Physician Consultation | 1 | 900.00 | 900.00
- Abhyanga Therapy Session | 1 | 1500.00 | 1500.00
- Prescribed Kashayam Pack | 1 | 650.00 | 650.00

Totals (visible despite crease):
- Subtotal: 3050.00
- Discount: 150.00
- GST: 0.00
- Total Amount: 2900.00

Footer — partially obscured by bent corner:
- Payment Mode: Cash (visible)
- Received By: L. Haridas (partially obscured — first name "L." visible, surname "Haridas" hidden under the bent corner)
- Stamp placeholder: [AYURVEDA BILLING STAMP] (mostly hidden under the bent corner)

Physical damage characteristics — render with precision:
- Horizontal fold crease: a clear ridge line running across the full width of the page at approximately the vertical midpoint. Above the crease the paper is smooth; below the crease the paper has slight wave distortion from being unfolded.
- Along the crease itself, a thin shadow line appears where the paper was pressed — text that falls directly on the crease line may show minor distortion but remains readable.
- Bottom-right corner bent: roughly a 4 cm triangular fold in the lower-right corner, with the paper turned over onto itself. The bent flap creates a triangular shadow zone beneath it.
- The "Received By: L. Haridas" line and the "[AYURVEDA BILLING STAMP]" text fall within the bent corner zone — only "Received By: L." is visible; the rest is hidden under the folded corner.
- The Total Amount: 2900.00 is fully visible despite being near the crease — it sits just above the fold line.
- Warm ambient desk lighting: slight warm-yellow tone to the white paper. A faint shadow from the bent corner flap falls on the paper surface.
- No perspective skew — camera is directly above. But the crease causes a subtle 3D ridge effect in the center.

Visual characteristics:
- Photograph on a desk surface, not a flat scanner output.
- All upper-half content (provider name through billing table) is clean and fully legible.
- Lower-half content readable except in the bent-corner zone.
- No spa candles, no leaf graphics, no decorative backgrounds.
- No handwriting additions. Machine-printed text only.

Style: patient-submitted document with real physical handling damage. The pipeline must extract all available fields and explicitly flag "Received By" and stamp as unreadable/missing.
