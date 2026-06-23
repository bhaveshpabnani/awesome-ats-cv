#!/usr/bin/env python3
"""Measure rendered bullet line-width ratios in an HTML resume."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from atscv_utils import fail, find_chromium, path_to_file_url


MEASURE_JS = r"""
async ({ selector, pageSelector }) => {
  const pageEl = document.querySelector(pageSelector) || document.body;
  const pageRect = pageEl.getBoundingClientRect();
  const items = [...document.querySelectorAll(selector)];
  return items.map((li, index) => {
    const range = document.createRange();
    range.selectNodeContents(li);
    const rect = range.getBoundingClientRect();
    const liRect = li.getBoundingClientRect();
    const available = pageRect.right - liRect.left - 2;
    return {
      index: index + 1,
      ratio: Number((rect.width / available).toFixed(3)),
      width: Math.round(rect.width),
      available: Math.round(available),
      text: li.innerText.replace(/\s+/g, " ").trim()
    };
  });
}
"""


def load_playwright():
    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:  # pragma: no cover - environment dependent
        raise RuntimeError("Playwright is required: python -m pip install playwright && playwright install chromium") from exc
    return sync_playwright


def measure(args: argparse.Namespace) -> list[dict[str, object]]:
    sync_playwright = load_playwright()
    browser_path = str(args.browser) if args.browser else find_chromium()
    with sync_playwright() as p:
        if browser_path:
            browser = p.chromium.launch(executable_path=browser_path, headless=True)
        else:
            browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": args.viewport_width, "height": args.viewport_height})
        page.goto(path_to_file_url(args.html.resolve()))
        rows = page.evaluate(MEASURE_JS, {"selector": args.selector, "pageSelector": args.page_selector})
        browser.close()
    return rows


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path, help="Input HTML resume")
    parser.add_argument("--selector", default="li", help="Bullet selector, default: li")
    parser.add_argument("--page-selector", default=".page", help="Page container selector, default: .page")
    parser.add_argument("--min", type=float, default=0.90, help="Minimum acceptable ratio")
    parser.add_argument("--max", type=float, default=0.98, help="Maximum acceptable ratio")
    parser.add_argument("--viewport-width", type=int, default=1240)
    parser.add_argument("--viewport-height", type=int, default=1754)
    parser.add_argument("--browser", type=Path, help="Chrome/Chromium executable")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if not args.html.exists():
        return fail(f"HTML file not found: {args.html}")
    try:
        rows = measure(args)
    except RuntimeError as exc:
        return fail(str(exc))

    offenders = [row for row in rows if float(row["ratio"]) < args.min or float(row["ratio"]) > args.max]
    if args.json:
        print(json.dumps({"rows": rows, "offenders": offenders}, indent=2))
    else:
        print(f"measured {len(rows)} bullet(s)")
        if rows:
            ratios = [float(row["ratio"]) for row in rows]
            print(f"ratio range: {min(ratios):.3f} - {max(ratios):.3f}")
        for row in offenders:
            print(
                f"{int(row['index']):02d} {float(row['ratio']):.3f} "
                f"{row['width']}/{row['available']} {row['text']}"
            )
    return 1 if offenders else 0


if __name__ == "__main__":
    raise SystemExit(main())

