#!/usr/bin/env python3
"""Edit structured resume JSON data for bundled HTML templates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from atscv_utils import ensure_parent, fail
except ModuleNotFoundError:  # pragma: no cover - package entry point path
    from .atscv_utils import ensure_parent, fail


def set_dotted(data: dict[str, Any], dotted: str, value: str) -> None:
    parts = dotted.split(".")
    cursor: Any = data
    for part in parts[:-1]:
        if part.isdigit():
            cursor = cursor[int(part)]
        else:
            cursor = cursor.setdefault(part, {})
    last = parts[-1]
    if last.isdigit():
        cursor[int(last)] = value
    else:
        cursor[last] = value


def add_skill(data: dict[str, Any], spec: str) -> None:
    if "=" not in spec:
        raise ValueError("--add-skill expects Category=Skill")
    category, skill = spec.split("=", 1)
    skills = data.setdefault("skills", {})
    rows = skills.setdefault(category.strip(), [])
    if skill.strip() not in rows:
        rows.append(skill.strip())


def add_bullet(data: dict[str, Any], spec: str) -> None:
    parts = spec.split(":", 2)
    if len(parts) != 3 or not parts[1].isdigit():
        raise ValueError("--add-bullet expects section:index:bullet")
    section, index_raw, bullet = parts
    entries = data.setdefault(section, [])
    index = int(index_raw)
    while len(entries) <= index:
        entries.append({"title": "", "organization": "", "bullets": []})
    entries[index].setdefault("bullets", []).append(bullet.strip())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data", type=Path, help="Input resume JSON")
    parser.add_argument("--out", type=Path, help="Output JSON path")
    parser.add_argument("--in-place", action="store_true", help="Overwrite input JSON")
    parser.add_argument("--set", action="append", default=[], help="Set dotted path, for example profile.summary=Text")
    parser.add_argument("--add-skill", action="append", default=[], help="Append skill, for example Cloud=Azure")
    parser.add_argument("--add-bullet", action="append", default=[], help="Append bullet, for example experience:0:Built APIs")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if not args.data.exists():
        return fail(f"data file not found: {args.data}")
    if not args.in_place and not args.out:
        return fail("pass --out or --in-place")
    data = json.loads(args.data.read_text(encoding="utf-8"))

    try:
        for spec in args.set:
            if "=" not in spec:
                raise ValueError("--set expects dotted.path=value")
            key, value = spec.split("=", 1)
            set_dotted(data, key.strip(), value.strip())
        for spec in args.add_skill:
            add_skill(data, spec)
        for spec in args.add_bullet:
            add_bullet(data, spec)
    except (IndexError, TypeError, ValueError) as exc:
        return fail(str(exc))

    out = args.data if args.in_place else args.out
    assert out is not None
    ensure_parent(out)
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
