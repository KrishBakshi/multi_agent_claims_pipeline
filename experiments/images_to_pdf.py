from __future__ import annotations

import argparse
from pathlib import Path

import fitz


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg"}


def iter_images(input_file: Path | None, input_dir: Path | None) -> list[Path]:
    if input_file:
        return [input_file]
    if input_dir:
        return sorted(path for path in input_dir.iterdir() if path.suffix.lower() in IMAGE_EXTENSIONS)
    raise ValueError("Provide either --input-file or --input-dir")


def image_to_pdf(image_path: Path, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{image_path.stem}.pdf"

    pixmap = fitz.Pixmap(str(image_path))
    with fitz.open() as document:
        page = document.new_page(width=pixmap.width, height=pixmap.height)
        page.insert_image(page.rect, filename=str(image_path))
        document.save(output_path)

    return output_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Convert invoice images to one-page PDFs using PyMuPDF.")
    parser.add_argument("--input-file", type=Path, help="Single image file to convert.")
    parser.add_argument("--input-dir", type=Path, help="Directory containing PNG/JPG images.")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory for output PDF files.")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    images = iter_images(args.input_file, args.input_dir)

    for image_path in images:
        pdf_path = image_to_pdf(image_path, args.output_dir)
        print(f"Converted {image_path} -> {pdf_path}")


if __name__ == "__main__":
    main()
