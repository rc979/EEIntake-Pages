#!/usr/bin/env python3
"""
Local GitHub Pages site builder.

Builds a static site under ./docs suitable for GitHub Pages (same repo):
  - Copies phase artifacts from ./phases -> ./docs/phases (excluding .zip and .DS_Store)
  - Extracts images from any .zip photo sets into ./docs/galleries/<zip-stem>/assets/
  - Generates minimal HTML gallery pages for each zip
  - Writes ./docs/publish_manifest.json to support later link-rewrites in the outline

This script intentionally does NOT modify the main markdown document yet.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import zipfile
from dataclasses import dataclass
from pathlib import Path


IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
SKIP_NAMES = {".DS_Store"}


def _repo_root() -> Path:
    # scripts/publish/publish_pages_site.py -> repo root (three parents up)
    return Path(__file__).resolve().parents[2]


def _slugify(s: str) -> str:
    s = s.strip()
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"[^A-Za-z0-9._-]+", "-", s)
    s = re.sub(r"-{2,}", "-", s)
    return s.strip("-").lower() or "gallery"


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _copy_tree_excluding(phases_dir: Path, out_phases_dir: Path) -> list[str]:
    copied: list[str] = []
    for src in phases_dir.rglob("*"):
        if src.is_dir():
            continue
        if src.name in SKIP_NAMES:
            continue
        if src.suffix.lower() == ".zip":
            continue
        rel = src.relative_to(phases_dir)
        dst = out_phases_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied.append(str(Path("phases") / rel))
    return sorted(copied)


@dataclass(frozen=True)
class Gallery:
    zip_rel: str  # e.g. phases/P1/Inputs/....zip (source)
    page_rel: str  # e.g. galleries/<slug>/index.html (published)
    image_rel_paths: list[str]  # e.g. ["galleries/<slug>/assets/IMG_0001.jpg", ...]
    image_names: list[str]  # e.g. ["IMG_0001.jpg", ...] (relative to gallery page)


def _extract_zip_images_to_gallery(
    *,
    phases_dir: Path,
    zip_path: Path,
    galleries_dir: Path,
) -> Gallery | None:
    zip_rel = str(Path("phases") / zip_path.relative_to(phases_dir))
    stem = zip_path.stem
    slug = _slugify(stem)
    gallery_dir = galleries_dir / slug
    assets_dir = gallery_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    image_rel_paths: list[str] = []
    image_names: list[str] = []
    extracted = 0

    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            for info in zf.infolist():
                if info.is_dir():
                    continue
                ext = Path(info.filename).suffix.lower()
                if ext not in IMAGE_EXTS:
                    continue

                # Flatten to basename; de-dupe if collisions
                base = Path(info.filename).name
                out_name = base
                i = 2
                while (assets_dir / out_name).exists():
                    out_name = f"{Path(base).stem}-{i}{Path(base).suffix}"
                    i += 1

                (assets_dir / out_name).write_bytes(zf.read(info.filename))
                image_rel_paths.append(str(Path("galleries") / slug / "assets" / out_name))
                image_names.append(out_name)
                extracted += 1
    except zipfile.BadZipFile:
        return None

    if extracted == 0:
        return None

    page_rel = str(Path("galleries") / slug / "index.html")
    _write_text(gallery_dir / "index.html", _render_gallery_html(zip_rel=zip_rel, image_names=sorted(image_names)))

    return Gallery(
        zip_rel=zip_rel,
        page_rel=page_rel,
        image_rel_paths=sorted(image_rel_paths),
        image_names=sorted(image_names),
    )


def _render_gallery_html(*, zip_rel: str, image_names: list[str]) -> str:
    title = f"Gallery: {zip_rel}"
    items = "\n".join(
        f'<figure class="card"><a href="assets/{html.escape(name)}"><img src="assets/{html.escape(name)}" alt="{html.escape(name)}"></a><figcaption>{html.escape(name)}</figcaption></figure>'
        for name in image_names
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif; margin: 24px; }}
    a {{ color: #0b57d0; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .meta {{ color: #444; margin: 8px 0 16px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 12px; }}
    .card {{ border: 1px solid #ddd; border-radius: 10px; padding: 10px; background: #fff; }}
    img {{ width: 100%; height: 180px; object-fit: cover; border-radius: 8px; background: #f5f5f5; }}
    figcaption {{ font-size: 12px; color: #333; margin-top: 6px; word-break: break-word; }}
  </style>
</head>
<body>
  <p><a href="../index.html">All galleries</a></p>
  <h1>{html.escape(title)}</h1>
  <div class="meta">Extracted images from: <code>{html.escape(zip_rel)}</code></div>
  <div class="grid">
    {items}
  </div>
</body>
</html>
"""


def _render_galleries_index(galleries: list[Gallery]) -> str:
    def href_from_galleries_index(page_rel: str) -> str:
        # docs/galleries/index.html -> sibling folders under docs/galleries/
        # page_rel is like "galleries/<slug>/index.html"
        p = Path(page_rel)
        return str(Path(p.parts[1]) / p.parts[2]) if len(p.parts) >= 3 and p.parts[0] == "galleries" else page_rel

    items = "\n".join(
        f'<li><a href="{html.escape(href_from_galleries_index(g.page_rel))}">{html.escape(g.zip_rel)}</a> ({len(g.image_names)} images)</li>'
        for g in galleries
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Galleries</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif; margin: 24px; }}
    a {{ color: #0b57d0; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
  </style>
</head>
<body>
  <p><a href="../index.html">Home</a></p>
  <h1>Galleries</h1>
  <ul>
    {items or "<li>(none)</li>"}
  </ul>
</body>
</html>
"""


def _render_site_index(*, artifact_count: int, gallery_count: int) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>EE Intake Artifacts</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif; margin: 24px; max-width: 900px; }}
    a {{ color: #0b57d0; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .box {{ border: 1px solid #ddd; border-radius: 12px; padding: 14px; margin: 12px 0; }}
    code {{ background: #f6f6f6; padding: 1px 4px; border-radius: 4px; }}
  </style>
</head>
<body>
  <h1>EE Intake – Published Artifacts</h1>
  <div class="box">
    <div><strong>Phase artifacts</strong>: <code>docs/phases/</code> (published)</div>
    <div><strong>Galleries</strong>: <code>docs/galleries/</code> (published)</div>
    <div><strong>Manifest</strong>: <code>docs/publish_manifest.json</code></div>
  </div>
  <div class="box">
    <div>Artifacts copied: <strong>{artifact_count}</strong></div>
    <div>Galleries generated: <strong>{gallery_count}</strong></div>
  </div>
  <ul>
    <li><a href="galleries/index.html">Browse galleries</a></li>
    <li><a href="phases/">Browse phases folder</a> (directory listing depends on host; GitHub Pages may not show folder listings)</li>
  </ul>
  <p>
    Note: This site is generated locally by <code>scripts/publish/publish_pages_site.py</code>.
    It does not modify the project outline links yet.
  </p>
</body>
</html>
"""


def build_site(*, phases_dir: Path, docs_dir: Path, clean: bool) -> dict:
    out_phases_dir = docs_dir / "phases"
    galleries_dir = docs_dir / "galleries"

    if clean:
        # Only remove generated areas; avoid nuking user-owned files like docs/CNAME.
        for p in [out_phases_dir, galleries_dir]:
            if p.exists():
                shutil.rmtree(p)
        for f in [docs_dir / "index.html", docs_dir / "publish_manifest.json", docs_dir / ".nojekyll"]:
            if f.exists():
                f.unlink()

    docs_dir.mkdir(parents=True, exist_ok=True)
    _write_text(docs_dir / ".nojekyll", "")  # disable Jekyll for consistent handling

    artifacts = _copy_tree_excluding(phases_dir, out_phases_dir)

    galleries: list[Gallery] = []
    for zip_path in sorted(phases_dir.rglob("*.zip")):
        if zip_path.name in SKIP_NAMES:
            continue
        g = _extract_zip_images_to_gallery(phases_dir=phases_dir, zip_path=zip_path, galleries_dir=galleries_dir)
        if g is not None:
            galleries.append(g)

    _write_text(galleries_dir / "index.html", _render_galleries_index(galleries))
    _write_text(docs_dir / "index.html", _render_site_index(artifact_count=len(artifacts), gallery_count=len(galleries)))

    manifest = {
        "published_root": "docs/",
        "artifacts_copied": artifacts,
        "zip_galleries": {g.zip_rel: g.page_rel for g in galleries},
    }
    _write_text(docs_dir / "publish_manifest.json", json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return manifest


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--phases", default="phases", help="Source phases directory (default: phases)")
    ap.add_argument("--docs", default="docs", help="Output docs directory for Pages (default: docs)")
    ap.add_argument("--no-clean", action="store_true", help="Do not delete existing generated outputs first")
    args = ap.parse_args()

    root = _repo_root()
    phases_dir = (root / args.phases).resolve()
    docs_dir = (root / args.docs).resolve()

    if not phases_dir.exists():
        raise SystemExit(f"Missing phases dir: {phases_dir}")

    manifest = build_site(phases_dir=phases_dir, docs_dir=docs_dir, clean=not args.no_clean)
    print("Built Pages site at:", docs_dir)
    print("Artifacts copied:", len(manifest["artifacts_copied"]))
    print("Galleries:", len(manifest["zip_galleries"]))
    print("Manifest:", docs_dir / "publish_manifest.json")


if __name__ == "__main__":
    main()

