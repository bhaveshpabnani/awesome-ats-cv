#!/usr/bin/env python3
"""Extract PDF text for ATS order checks."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from atscv_utils import ensure_parent, fail, find_poppler_tool


def extract_with_pypdf(pdf: Path) -> str | None:
    try:
        from pypdf import PdfReader
    except Exception:
        return None
    reader = PdfReader(str(pdf))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def extract_with_pdftotext(pdf: Path) -> str | None:
    pdftotext = find_poppler_tool("pdftotext")
    if not pdftotext:
        return None
    result = subprocess.run([pdftotext, "-layout", str(pdf), "-"], text=True, capture_output=True)
    if result.returncode != 0:
        return None
    return result.stdout


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path, help="Input PDF file")
    parser.add_argument("--out", type=Path, help="Optional text output file")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    pdf = args.pdf.resolve()
    if not pdf.exists():
        return fail(f"PDF file not found: {pdf}")

    text = extract_with_pdftotext(pdf) or extract_with_pypdf(pdf)
    if text is None:
        return fail("No PDF text extractor available. Install poppler-utils or pypdf")

    if args.out:
        ensure_parent(args.out)
        args.out.write_text(text, encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

