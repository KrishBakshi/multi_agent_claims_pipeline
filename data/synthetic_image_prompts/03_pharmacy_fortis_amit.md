# Image Prompt 03 — Fortis Pharmacy Bill, Amit Verma
# Edge Scenario: Rubber stamp over text — pharmacist stamp obscuring doctor registration number

## Real-World Context

The Fortis Healthcare pharmacy issued Amit Verma's bill at the counter. Before handing it over, the pharmacist pressed the official pharmacy rubber stamp firmly onto the document — a standard procedure for authentication. The stamp landed awkwardly, with the bottom arc of the circular stamp landing directly over the "Doctor Reg No: KA/45678/2015" line in the patient section, partially obscuring those characters. This is the "rubber stamp over text" scenario from the guide: the registration number or amounts may be partially obscured, and should be flagged as LOW confidence fields.

## Image Generation Prompt

Generate a flat scan of an Indian hospital pharmacy bill on white A4 paper. The document is printed in black text, clean and straight. A circular rubber stamp in dark blue ink has been applied to the document, landing in the patient/doctor section area on the right side. The stamp partially overlaps the doctor registration number field, making some characters of "KA/45678/2015" difficult to read through the ink.

Document type: pharmacy bill.
Provider name: Fortis Healthcare.
Provider address: 77 Bannerghatta Main Road, Bengaluru - 560076.
Header metadata line: Drug Lic. No: KA-BLR-48291 | Ph: 080-66214444 | Network Pharmacy Desk.
Title text: PHARMACY BILL.
Bill number: FOR/PH/2024/11803.
Bill date: 2024-12-03.
Patient name: Amit Verma.
Patient age and gender: 35 / Male.
Member ID: EMP003.
Relationship: SELF.
Prescribing doctor: Dr. Arun Sharma.
Doctor registration: KA/45678/2015.

Medicine table — column headers: MEDICINE, QTY, MRP, AMOUNT — exactly four rows:
- Azithromycin 500 mg Tablets | 3 | 62.00 | 186.00
- Levocetirizine Tablets | 10 | 4.50 | 45.00
- Pantoprazole 40 mg Tablets | 10 | 6.50 | 65.00
- Cough Syrup 100 ml | 1 | 118.00 | 118.00

Totals:
- Subtotal: 414.00
- Discount: 14.00
- GST: 0.00
- Total Amount: 400.00

Footer:
- Payment Mode: Cash
- Received By: R. D'Souza
- Stamp placeholder: [PHARMACIST STAMP]

Rubber stamp details — render with precision:
- Circular stamp, approximately 4 cm diameter, dark blue ink.
- Stamp text around the outer rim reads: "FORTIS HEALTHCARE PHARMACY".
- Center of the stamp reads: "PHARMACIST SEAL".
- Stamp position: right-center of the patient/doctor information section, the bottom arc of the circle landing directly over the "Doctor Reg No: KA/45678/2015" line.
- The characters "KA/45678" are partially covered by ink — legible with effort but the last four digits "/2015" are clearer.
- Stamp ink coverage is uneven: the upper arc of the circle is solid and dark, the lower arc is slightly lighter where the stamp pressure was less even.
- A faint ink bleed halo of 1–2 pixels around the stamp perimeter from ink spreading on the paper.
- All other document fields — patient name, medicine table, totals, footer — are fully printed and unobscured.

Visual characteristics:
- Flat institutional scan. No perspective, no shadow.
- Black printed text on white paper except for the blue rubber stamp.
- No handwriting anywhere else on the document.
- No extra stamps, no torn edges, no color backgrounds.

Style: pharmacy counter authentication copy — authentic Indian pharmacy document with standard post-print stamping.
