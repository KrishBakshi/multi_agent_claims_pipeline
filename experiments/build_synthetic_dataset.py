from __future__ import annotations

import argparse
from pathlib import Path

import cv2

from apply_document_distortions import apply_preset, load_presets_from_spec
from images_to_pdf import image_to_pdf
from render_invoice_from_markdown import render_markdown_file


def build_outputs(
    specs_dir: Path,
    clean_dir: Path,
    distorted_dir: Path,
    clean_pdf_dir: Path,
    distorted_pdf_dir: Path,
) -> None:
    spec_files = sorted(specs_dir.glob("*.md"))
    distorted_dir.mkdir(parents=True, exist_ok=True)
    clean_pdf_dir.mkdir(parents=True, exist_ok=True)
    distorted_pdf_dir.mkdir(parents=True, exist_ok=True)

    for spec_file in spec_files:
        clean_image_path = render_markdown_file(spec_file, clean_dir)
        print(f"Rendered {spec_file.name} -> {clean_image_path.name}")
        image_to_pdf(clean_image_path, clean_pdf_dir)

        presets = load_presets_from_spec(spec_file)
        image = cv2.imread(str(clean_image_path))
        if image is None:
            raise FileNotFoundError(f"Could not read rendered image: {clean_image_path}")

        for preset_name in presets:
            distorted_image = apply_preset(image, preset_name)
            distorted_path = distorted_dir / f"{clean_image_path.stem}_{preset_name}.png"
            cv2.imwrite(str(distorted_path), distorted_image)
            print(f"Distorted {clean_image_path.name} -> {distorted_path.name}")
            image_to_pdf(distorted_path, distorted_pdf_dir)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Render all synthetic invoice specs, generate distortion variants, and convert images to PDFs."
    )
    parser.add_argument("--specs-dir", type=Path, default=Path("data/synthetic_data"))
    parser.add_argument("--clean-dir", type=Path, default=Path("experiments/output/clean"))
    parser.add_argument("--distorted-dir", type=Path, default=Path("experiments/output/distorted"))
    parser.add_argument("--clean-pdf-dir", type=Path, default=Path("experiments/output/clean_pdf"))
    parser.add_argument("--distorted-pdf-dir", type=Path, default=Path("experiments/output/distorted_pdf"))
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    build_outputs(
        specs_dir=args.specs_dir,
        clean_dir=args.clean_dir,
        distorted_dir=args.distorted_dir,
        clean_pdf_dir=args.clean_pdf_dir,
        distorted_pdf_dir=args.distorted_pdf_dir,
    )


if __name__ == "__main__":
    main()
