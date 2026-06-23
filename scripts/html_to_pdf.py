#!/usr/bin/env python3
"""Convert an HTML resume to PDF with a local Chromium-family browser."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

try:
    from atscv_utils import ensure_parent, fail, find_chromium, path_to_file_url
except ModuleNotFoundError:  # pragma: no cover - package entry point path
    from .atscv_utils import ensure_parent, fail, find_chromium, path_to_file_url


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path, help="Input HTML file")
    parser.add_argument("pdf", type=Path, help="Output PDF file")
    parser.add_argument("--browser", type=Path, help="Chrome/Chromium/Edge executable")
    parser.add_argument("--with-header-footer", action="store_true", help="Keep browser print headers/footers")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    html = args.html.resolve()
    pdf = args.pdf.resolve()
    if not html.exists():
        return fail(f"HTML file not found: {html}")

    browser = str(args.browser) if args.browser else find_chromium()
    if not browser:
        return fail("Chrome/Chromium/Edge not found. Set ATS_CV_CHROME or pass --browser")

    ensure_parent(pdf)
    command = [
        browser,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        f"--print-to-pdf={pdf}",
    ]
    if not args.with_header_footer:
        command.append("--print-to-pdf-no-header")
    command.append(path_to_file_url(html))

    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        return result.returncode
    print(f"wrote {pdf}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
