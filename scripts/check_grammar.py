#!/usr/bin/env python3
"""Check resume grammar with offline hygiene, optional spellcheck, LanguageTool, or Grammarly gates."""

from __future__ import annotations

import argparse
import json
import re
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

try:
    from atscv_utils import fail
except ModuleNotFoundError:  # pragma: no cover - package entry point path
    from .atscv_utils import fail


DEFAULT_LANGUAGETOOL_URL = "https://api.languagetool.org/v2/check"
FALLBACK_COMMON_TYPOS = {
    "grammer": "grammar",
    "recieve": "receive",
    "seperate": "separate",
    "definately": "definitely",
    "occured": "occurred",
    "enviroment": "environment",
    "acheived": "achieved",
    "developement": "development",
    "maintainence": "maintenance",
    "performace": "performance",
    "scalablee": "scalable",
}

DEFAULT_TECH_TERMS = {
    "api", "apis", "aws", "azure", "backend", "bitbucket", "ci", "cosmos", "db", "devops", "docker",
    "dynamodb", "ec2", "etl", "fastapi", "github", "gitlab", "graphql", "html", "http", "https",
    "javascript", "kafka", "kubernetes", "langgraph", "linkedin", "linux", "llm", "llms", "macos",
    "mongodb", "node", "postgresql", "python", "rag", "redis", "rest", "sdk", "sql", "swiftui",
    "typescript", "ui", "ux", "websocket", "websockets", "winui",
}


class VisibleTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in {"script", "style", "noscript", "title"}:
            self.skip_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"script", "style", "noscript", "title"} and self.skip_depth:
            self.skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        clean = " ".join(data.split())
        if clean:
            self.parts.append(clean)


def extract_visible_text(path: Path) -> str:
    raw = path.read_text(encoding="utf-8")
    suffix = path.suffix.lower()
    if suffix in {".html", ".htm"}:
        parser = VisibleTextParser()
        parser.feed(raw)
        text = " ".join(parser.parts)
        return re.sub(r"\s+([,.!?;:])", r"\1", text)
    text = re.sub(r"\\href\{[^}]*\}\{([^}]*)\}", r"\1", raw)
    text = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^]]*\])?", " ", text)
    text = text.replace("{", " ").replace("}", " ")
    return text


def load_custom_terms(paths: list[Path]) -> set[str]:
    terms = set(DEFAULT_TECH_TERMS)
    for path in paths:
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            term = line.strip().lower()
            if term and not term.startswith("#"):
                terms.add(term)
    return terms


def offline_hygiene_issues(text: str) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    compact = re.sub(r"https?://\S+", " ", text)
    compact = re.sub(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b", " ", compact)
    for match in re.finditer(r"\b([A-Za-z]+)\s+\1\b", compact, re.I):
        issues.append({"rule": "REPEATED_WORD", "message": f"Repeated word `{match.group(0)}`", "suggestion": match.group(1)})
    for match in re.finditer(r"\s+[,.!?;:]", compact):
        issues.append({"rule": "SPACE_BEFORE_PUNCTUATION", "message": "Remove space before punctuation", "suggestion": ""})
    for typo, correction in FALLBACK_COMMON_TYPOS.items():
        for match in re.finditer(rf"\b{re.escape(typo)}\b", compact, re.I):
            issues.append({"rule": "FALLBACK_TYPO_LIST", "message": f"Possible typo `{match.group(0)}`", "suggestion": correction})
    return issues


def spellchecker_issues(text: str, custom_terms: set[str], max_words: int) -> list[dict[str, str]]:
    try:
        from spellchecker import SpellChecker
    except Exception as exc:  # pragma: no cover - optional dependency
        raise RuntimeError("pyspellchecker is required: python -m pip install 'awesome-ats-cv[grammar]'") from exc

    compact = re.sub(r"https?://\S+|\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b", " ", text)
    words = []
    for token in re.findall(r"[A-Za-z][A-Za-z'-]*", compact):
        normalized = token.strip("'").lower()
        if not normalized or normalized in custom_terms:
            continue
        if len(normalized) <= 2 or token.isupper() or any(char.isdigit() for char in token):
            continue
        if re.search(r"[A-Z][a-z]+[A-Z]", token):
            continue
        words.append(normalized)

    spell = SpellChecker()
    spell.word_frequency.load_words(custom_terms)
    unknown = sorted(spell.unknown(words))
    issues = []
    for word in unknown[:max_words]:
        correction = spell.correction(word) or ""
        issues.append({"rule": "SPELLCHECK", "message": f"Possible misspelling `{word}`", "suggestion": correction})
    if len(unknown) > max_words:
        issues.append({"rule": "SPELLCHECK_TRUNCATED", "message": f"{len(unknown) - max_words} more spelling issues suppressed", "suggestion": ""})
    return issues


def languagetool_issues(text: str, url: str, language: str) -> list[dict[str, str]]:
    payload = urllib.parse.urlencode({"text": text, "language": language}).encode("utf-8")
    request = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.loads(response.read().decode("utf-8"))
    issues = []
    for match in data.get("matches", []):
        replacements = match.get("replacements", [])
        suggestion = replacements[0].get("value", "") if replacements else ""
        issues.append(
            {
                "rule": match.get("rule", {}).get("id", "LANGUAGETOOL"),
                "message": match.get("message", ""),
                "suggestion": suggestion,
                "context": match.get("context", {}).get("text", ""),
            }
        )
    return issues


def print_manual_gate() -> None:
    print("Manual Grammarly/grammar gate:")
    print("- Paste the final plain-text resume or editable source into Grammarly")
    print("- Review grammar, spelling, punctuation, clarity, concision, and tone suggestions")
    print("- Reject suggestions that change technical meaning, metrics, product names, or resume style rules")
    print("- Re-render the resume after edits and rerun PDF/text extraction validation")
    print("- Save the final Grammarly-reviewed source/PDF with a timestamp")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, nargs="?", help="Resume source or extracted text file")
    parser.add_argument("--provider", choices=["offline", "spellchecker", "languagetool", "manual", "skip"], default="offline")
    parser.add_argument("--language", default="en-US")
    parser.add_argument("--url", default=DEFAULT_LANGUAGETOOL_URL, help="LanguageTool endpoint")
    parser.add_argument("--dictionary", action="append", default=[], type=Path, help="Custom dictionary file, one allowed term per line")
    parser.add_argument("--max-spelling-issues", type=int, default=50, help="Maximum spellchecker issues to print")
    parser.add_argument("--max-issues", type=int, default=0, help="Fail when issues exceed this count")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.provider == "skip":
        print("grammar check skipped")
        return 0
    if args.provider == "manual":
        print_manual_gate()
        return 0
    if not args.source:
        return fail("source is required unless --provider manual or --provider skip")
    if not args.source.exists():
        return fail(f"source not found: {args.source}")

    text = extract_visible_text(args.source)
    if args.provider == "offline":
        issues = offline_hygiene_issues(text)
        provider_note = "offline hygiene only: repeated words, punctuation spacing, and a small fallback typo list"
    elif args.provider == "spellchecker":
        try:
            issues = spellchecker_issues(text, load_custom_terms(args.dictionary), args.max_spelling_issues)
        except Exception as exc:
            return fail(str(exc))
        provider_note = "dictionary spellcheck: pyspellchecker plus resume technical-term allowlist"
    else:
        try:
            issues = languagetool_issues(text, args.url, args.language)
        except Exception as exc:  # pragma: no cover - network dependent
            return fail(f"LanguageTool check failed: {exc}")
        provider_note = "LanguageTool grammar and spelling API"

    if args.json:
        print(json.dumps({"provider": args.provider, "note": provider_note, "issues": issues}, indent=2))
    else:
        print(f"grammar provider: {args.provider}")
        print(f"scope: {provider_note}")
        print(f"issues: {len(issues)}")
        for issue in issues:
            suggestion = f" -> {issue['suggestion']}" if issue.get("suggestion") else ""
            context = f" | {issue['context']}" if issue.get("context") else ""
            print(f"- {issue['rule']}: {issue['message']}{suggestion}{context}")
    return 1 if len(issues) > args.max_issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
