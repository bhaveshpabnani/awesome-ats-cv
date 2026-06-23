#!/usr/bin/env python3
"""Render an ATS-friendly HTML resume template from structured JSON data."""

from __future__ import annotations

import argparse
import json
import re
from html import escape
from pathlib import Path
from typing import Any

try:
    from atscv_utils import ensure_parent, fail
except ModuleNotFoundError:  # pragma: no cover - package entry point path
    from .atscv_utils import ensure_parent, fail


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / "templates"


def rich(text: str) -> str:
    escaped = escape(text)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)


def join_nonempty(parts: list[str], sep: str = " | ") -> str:
    return sep.join(part for part in parts if part)


def contact_html(profile: dict[str, Any]) -> str:
    rows = []
    for item in profile.get("contact", []):
        label = escape(str(item.get("label", "")))
        value = str(item.get("value", ""))
        href = str(item.get("href", ""))
        if href:
            rows.append(f'<a href="{escape(href, quote=True)}">{label or escape(value)}</a>')
        elif value:
            rows.append(escape(value))
    return " | ".join(rows)


def skills_html(skills: dict[str, list[str]]) -> str:
    chunks = []
    for label, values in skills.items():
        if not values:
            continue
        chunks.append(f"<p><strong>{escape(label)}:</strong> {escape(', '.join(values))}</p>")
    return "\n".join(chunks)


def bullet_list(bullets: list[str]) -> str:
    if not bullets:
        return ""
    rows = "\n".join(f"<li>{rich(str(bullet))}</li>" for bullet in bullets)
    return f"<ul>\n{rows}\n</ul>"


def role_html(item: dict[str, Any]) -> str:
    left = join_nonempty([str(item.get("title", "")), str(item.get("organization", ""))])
    right = join_nonempty([str(item.get("location", "")), str(item.get("dates", ""))])
    tech = item.get("keywords") or item.get("technologies") or []
    tech_html = f'<p class="keywords">{escape(", ".join(tech))}</p>' if tech else ""
    return f"""
<article class="entry">
  <div class="entry-head">
    <strong>{escape(left)}</strong>
    <span>{escape(right)}</span>
  </div>
  {tech_html}
  {bullet_list([str(bullet) for bullet in item.get("bullets", [])])}
</article>""".strip()


def section_html(title: str, items: list[dict[str, Any]], empty: str = "") -> str:
    if not items:
        return empty
    body = "\n".join(role_html(item) for item in items)
    return f"<section>\n<h2>{escape(title)}</h2>\n{body}\n</section>"


def education_html(items: list[dict[str, Any]]) -> str:
    if not items:
        return ""
    rows = []
    for item in items:
        left = join_nonempty([str(item.get("degree", "")), str(item.get("institution", ""))])
        right = join_nonempty([str(item.get("location", "")), str(item.get("dates", ""))])
        details = item.get("details", [])
        detail_html = f"<p>{escape('; '.join(details))}</p>" if details else ""
        rows.append(
            f'<article class="entry"><div class="entry-head"><strong>{escape(left)}</strong><span>{escape(right)}</span></div>{detail_html}</article>'
        )
    return f"<section>\n<h2>Education</h2>\n{''.join(rows)}\n</section>"


def simple_list_section(title: str, rows: list[str]) -> str:
    if not rows:
        return ""
    return f"<section>\n<h2>{escape(title)}</h2>\n{bullet_list([str(row) for row in rows])}\n</section>"


def render(template: str, data: dict[str, Any]) -> str:
    profile = data.get("profile", {})
    replacements = {
        "NAME": escape(str(profile.get("name", ""))),
        "HEADLINE": escape(str(profile.get("headline", ""))),
        "CONTACT": contact_html(profile),
        "SUMMARY": rich(str(profile.get("summary", ""))),
        "SKILLS": skills_html(data.get("skills", {})),
        "EXPERIENCE": section_html("Work Experience", data.get("experience", [])),
        "PROJECTS": section_html("Projects", data.get("projects", [])),
        "EDUCATION": education_html(data.get("education", [])),
        "CERTIFICATIONS": simple_list_section("Certifications", data.get("certifications", [])),
        "LEADERSHIP": simple_list_section("Leadership", data.get("leadership", [])),
        "ACHIEVEMENTS": simple_list_section("Achievements", data.get("achievements", [])),
        "PUBLICATIONS": simple_list_section("Publications", data.get("publications", [])),
    }
    rendered = template
    for key, value in replacements.items():
        rendered = rendered.replace("{{" + key + "}}", value)
    return rendered


def list_templates() -> None:
    for path in sorted(TEMPLATE_DIR.glob("*.html")):
        print(path.name)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="List bundled templates")
    parser.add_argument("--template", type=Path, help="Template HTML path or name from templates/")
    parser.add_argument("--data", type=Path, help="Resume JSON data")
    parser.add_argument("--out", type=Path, help="Output HTML path")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.list:
        list_templates()
        return 0
    if not args.template or not args.data or not args.out:
        return fail("pass --template, --data, and --out, or use --list")
    template_path = args.template
    if not template_path.exists():
        template_path = TEMPLATE_DIR / str(args.template)
    if not template_path.exists():
        return fail(f"template not found: {args.template}")
    if not args.data.exists():
        return fail(f"data file not found: {args.data}")
    data = json.loads(args.data.read_text(encoding="utf-8"))
    html = render(template_path.read_text(encoding="utf-8"), data)
    ensure_parent(args.out)
    args.out.write_text(html, encoding="utf-8")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
