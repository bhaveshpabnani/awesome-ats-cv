#!/usr/bin/env python3
"""Lightweight CV text/LaTeX hygiene checks for ATS CV Crafter."""

from __future__ import annotations

import re
import argparse
import sys
from collections import Counter
from pathlib import Path


ACTION_LINE = re.compile(r"^\s*(?:\\item\s*\{?|[-*•]\s+)([A-Za-z][A-Za-z-]+)")
MONTH_RANGE = re.compile(
    r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sept|Sep|Oct|Nov|Dec) \d{4} - "
    r"(?:(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sept|Sep|Oct|Nov|Dec) \d{4}|Present)\b"
)


def strip_tex(line: str) -> str:
    line = re.sub(r"\\href\{[^}]*\}\{([^}]*)\}", r"\1", line)
    line = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^]]*\])?", "", line)
    line = line.replace("{", "").replace("}", "")
    return line.strip()


def lint(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    issues: list[str] = []
    verbs: list[str] = []

    for idx, raw in enumerate(lines, 1):
        line = strip_tex(raw)
        if not line:
            continue

        if re.search(r" {2,}", line):
            issues.append(f"{idx}: multiple consecutive spaces")
        if re.search(r"\s+,", line) or re.search(r",[^\s)\]}0-9]", line):
            issues.append(f"{idx}: comma spacing issue")
        if re.search(r"\s+:", line) or re.search(r":[^\s)\]}0-9]", line):
            issues.append(f"{idx}: colon spacing issue")
        if re.search(r"\s+/", line) or re.search(r"/\s+", line):
            issues.append(f"{idx}: slash spacing issue")
        if re.search(r"\(\s|\[\s|\{\s", raw) or re.search(r"\s\)|\s\]|\s\}", raw):
            issues.append(f"{idx}: bracket spacing issue")
        if "|" in line and not re.search(r" \| ", line):
            issues.append(f"{idx}: pipe spacing issue")

        bullet = re.match(r"^\s*(?:\\item|[-*•])", raw)
        if bullet:
            clean = line.rstrip()
            if clean.endswith("."):
                issues.append(f"{idx}: bullet ends with full stop")
            if re.match(r"^\s*[-*•]\S", raw):
                issues.append(f"{idx}: missing space after bullet marker")
            match = ACTION_LINE.match(raw)
            if match:
                verbs.append(match.group(1).lower())

    text_plain = "\n".join(strip_tex(line) for line in lines)
    for bad in re.findall(r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sept|Sep|Oct|Nov|Dec)' ?\d{2,4}\b", text_plain):
        issues.append(f"date style: avoid compact quote date `{bad}` unless explicitly requested")
    for bad in re.findall(r"\b\d{2}/\d{4}\b", text_plain):
        issues.append(f"date style: numeric date `{bad}` is ATS-safe only when the platform asks for MM/YYYY")

    month_like = re.findall(r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sept|Sep|Oct|Nov|Dec)\.?\s*'?\s*\d{2,4}\s*[-–—]\s*(?:Present|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sept|Sep|Oct|Nov|Dec)\.?\s*'?\s*\d{2,4})", text_plain)
    for candidate in month_like:
        normalized = candidate.replace(".", "")
        if not MONTH_RANGE.search(normalized):
            issues.append(f"date style: prefer `Apr 2021 - Jul 2021`, found `{candidate}`")

    repeated = [verb for verb, count in Counter(verbs).items() if count > 2]
    for verb in repeated:
        issues.append(f"action verbs: `{verb}` starts {Counter(verbs)[verb]} bullets")

    if issues:
        print(f"CV lint found issues in {path}:")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print(f"CV lint passed for {path}: no obvious style issues found")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="One or more CV text, Markdown, or LaTeX files")
    args = parser.parse_args()

    exit_code = 0
    for path in args.paths:
        if not path.exists():
            print(f"File not found: {path}", file=sys.stderr)
            exit_code = 2
            continue
        exit_code = max(exit_code, lint(path))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
