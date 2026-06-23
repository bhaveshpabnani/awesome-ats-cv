#!/usr/bin/env python3
"""Extract ATS keyword candidates from a job description and compare resume coverage."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

try:
    from atscv_utils import fail
except ModuleNotFoundError:  # pragma: no cover - package entry point path
    from .atscv_utils import fail


STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "can", "for", "from", "in", "into", "is", "it", "of", "on",
    "or", "our", "the", "their", "this", "to", "with", "you", "your", "we", "will", "work", "working", "role",
    "team", "teams", "company", "including", "such", "like", "within", "across", "using", "use", "used",
}

TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9+#./-]*")


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def tokens(text: str) -> list[str]:
    return [token for token in TOKEN_RE.findall(text) if token.lower() not in STOPWORDS and len(token) > 1]


def ngrams(words: list[str], size: int) -> list[str]:
    rows: list[str] = []
    for idx in range(0, max(0, len(words) - size + 1)):
        gram = " ".join(words[idx : idx + size])
        if any(part.lower() not in STOPWORDS for part in gram.split()):
            rows.append(gram)
    return rows


def extract_keywords(text: str, limit: int) -> list[dict[str, object]]:
    words = tokens(text)
    counts: Counter[str] = Counter()
    for size in (1, 2, 3):
        for gram in ngrams(words, size):
            normalized = normalize(gram)
            if len(normalized) >= 3:
                counts[normalized] += 1
    scored = []
    for term, count in counts.items():
        parts = term.split()
        score = count * (1 + 0.65 * (len(parts) - 1))
        if any(char.isdigit() for char in term) or any(char in term for char in "+#./-"):
            score += 0.5
        scored.append((score, count, term))
    scored.sort(key=lambda row: (-row[0], -row[1], row[2]))
    return [{"term": term, "count": count, "score": round(score, 3)} for score, count, term in scored[:limit]]


def compare(resume_text: str, keywords: list[dict[str, object]]) -> list[dict[str, object]]:
    resume = normalize(resume_text)
    rows = []
    for keyword in keywords:
        term = str(keyword["term"])
        rows.append({**keyword, "present": term in resume})
    return rows


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("job_description", type=Path, help="Plain text job description")
    parser.add_argument("--resume", type=Path, help="Resume text/HTML/Markdown/LaTeX to compare against")
    parser.add_argument("--limit", type=int, default=40)
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if not args.job_description.exists():
        return fail(f"job description not found: {args.job_description}")
    jd_text = args.job_description.read_text(encoding="utf-8")
    rows = extract_keywords(jd_text, args.limit)
    if args.resume:
        if not args.resume.exists():
            return fail(f"resume not found: {args.resume}")
        rows = compare(args.resume.read_text(encoding="utf-8"), rows)

    if args.json:
        print(json.dumps(rows, indent=2))
        return 0

    for row in rows:
        marker = ""
        if "present" in row:
            marker = "present" if row["present"] else "missing"
            marker = f" [{marker}]"
        print(f"{row['term']} ({row['count']}){marker}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
