# Image Prompt 05 — Narayana Health Dental Bill, Vikram Joshi
# Edge Scenario: Multilingual document — Kannada and English mixed in procedure descriptions

## Real-World Context

Narayana Health serves a predominantly Kannada-speaking patient population in Bengaluru. Their dental billing system prints procedure descriptions in both English and Kannada script on the same bill — English for the insurance/admin record, Kannada for the patient's own reference. Vikram Joshi's root canal bill therefore has bilingual text in the DESCRIPTION column, with the Kannada equivalent appearing in a slightly smaller font directly beneath each English procedure name. This is the "multilingual doc" scenario from the guide: regional language text mixed with English.

## Image Generation Prompt

Generate a flat scan of an Indian hospital dental procedure bill on white A4 paper, printed in black ink. The key distinguishing feature is the DESCRIPTION column of the billing table: each procedure row contains two lines of text — the English name on the first line, and the Kannada (Devanagari-adjacent script, Kannada script specifically) equivalent on the second line in a slightly smaller font size. All other fields (patient name, doctor details, amounts, totals, footer) are in English only.

Document type: dental procedure bill.
Provider name: Narayana Health.
Provider address: 258 Hosur Road, Bengaluru - 560099.
Header metadata line: GSTIN: 29NARAYANA9101X1ZX | Ph: 080-71222222 | Network Dental Unit.
Title text: DENTAL PROCEDURE BILL.
Bill number: NH/DEN/2024/09110.
Bill date: 2024-11-22.
Patient name: Vikram Joshi.
Patient age and gender: 45 / Male.
Member ID: EMP005.
Relationship: SELF.
Doctor name: Dr. Neha Gupta.
Doctor registration: DL/34567/2016.

Billing table — column headers: DESCRIPTION, QTY, RATE, AMOUNT.
Each DESCRIPTION cell contains English on line 1 and Kannada script on line 2 (smaller font):
- Row 1: "Dental Consultation" / "ದಂತ ಸಮಾಲೋಚನೆ" | 1 | 600.00 | 600.00
- Row 2: "Root Canal Treatment" / "ರೂಟ್ ಕೆನಾಲ್ ಚಿಕಿತ್ಸೆ" | 1 | 3600.00 | 3600.00
- Row 3: "Temporary Crown Placement" / "ತಾತ್ಕಾಲಿಕ ಕ್ರೌನ್ ಅಳವಡಿಕೆ" | 1 | 700.00 | 700.00

Totals (English only):
- Subtotal: 4900.00
- Discount: 0.00
- GST: 0.00
- Total Amount: 4900.00

Footer (English only):
- Payment Mode: Card
- Received By: A. Prakash
- Stamp placeholder: [BILLING SEAL]

Bilingual layout characteristics — render with precision:
- DESCRIPTION column is visibly taller than in a standard bill because each row spans two text lines.
- English procedure name: regular font, same size as other column text.
- Kannada script line: same column, roughly 80% font size of the English line, positioned immediately below with a small gap.
- The Kannada script is printed in the same black ink — not a stamp, not handwriting, it is machine-printed.
- All four Kannada strings must render as actual Kannada script characters, not as placeholder boxes or garbled glyphs.
- QTY, RATE, and AMOUNT columns remain single-line and numerals only; no Kannada text in those columns.

Visual characteristics:
- Flat scan. No perspective distortion, no shadows.
- Black printed text throughout. No handwriting, no colored ink.
- No imagery of teeth, no decorative border, no clinic advertisement.
- All four page edges visible.
- All numeric values sharp and unambiguous.

Style: bilingual institutional hospital invoice — English for claim processing, Kannada for patient comprehension. OCR must handle both scripts in the same table column.
