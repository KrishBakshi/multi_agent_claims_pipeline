# Synthetic Invoice Experiments

This folder contains lightweight utilities for turning the structured markdown specs in `data/synthetic_data` into image-ready invoices and OCR stress-test variants.

## Files

- `render_invoice_from_markdown.py`: reads one markdown spec or a whole directory, extracts the `invoice_spec` JSON block, and renders a clean invoice PNG using OpenCV.
- `apply_document_distortions.py`: applies blur, skew, noise, JPEG compression, shadow, and grayscale presets to a rendered invoice image.
- `images_to_pdf.py`: converts rendered PNG/JPG invoice images into one-page PDFs using PyMuPDF.
- `build_synthetic_dataset.py`: batch pipeline that renders every synthetic spec, generates all listed distortion variants, and converts both clean and distorted images into PDFs.

## Usage

Render every synthetic document:

```bash
python experiments/render_invoice_from_markdown.py \
  --input-dir data/synthetic_data \
  --output-dir experiments/output/clean
```

Render a single document:

```bash
python experiments/render_invoice_from_markdown.py \
  --input-file data/synthetic_data/01_consultation_apollo_rajesh.md \
  --output-dir experiments/output/clean
```

Apply distortion presets to one image:

```bash
python experiments/apply_document_distortions.py \
  --input experiments/output/clean/01_consultation_apollo_rajesh.png \
  --output-dir experiments/output/distorted \
  --presets mild_blur phone_photo grayscale_scan
```

Use presets from the markdown spec:

```bash
python experiments/apply_document_distortions.py \
  --input experiments/output/clean/01_consultation_apollo_rajesh.png \
  --spec-file data/synthetic_data/01_consultation_apollo_rajesh.md \
  --output-dir experiments/output/distorted
```

Convert a directory of generated images into PDFs:

```bash
python experiments/images_to_pdf.py \
  --input-dir experiments/output/clean \
  --output-dir experiments/output/clean_pdf
```

Run the full synthetic build pipeline:

```bash
python experiments/build_synthetic_dataset.py
```

## Notes

- The renderer stays intentionally plain: black text, ruled tables, and fixed positioning so it is easy to modify for OpenCV paste/composite workflows.
- Image-model prompt templates now live separately in `data/synthetic_image_prompts`.
- Keep `data/synthetic_data` for script-driven rendering and `data/synthetic_image_prompts` for Nano Banana / ChatGPT image generation.
- All entity values are grounded in `config/policy_terms.json` and the layout conventions in `data/sample_documents_guide.md`.
