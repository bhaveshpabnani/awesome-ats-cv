#!/usr/bin/env python3
"""Audit resume content quality: metrics, verbs, weak phrases, sections, and contact."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

try:
    from atscv_utils import fail
except ModuleNotFoundError:  # pragma: no cover - package entry point path
    from .atscv_utils import fail


ACTION_VERBS = {
    "accelerated", "achieved", "analyzed", "architected", "automated", "built", "collaborated", "created",
    "delivered", "designed", "developed", "deployed", "engineered", "evaluated", "implemented", "improved",
    "integrated", "launched", "led", "modeled", "optimized", "orchestrated", "owned", "reduced", "scaled",
    "shipped", "streamlined", "validated", "visualized",
}

WEAK_PHRASES = [
    "worked on", "helped", "responsible for", "various", "multiple", "several", "etc", "stuff", "things",
    "good", "great", "amazing", "many", "some", "basic",
]

STANDARD_SECTIONS = {
    "education", "experience", "work experience", "professional experience", "projects", "skills",
    "technical skills", "certifications", "leadership", "achievements", "publications", "summary",
}

METRIC_RE = re.compile(
    r"(\b\d+(\.\d+)?\s?(%|ms|s|sec|seconds|min|minutes|hrs|hours|x|k|m|gb|mb|tb|records|users|requests|apis|endpoints|repos|services|files|tests|rank|/)\b|\$\s?\d+)",
    re.I,
)


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.in_li = False
        self.bullets: list[str] = []
        self._current: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "li":
            self.in_li = True
            self._current = []

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "li" and self.in_li:
            text = " ".join(" ".join(self._current).split())
            if text:
                self.bullets.append(text)
            self.in_li = False

    def handle_data(self, data: str) -> None:
        clean = " ".join(data.split())
        if not clean:
            return
        self.parts.append(clean)
        if self.in_li:
            self._current.append(clean)


def strip_tex(text: str) -> str:
    text = re.sub(r"\\href\{[^}]*\}\{([^}]*)\}", r"\1", text)
    text = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^]]*\])?", " ", text)
    return text.replace("{", " ").replace("}", " ")


def load_text_and_bullets(path: Path) -> tuple[str, list[str]]:
    raw = path.read_text(encoding="utf-8")
    if path.suffix.lower() in {".html", ".htm"}:
        parser = TextExtractor()
        parser.feed(raw)
        return " ".join(parser.parts), parser.bullets
    text = strip_tex(raw)
    bullets = []
    for line in text.splitlines():
        cleaned = line.strip()
        if re.match(r"^[-*•]\s+", cleaned):
            bullets.append(re.sub(r"^[-*•]\s+", "", cleaned))
        elif re.match(r"^\\item\b", line.strip()):
            bullets.append(re.sub(r"^\\item\s*", "", line.strip()))
    return text, bullets


def audit(path: Path, strict: bool) -> int:
    text, bullets = load_text_and_bullets(path)
    normalized = " ".join(text.lower().split())
    issues: list[str] = []
    warnings: list[str] = []

    if not re.search(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", text):
        issues.append("missing obvious email")
    if not re.search(r"\+?\d[\d\s().-]{7,}\d", text):
        warnings.append("missing obvious phone number")

    found_sections = {section for section in STANDARD_SECTIONS if re.search(rf"\b{re.escape(section)}\b", normalized)}
    for required in ("education", "skills"):
        if required not in found_sections and f"technical {required}" not in found_sections:
            warnings.append(f"missing standard `{required}` section")
    if not ({"experience", "work experience", "professional experience"} & found_sections or "projects" in found_sections):
        warnings.append("missing standard experience/projects section")

    if not bullets:
        warnings.append("no bullet lines detected")
    else:
        metric_hits = sum(1 for bullet in bullets if METRIC_RE.search(bullet))
        action_hits = 0
        first_words: list[str] = []
        for bullet in bullets:
            match = re.match(r"([A-Za-z][A-Za-z-]+)", bullet.strip())
            if match:
                first = match.group(1).lower()
                first_words.append(first)
                if first in ACTION_VERBS:
                    action_hits += 1
            if bullet.rstrip().endswith("."):
                issues.append(f"bullet ends with full stop: {bullet[:90]}")
            for phrase in WEAK_PHRASES:
                if re.search(rf"\b{re.escape(phrase)}\b", bullet.lower()):
                    warnings.append(f"weak phrase `{phrase}` in: {bullet[:90]}")

        metric_ratio = metric_hits / len(bullets)
        action_ratio = action_hits / len(bullets)
        if metric_ratio < 0.35:
            warnings.append(f"low quantified-impact ratio: {metric_hits}/{len(bullets)} bullets include metrics")
        if action_ratio < 0.75:
            warnings.append(f"low recognized-action-verb ratio: {action_hits}/{len(bullets)} bullets start with known action verbs")
        for verb, count in Counter(first_words).items():
            if count > 2:
                warnings.append(f"repeated opening verb `{verb}` appears {count} times")

    if not re.search(r"github|gitlab|bitbucket|portfolio|linkedin", normalized):
        warnings.append("missing obvious GitHub/LinkedIn/portfolio signal")

    print(f"Resume content audit for {path}")
    print(f"- bullets: {len(bullets)}")
    if bullets:
        print(f"- metric bullets: {sum(1 for bullet in bullets if METRIC_RE.search(bullet))}/{len(bullets)}")
    if issues:
        print("Issues:")
        for issue in issues:
            print(f"- {issue}")
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"- {warning}")
    if not issues and not warnings:
        print("No obvious content issues found")
    return 1 if issues or (strict and warnings) else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Resume source as HTML, text, Markdown, LaTeX, or extracted PDF text")
    parser.add_argument("--strict", action="store_true", help="Return non-zero for warnings as well as issues")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if not args.source.exists():
        return fail(f"source not found: {args.source}")
    return audit(args.source, args.strict)


if __name__ == "__main__":
    raise SystemExit(main())
