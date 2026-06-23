#!/usr/bin/env python3
"""Audit HTML resume structure for common ATS parsing risks."""

from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

try:
    from atscv_utils import fail
except ModuleNotFoundError:  # pragma: no cover - package entry point path
    from .atscv_utils import fail


STANDARD_HEADINGS = {
    "summary",
    "professional summary",
    "education",
    "work experience",
    "experience",
    "professional experience",
    "projects",
    "selected projects",
    "skills",
    "technical skills",
    "certifications",
    "leadership",
    "achievements",
    "publications",
    "research experience",
    "awards",
}

RISKY_TAGS = {"table", "thead", "tbody", "tfoot", "tr", "td", "th", "img", "svg", "canvas", "header", "footer", "aside"}
RISKY_STYLE_PATTERNS = {
    "absolute positioning": re.compile(r"position\s*:\s*(absolute|fixed)", re.I),
    "css columns": re.compile(r"(column-count|columns)\s*:", re.I),
    "css grid": re.compile(r"display\s*:\s*grid|grid-template", re.I),
    "text box like overflow": re.compile(r"overflow\s*:\s*(hidden|scroll)", re.I),
}


class ResumeHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[tuple[str, int]] = []
        self.risky_styles: list[tuple[str, str, int]] = []
        self.heading_stack: list[str] = []
        self.headings: list[tuple[str, int]] = []
        self.links: list[tuple[str, int]] = []
        self.text_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        line = self.getpos()[0]
        self.tags.append((tag.lower(), line))
        attrs_map = {key.lower(): value or "" for key, value in attrs}
        style = attrs_map.get("style", "")
        for label, pattern in RISKY_STYLE_PATTERNS.items():
            if pattern.search(style):
                self.risky_styles.append((label, tag.lower(), line))
        if tag.lower() in {"h2", "h3"}:
            self.heading_stack.append(tag.lower())
        if tag.lower() == "a":
            self.links.append((attrs_map.get("href", ""), line))

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"h2", "h3"} and self.heading_stack:
            self.heading_stack.pop()

    def handle_data(self, data: str) -> None:
        clean = " ".join(data.split())
        if not clean:
            return
        self.text_parts.append(clean)
        if self.heading_stack:
            self.headings.append((clean, self.getpos()[0]))


def audit(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    parser = ResumeHTMLParser()
    parser.feed(text)
    issues: list[str] = []
    warnings: list[str] = []

    for tag, line in parser.tags:
        if tag in RISKY_TAGS:
            issues.append(f"{line}: avoid <{tag}> in ATS-first templates")

    for label, tag, line in parser.risky_styles:
        warnings.append(f"{line}: {label} on <{tag}> can hurt parsing or text extraction")

    heading_texts = [heading.strip().lower() for heading, _ in parser.headings]
    if not any(heading in heading_texts for heading in {"experience", "work experience", "professional experience"}):
        warnings.append("missing standard experience heading")
    if not any(heading in heading_texts for heading in {"education"}):
        warnings.append("missing standard education heading")
    if not any(heading in heading_texts for heading in {"skills", "technical skills"}):
        warnings.append("missing standard skills heading")

    for heading, line in parser.headings:
        normalized = heading.strip().lower()
        if normalized and normalized not in STANDARD_HEADINGS and len(normalized.split()) <= 4:
            warnings.append(f"{line}: non-standard heading `{heading}` may parse less reliably")

    body_text = " ".join(parser.text_parts)
    if not re.search(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", body_text):
        warnings.append("missing obvious email in main document text")
    if not re.search(r"(\+?\d[\d\s().-]{7,}\d)", body_text):
        warnings.append("missing obvious phone number in main document text")

    for href, line in parser.links:
        if href and not re.match(r"^(https?:|mailto:|tel:)", href):
            warnings.append(f"{line}: link `{href}` is not an absolute web, mail, or phone URL")

    if issues:
        print(f"ATS structure audit failed for {path}:")
        for issue in issues:
            print(f"- {issue}")
    else:
        print(f"ATS structure audit passed for {path}: no blocking structure risks found")

    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"- {warning}")

    return 1 if issues else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path, help="HTML resume file")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if not args.html.exists():
        return fail(f"HTML file not found: {args.html}")
    return audit(args.html)


if __name__ == "__main__":
    raise SystemExit(main())
