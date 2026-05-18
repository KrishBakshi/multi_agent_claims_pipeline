from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import cv2
import numpy as np


BLOCK_PATTERN = r"```{label}\n(.*?)\n```"


def extract_json_block(markdown_text: str, label: str) -> dict:
    match = re.search(BLOCK_PATTERN.format(label=re.escape(label)), markdown_text, re.DOTALL)
    if not match:
        raise ValueError(f"Could not find fenced block '{label}'")
    return json.loads(match.group(1))


def money(value: float) -> str:
    return f"{value:.2f}"


def draw_text(image: np.ndarray, text: str, x: int, y: int, scale: float = 0.8, thickness: int = 1) -> None:
    cv2.putText(
        image,
        text,
        (x, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        scale,
        (0, 0, 0),
        thickness,
        cv2.LINE_AA,
    )


def render_invoice(spec: dict) -> np.ndarray:
    layout = spec["layout"]
    width = layout["canvas"]["width"]
    height = layout["canvas"]["height"]
    margin = layout["canvas"]["margin"]
    row_height = layout["table"]["row_height"]
    top = layout["table"]["top_y"]

    image = np.full((height, width, 3), 255, dtype=np.uint8)
    cv2.rectangle(image, (margin, margin), (width - margin, height - margin), (0, 0, 0), 2)

    provider = spec["provider"]
    patient = spec["patient"]
    bill = spec["bill"]
    totals = spec["totals"]
    payment = spec["payment"]
    columns = layout["table"]["columns"]
    line_items = spec["line_items"]

    draw_text(image, provider["name"].upper(), margin + 20, margin + 45, scale=1.0, thickness=2)
    draw_text(image, provider["address"], margin + 20, margin + 82, scale=0.65)
    draw_text(image, provider["meta_line"], margin + 20, margin + 114, scale=0.6)
    cv2.line(image, (margin, margin + 135), (width - margin, margin + 135), (0, 0, 0), 1)

    draw_text(image, bill["title"], margin + 20, margin + 185, scale=0.85, thickness=2)
    draw_text(image, f"Bill No: {bill['bill_no']}", margin + 20, margin + 225, scale=0.7)
    draw_text(image, f"Date: {bill['date']}", width - 360, margin + 225, scale=0.7)
    draw_text(image, f"Claim Category: {spec['claim_category']}", margin + 20, margin + 260, scale=0.62)
    draw_text(image, f"Policy Ref: {spec['policy_context']['policy_id']}", width - 420, margin + 260, scale=0.62)
    cv2.line(image, (margin, margin + 285), (width - margin, margin + 285), (0, 0, 0), 1)

    draw_text(image, f"Patient Name: {patient['name']}", margin + 20, margin + 335, scale=0.7)
    draw_text(image, f"Member ID: {patient['member_id']}", width - 360, margin + 335, scale=0.65)
    draw_text(image, f"Age/Gender: {patient['age']} / {patient['gender_display']}", margin + 20, margin + 372, scale=0.65)
    draw_text(image, f"Relationship: {patient['relationship']}", width - 360, margin + 372, scale=0.65)
    draw_text(image, f"Referring Doctor: {spec['doctor']['name']}", margin + 20, margin + 409, scale=0.65)
    draw_text(image, f"Doctor Reg No: {spec['doctor']['registration']}", width - 430, margin + 409, scale=0.6)
    cv2.line(image, (margin, margin + 440), (width - margin, margin + 440), (0, 0, 0), 1)

    table_left = margin + 20
    table_right = width - margin - 20
    table_bottom = top + row_height * (len(line_items) + 1) + 8
    cv2.rectangle(image, (table_left, top - 40), (table_right, table_bottom), (0, 0, 0), 1)

    for column in columns:
        draw_text(image, column["label"], column["x"], top - 12, scale=0.62, thickness=2)

    for index, item in enumerate(line_items):
        y = top + row_height * index + 20
        cv2.line(image, (table_left, top + row_height * (index + 1)), (table_right, top + row_height * (index + 1)), (220, 220, 220), 1)
        draw_text(image, item["description"], columns[0]["x"], y, scale=0.58)
        draw_text(image, str(item["qty"]), columns[1]["x"], y, scale=0.58)
        draw_text(image, money(item["rate"]), columns[2]["x"], y, scale=0.58)
        draw_text(image, money(item["amount"]), columns[3]["x"], y, scale=0.58)

    totals_y = table_bottom + 55
    draw_text(image, f"Subtotal: {money(totals['subtotal'])}", width - 360, totals_y, scale=0.7)
    draw_text(image, f"Discount: {money(totals['discount'])}", width - 360, totals_y + 36, scale=0.7)
    draw_text(image, f"GST: {money(totals['gst'])}", width - 360, totals_y + 72, scale=0.7)
    draw_text(image, f"Total Amount: {money(totals['total'])}", width - 420, totals_y + 118, scale=0.82, thickness=2)

    footer_y = height - margin - 180
    cv2.line(image, (margin, footer_y - 20), (width - margin, footer_y - 20), (0, 0, 0), 1)
    draw_text(image, f"Payment Mode: {payment['mode']}", margin + 20, footer_y + 20, scale=0.65)
    draw_text(image, f"Received By: {payment['received_by']}", margin + 20, footer_y + 58, scale=0.65)
    draw_text(image, f"Notes: {spec['notes']}", margin + 20, footer_y + 96, scale=0.58)
    draw_text(image, payment["stamp_text"], width - 300, footer_y + 58, scale=0.65, thickness=2)

    return image


def render_markdown_file(markdown_path: Path, output_dir: Path) -> Path:
    text = markdown_path.read_text(encoding="utf-8")
    spec = extract_json_block(text, "invoice_spec")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{spec['document_id']}.png"
    image = render_invoice(spec)
    cv2.imwrite(str(output_path), image)
    return output_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render synthetic invoice PNGs from markdown specs.")
    parser.add_argument("--input-file", type=Path, help="Single markdown spec file.")
    parser.add_argument("--input-dir", type=Path, help="Directory containing markdown specs.")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory for rendered PNG files.")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not args.input_file and not args.input_dir:
        parser.error("Provide either --input-file or --input-dir")

    files: list[Path] = []
    if args.input_file:
        files.append(args.input_file)
    if args.input_dir:
        files.extend(sorted(args.input_dir.glob("*.md")))

    for markdown_path in files:
        output_path = render_markdown_file(markdown_path, args.output_dir)
        print(f"Rendered {markdown_path} -> {output_path}")


if __name__ == "__main__":
    main()
