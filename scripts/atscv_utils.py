#!/usr/bin/env python3
"""Shared helpers for Awesome ATS CV command-line scripts."""

from __future__ import annotations

import os
import platform
import shutil
from pathlib import Path


def fail(message: str, code: int = 2) -> int:
    print(f"error: {message}")
    return code


def which_any(names: list[str]) -> str | None:
    for name in names:
        found = shutil.which(name)
        if found:
            return found
    return None


def find_chromium() -> str | None:
    """Find a Chrome/Chromium/Edge executable across macOS, Linux, and Windows."""
    env = os.environ.get("ATS_CV_CHROME") or os.environ.get("CHROME_PATH")
    if env and Path(env).exists():
        return env

    system = platform.system().lower()
    candidates: list[str] = []
    if system == "darwin":
        candidates = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        ]
    elif system == "windows":
        program_files = [
            os.environ.get("PROGRAMFILES", r"C:\Program Files"),
            os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)"),
            os.environ.get("LOCALAPPDATA", ""),
        ]
        for root in program_files:
            if not root:
                continue
            candidates.extend(
                [
                    str(Path(root) / "Google/Chrome/Application/chrome.exe"),
                    str(Path(root) / "Microsoft/Edge/Application/msedge.exe"),
                    str(Path(root) / "Chromium/Application/chrome.exe"),
                ]
            )
    else:
        found = which_any(
            [
                "google-chrome",
                "google-chrome-stable",
                "chromium",
                "chromium-browser",
                "microsoft-edge",
                "microsoft-edge-stable",
            ]
        )
        if found:
            return found

    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate
    return None


def find_poppler_tool(tool: str) -> str | None:
    """Find a Poppler binary with optional environment override."""
    env_name = f"ATS_CV_{tool.upper()}"
    env = os.environ.get(env_name)
    if env and Path(env).exists():
        return env
    return which_any([tool])


def path_to_file_url(path: Path) -> str:
    return path.resolve().as_uri()


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

