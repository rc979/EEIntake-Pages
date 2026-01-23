#!/usr/bin/env python3
"""
Rewrite local evidence pointers in the outline into public GitHub Pages links.

Rules:
  - Any phases/*.{pdf,xlsx,csv} path becomes a link to:
      https://<user>.github.io/<repo>/<path>
    where <path> starts at phases/...
  - Any phases/*.zip pointer (photo sets) becomes a link to the extracted gallery page:
      https://<user>.github.io/<repo>/<gallery_rel>
    where gallery_rel comes from docs/publish_manifest.json ("zip_galleries").

This script edits the Markdown in place.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


BASE_URL_DEFAULT = "https://rc979.github.io/EEIntake"


PHASES_PATH_RE = re.compile(r"phases/P[0-7]/(?:Inputs|Outputs)/[A-Za-z0-9._-]+\.(?:pdf|xlsx|csv|zip)")
# Code spans we can convert into links, but avoid matching the code span inside an existing link
# like [`phases/...`](...) to prevent double-wrapping.
CODE_SPAN_RE = re.compile(r"(?<!\[)`(?P<path>" + PHASES_PATH_RE.pattern + r")`")

# "Bare" pointers: appear as standalone tokens (e.g. in Addendum A lists and tables).
# Carefully avoid URLs and already-linked occurrences by requiring that the preceding character is
# not one of: backtick, [, (, /, :
BARE_TOKEN_RE = re.compile(
    r"(?P<prefix>^|[\s>])"
    r"(?P<path>" + PHASES_PATH_RE.pattern + r")"
    r"(?P<suffix>[),.;:]?)",
    flags=re.MULTILINE,
)


def load_manifest(manifest_path: Path) -> dict:
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def to_public_url(*, base_url: str, path_or_rel: str) -> str:
    return base_url.rstrip("/") + "/" + path_or_rel.lstrip("/")


def link_text(path: str) -> str:
    # Preserve a "file-like" look in Markdown/Word by using code-formatted link text.
    return f"`{path}`"


def rewrite_markdown(md: str, *, base_url: str, zip_galleries: dict[str, str]) -> tuple[str, int]:
    changed = 0

    def to_url(path: str) -> str | None:
        if path.lower().endswith(".zip"):
            gallery_rel = zip_galleries.get(path)
            if not gallery_rel:
                return None
            return to_public_url(base_url=base_url, path_or_rel=gallery_rel)
        if path.lower().endswith(".csv") or path.lower().endswith(".xlsx"):
            # Viewer pages live alongside the artifact in /phases/... as <file>.<ext>.html
            return to_public_url(base_url=base_url, path_or_rel=path + ".html")
        return to_public_url(base_url=base_url, path_or_rel=path)

    # 0) Fix accidental double-wrapped links (idempotency guard).
    # Pattern produced by older passes: [[<link>](url)](url) where inner+outer URL are identical.
    nested_re = re.compile(
        r"\[(?P<link>\[`"
        + PHASES_PATH_RE.pattern
        + r"`\]\((?P<url>[^)]+)\))\]\((?P=url)\)"
    )
    md, n_nested = nested_re.subn(r"\g<link>", md)
    changed += n_nested

    # 1) Update existing markdown links to point at viewer pages for CSV/XLSX.
    # e.g. [`phases/...xlsx`](https://.../phases/...xlsx) -> ...xlsx.html
    LINK_RE = re.compile(r"\[(?P<text>`(?P<path>" + PHASES_PATH_RE.pattern + r")`)\]\((?P<url>[^)]+)\)")

    def repl_link(m: re.Match[str]) -> str:
        nonlocal changed
        path = m.group("path")
        desired = to_url(path)
        if not desired:
            return m.group(0)
        current = m.group("url")
        if current == desired:
            return m.group(0)
        changed += 1
        return f"[{m.group('text')}]({desired})"

    md = LINK_RE.sub(repl_link, md)

    # 2) Replace code spans: `phases/...` -> [`phases/...`](url)
    def repl_code(m: re.Match[str]) -> str:
        nonlocal changed
        path = m.group("path")
        url = to_url(path)
        if not url:
            return m.group(0)
        changed += 1
        return f"[{link_text(path)}]({url})"

    md = CODE_SPAN_RE.sub(repl_code, md)

    # 3) Replace bare tokens (Addendum lists/tables/etc).
    # Skip if preceding character suggests this is already linkified or part of a URL.
    def repl_bare(m: re.Match[str]) -> str:
        nonlocal changed
        prefix = m.group("prefix")
        path = m.group("path")
        suffix = m.group("suffix")

        # If this token is already part of markdown link text like [`phases/...`](...)
        # then prefix will often be "[" or "`" (depending on where regex starts); avoid rewriting.
        prev_char = prefix[-1:] if prefix else ""
        if prev_char in ("`", "[", "(", "/", ":"):
            return m.group(0)

        url = to_url(path)
        if not url:
            return m.group(0)
        changed += 1
        return f"{prefix}[{link_text(path)}]({url}){suffix}"

    md2 = BARE_TOKEN_RE.sub(repl_bare, md)
    return md2, changed


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default=BASE_URL_DEFAULT)
    ap.add_argument("--manifest", default="docs/publish_manifest.json")
    ap.add_argument("--md", default="EV Charging Project Plan Outline.md")
    args = ap.parse_args()

    root = Path(".").resolve()
    manifest_path = (root / args.manifest).resolve()
    md_path = (root / args.md).resolve()

    manifest = load_manifest(manifest_path)
    zip_galleries: dict[str, str] = manifest.get("zip_galleries", {})

    s = md_path.read_text(encoding="utf-8")
    s2, n = rewrite_markdown(s, base_url=args.base_url, zip_galleries=zip_galleries)
    if n:
        md_path.write_text(s2, encoding="utf-8")

    print(f"Updated links: {n}")
    # Quick sanity: report any remaining .zip pointers in Addendum A style
    remaining_zip = len(re.findall(r"phases/P[0-7]/(?:Inputs|Outputs)/[^\\s`]+\\.zip", s2))
    if remaining_zip:
        print(f"WARNING: remaining zip pointers: {remaining_zip}")


if __name__ == "__main__":
    main()

