from __future__ import annotations

import argparse
import json
import random
import re
from pathlib import Path

import cv2
import numpy as np


BLOCK_PATTERN = r"```{label}\n(.*?)\n```"


def extract_json_block(markdown_text: str, label: str) -> dict | list:
    match = re.search(BLOCK_PATTERN.format(label=re.escape(label)), markdown_text, re.DOTALL)
    if not match:
        raise ValueError(f"Could not find fenced block '{label}'")
    return json.loads(match.group(1))


def add_gaussian_noise(image: np.ndarray, sigma: float = 8.0) -> np.ndarray:
    noise = np.random.normal(0, sigma, image.shape).astype(np.float32)
    noisy = image.astype(np.float32) + noise
    return np.clip(noisy, 0, 255).astype(np.uint8)


def adjust_jpeg_quality(image: np.ndarray, quality: int) -> np.ndarray:
    success, encoded = cv2.imencode(".jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
    if not success:
        raise RuntimeError("JPEG encoding failed")
    decoded = cv2.imdecode(encoded, cv2.IMREAD_COLOR)
    if decoded is None:
        raise RuntimeError("JPEG decoding failed")
    return decoded


def apply_shadow(image: np.ndarray) -> np.ndarray:
    height, width = image.shape[:2]
    overlay = image.copy().astype(np.float32)
    gradient = np.tile(np.linspace(0.65, 1.0, width, dtype=np.float32), (height, 1))
    overlay[:, :, 0] *= gradient
    overlay[:, :, 1] *= gradient
    overlay[:, :, 2] *= gradient
    return np.clip(overlay, 0, 255).astype(np.uint8)


def apply_skew(image: np.ndarray, magnitude: float = 0.05) -> np.ndarray:
    height, width = image.shape[:2]
    shift = int(width * magnitude)
    src = np.float32([[0, 0], [width - 1, 0], [0, height - 1], [width - 1, height - 1]])
    dst = np.float32([[shift, 0], [width - 1, 20], [0, height - 1], [width - shift - 1, height - 20]])
    matrix = cv2.getPerspectiveTransform(src, dst)
    return cv2.warpPerspective(image, matrix, (width, height), borderValue=(255, 255, 255))


def apply_preset(image: np.ndarray, preset_name: str) -> np.ndarray:
    if preset_name == "mild_blur":
        return cv2.GaussianBlur(image, (5, 5), 0)
    if preset_name == "strong_blur":
        return cv2.GaussianBlur(image, (11, 11), 0)
    if preset_name == "phone_photo":
        result = apply_skew(image, magnitude=0.04)
        result = add_gaussian_noise(result, sigma=6.0)
        return apply_shadow(result)
    if preset_name == "grayscale_scan":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    if preset_name == "jpeg_low_quality":
        return adjust_jpeg_quality(image, quality=35)
    if preset_name == "noisy_scan":
        return add_gaussian_noise(image, sigma=12.0)
    raise ValueError(f"Unsupported preset: {preset_name}")


def load_presets_from_spec(spec_file: Path) -> list[str]:
    text = spec_file.read_text(encoding="utf-8")
    presets = extract_json_block(text, "distortion_presets")
    return [preset["name"] for preset in presets]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Apply OCR-style distortions to rendered invoice images.")
    parser.add_argument("--input", type=Path, required=True, help="Input PNG/JPG invoice image.")
    parser.add_argument("--output-dir", type=Path, required=True, help="Output directory.")
    parser.add_argument("--presets", nargs="*", help="Explicit distortion preset names.")
    parser.add_argument("--spec-file", type=Path, help="Optional markdown spec file to read preset names from.")
    parser.add_argument("--seed", type=int, default=7, help="Random seed for reproducible noise.")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    random.seed(args.seed)
    np.random.seed(args.seed)

    image = cv2.imread(str(args.input))
    if image is None:
        raise FileNotFoundError(f"Could not read image: {args.input}")

    presets = args.presets or []
    if args.spec_file and not presets:
        presets = load_presets_from_spec(args.spec_file)
    if not presets:
        parser.error("Provide --presets or --spec-file")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for preset_name in presets:
        output = apply_preset(image, preset_name)
        output_path = args.output_dir / f"{args.input.stem}_{preset_name}.png"
        cv2.imwrite(str(output_path), output)
        print(f"Created {output_path}")


if __name__ == "__main__":
    main()
