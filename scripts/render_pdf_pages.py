#!/usr/bin/env python3
"""Render PDF pages to PNG for visual QA and page-coverage checks."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from atscv_utils import fail, find_poppler_tool


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path, help="Input PDF file")
    parser.add_argument("output_dir", type=Path, help="Directory for rendered PNG files")
    parser.add_argument("--dpi", type=int, default=180, help="Render DPI, default: 180")
    parser.add_argument("--prefix", default="page", help="Output prefix, default: page")
    parser.add_argument("--pdftoppm", type=Path, help="Path to Poppler pdftoppm")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    pdf = args.pdf.resolve()
    if not pdf.exists():
        return fail(f"PDF file not found: {pdf}")

    pdftoppm = str(args.pdftoppm) if args.pdftoppm else find_poppler_tool("pdftoppm")
    if not pdftoppm:
        return fail("Poppler pdftoppm not found. Install poppler-utils or set ATS_CV_PDFTOPPM")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for old_page in args.output_dir.glob(f"{args.prefix}-*.png"):
        old_page.unlink()
    prefix = args.output_dir / args.prefix
    command = [pdftoppm, "-png", "-r", str(args.dpi), str(pdf), str(prefix)]
    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        return result.returncode

    pages = sorted(args.output_dir.glob(f"{args.prefix}-*.png"))
    print(f"rendered {len(pages)} page(s) to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
