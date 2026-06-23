#!/usr/bin/env python3
"""End-to-end ATS CV validation for HTML/PDF/text resume artifacts."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

try:
    from atscv_utils import fail
except ModuleNotFoundError:  # pragma: no cover - package entry point path
    from .atscv_utils import fail


SCRIPT_DIR = Path(__file__).resolve().parent


def run(command: list[str], required: bool = True) -> int:
    print("+ " + " ".join(str(part) for part in command))
    result = subprocess.run(command, text=True)
    if required and result.returncode != 0:
        raise SystemExit(result.returncode)
    return result.returncode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="HTML, PDF, TXT, MD, or TeX resume source")
    parser.add_argument("--workdir", type=Path, default=Path("atscv-validation"), help="Validation output directory")
    parser.add_argument("--min-width", type=float, default=0.90)
    parser.add_argument("--max-width", type=float, default=0.98)
    parser.add_argument("--max-bottom-mm", type=float, default=14.0)
    parser.add_argument("--dpi", type=int, default=180)
    parser.add_argument("--grammar-provider", choices=["offline", "languagetool", "manual", "skip"], default="offline")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    source = args.source.resolve()
    if not source.exists():
        return fail(f"source not found: {source}")
    args.workdir.mkdir(parents=True, exist_ok=True)

    suffix = source.suffix.lower()
    pdf = source

    if suffix in {".txt", ".md", ".tex"}:
        run([sys.executable, str(SCRIPT_DIR / "lint_cv_text.py"), str(source)], required=False)
        run([sys.executable, str(SCRIPT_DIR / "audit_resume_content.py"), str(source)], required=False)
        run([sys.executable, str(SCRIPT_DIR / "check_grammar.py"), str(source), "--provider", args.grammar_provider], required=False)

    if suffix in {".html", ".htm"}:
        run([sys.executable, str(SCRIPT_DIR / "audit_ats_structure.py"), str(source)])
        run([sys.executable, str(SCRIPT_DIR / "audit_resume_content.py"), str(source)], required=False)
        run([sys.executable, str(SCRIPT_DIR / "check_grammar.py"), str(source), "--provider", args.grammar_provider], required=False)
        run(
            [
                sys.executable,
                str(SCRIPT_DIR / "measure_bullet_widths.py"),
                str(source),
                "--min",
                str(args.min_width),
                "--max",
                str(args.max_width),
            ]
        )
        pdf = args.workdir / (source.stem + ".pdf")
        run([sys.executable, str(SCRIPT_DIR / "html_to_pdf.py"), str(source), str(pdf)])

    if pdf.suffix.lower() == ".pdf":
        rendered = args.workdir / "rendered"
        run([sys.executable, str(SCRIPT_DIR / "render_pdf_pages.py"), str(pdf), str(rendered), "--dpi", str(args.dpi)])
        pages = sorted(str(path) for path in rendered.glob("page-*.png"))
        if pages:
            run(
                [
                    sys.executable,
                    str(SCRIPT_DIR / "measure_page_coverage.py"),
                    *pages,
                    "--dpi",
                    str(args.dpi),
                    "--max-bottom-mm",
                    str(args.max_bottom_mm),
                ]
            )
        extracted = args.workdir / "extracted.txt"
        run([sys.executable, str(SCRIPT_DIR / "extract_pdf_text.py"), str(pdf), "--out", str(extracted)], required=False)
        if extracted.exists():
            run([sys.executable, str(SCRIPT_DIR / "audit_resume_content.py"), str(extracted)], required=False)
            run([sys.executable, str(SCRIPT_DIR / "check_grammar.py"), str(extracted), "--provider", args.grammar_provider], required=False)

    print("ATS CV validation complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
