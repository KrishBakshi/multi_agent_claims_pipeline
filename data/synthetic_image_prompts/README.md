# Synthetic Image Prompt Templates

This directory is separate from `data/synthetic_data`.

- `data/synthetic_data`: structured source specs intended for local scripts and OpenCV-based rendering.
- `data/synthetic_image_prompts`: precise prompt sheets intended for image generation models such as Nano Banana or ChatGPT image models.

Each prompt file contains:

- a strict objective
- a field checklist that must appear in the generated invoice
- composition and styling constraints
- negative constraints to avoid decorative or non-document artifacts
- an optional PDF-like variant prompt

Use these files directly with image generation systems. Do not parse them with the renderer script.
