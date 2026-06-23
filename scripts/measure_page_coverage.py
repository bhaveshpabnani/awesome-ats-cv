#!/usr/bin/env python3
"""Measure ink coverage, margins, and bottom whitespace from rendered CV images."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from atscv_utils import fail


def load_pillow():
    try:
        from PIL import Image
    except Exception as exc:  # pragma: no cover - environment dependent
        raise RuntimeError("Pillow is required: python -m pip install pillow") from exc
    return Image


def analyze_image(path: Path, dpi: int, threshold: int) -> dict[str, float | int | str]:
    Image = load_pillow()
    image = Image.open(path).convert("RGB")
    width, height = image.size
    xs: list[int] = []
    ys: list[int] = []
    ink_pixels = 0

    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))
            if min(r, g, b) < threshold:
                ink_pixels += 1
                xs.append(x)
                ys.append(y)

    if not xs:
        return {
            "file": str(path),
            "width_px": width,
            "height_px": height,
            "ink_coverage": 0,
            "bottom_whitespace_px": height,
            "bottom_whitespace_mm": round(height / dpi * 25.4, 2),
        }

    left, right = min(xs), max(xs)
    top, bottom = min(ys), max(ys)
    return {
        "file": str(path),
        "width_px": width,
        "height_px": height,
        "ink_coverage": round(ink_pixels / (width * height), 5),
        "content_left_px": left,
        "content_right_px": right,
        "content_top_px": top,
        "content_bottom_px": bottom,
        "bottom_whitespace_px": height - bottom - 1,
        "bottom_whitespace_mm": round((height - bottom - 1) / dpi * 25.4, 2),
        "left_margin_mm": round(left / dpi * 25.4, 2),
        "right_margin_mm": round((width - right - 1) / dpi * 25.4, 2),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("images", nargs="+", type=Path, help="Rendered page PNG/JPEG files")
    parser.add_argument("--dpi", type=int, default=180, help="Render DPI used for images")
    parser.add_argument("--threshold", type=int, default=245, help="Pixel darkness threshold")
    parser.add_argument("--max-bottom-mm", type=float, default=None, help="Fail if bottom whitespace exceeds this")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    missing = [str(path) for path in args.images if not path.exists()]
    if missing:
        return fail("image file(s) not found: " + ", ".join(missing))

    results = [analyze_image(path, args.dpi, args.threshold) for path in args.images]
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for result in results:
            print(
                f"{result['file']}: bottom={result['bottom_whitespace_mm']}mm, "
                f"coverage={result['ink_coverage']}, "
                f"left={result.get('left_margin_mm', 'n/a')}mm, "
                f"right={result.get('right_margin_mm', 'n/a')}mm"
            )

    if args.max_bottom_mm is not None:
        offenders = [r for r in results if float(r["bottom_whitespace_mm"]) > args.max_bottom_mm]
        if offenders:
            for offender in offenders:
                print(
                    f"bottom whitespace too large: {offender['file']} "
                    f"{offender['bottom_whitespace_mm']}mm > {args.max_bottom_mm}mm"
                )
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

