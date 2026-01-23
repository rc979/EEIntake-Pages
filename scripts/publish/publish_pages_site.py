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
import subprocess
import zipfile
from dataclasses import dataclass
from pathlib import Path


IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
TABULAR_EXTS = {".csv", ".xlsx"}
SKIP_NAMES = {".DS_Store"}
ROBOTS_META = '<meta name="robots" content="noindex, nofollow">'


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
  {ROBOTS_META}
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
  {ROBOTS_META}
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
  {ROBOTS_META}
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
    <li><a href="outline/index.html">Browse project outline (HTML)</a></li>
    <li><a href="galleries/index.html">Browse galleries</a></li>
    <li><a href="phases/index.html">Browse phases folder</a></li>
  </ul>
  <p>
    Note: This site is generated locally by <code>scripts/publish/publish_pages_site.py</code>.
    To update the project outline to point at these public URLs, run <code>scripts/publish/linkify_outline_public_urls.py</code>
    and then re-export the Word doc.
  </p>
</body>
</html>
"""


def _render_dir_index(*, title: str, rel_root: str, entries: list[tuple[str, str, bool, str | None]]) -> str:
    """
    entries: (name, href, is_dir, download_href)
    rel_root: path from this index.html to docs/ root (e.g. "..", "../..", ".")
    """
    def row_html(name: str, href: str, is_dir: bool, download_href: str | None) -> str:
        dl = "—" if download_href is None else f'<a href="{html.escape(download_href)}">download</a>'
        kind = "dir" if is_dir else "file"
        return (
            f"<tr>"
            f'<td class="kind">{kind}</td>'
            f'<td><a href="{html.escape(href)}">{html.escape(name)}</a></td>'
            f'<td class="dl">{dl}</td>'
            f"</tr>"
        )

    rows = "\n".join(row_html(name, href, is_dir, download_href) for name, href, is_dir, download_href in entries)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  {ROBOTS_META}
  <title>{html.escape(title)}</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif; margin: 24px; max-width: 1000px; }}
    a {{ color: #0b57d0; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border-bottom: 1px solid #eee; padding: 8px 6px; text-align: left; vertical-align: top; }}
    .kind {{ color: #666; width: 60px; }}
    .dl {{ width: 90px; color: #666; }}
    code {{ background: #f6f6f6; padding: 1px 4px; border-radius: 4px; }}
  </style>
</head>
<body>
  <p>
    <a href="{html.escape(rel_root)}/index.html">Home</a>
  </p>
  <h1>{html.escape(title)}</h1>
  <table>
    <thead>
      <tr><th class="kind">Type</th><th>Name</th><th class="dl">Download</th></tr>
    </thead>
    <tbody>
      {rows or '<tr><td colspan="2">(empty)</td></tr>'}
    </tbody>
  </table>
</body>
</html>
"""


def _write_directory_indexes(*, docs_dir: Path, out_root: Path) -> None:
    """
    GitHub Pages does not provide directory listings. Create index.html pages for out_root
    and every subdirectory so users can browse artifacts.
    """
    for d in sorted([out_root] + [p for p in out_root.rglob("*") if p.is_dir()]):
        # entries relative to current directory
        entries: list[tuple[str, str, bool, str | None]] = []

        # up link (except for root)
        if d != out_root:
            entries.append(("..", "../index.html", True, None))

        children = [p for p in d.iterdir() if p.name not in SKIP_NAMES]
        # Do not show generated index itself as an entry
        children = [p for p in children if p.name != "index.html"]

        dirs = sorted([p for p in children if p.is_dir()], key=lambda p: p.name.lower())
        files = sorted([p for p in children if p.is_file()], key=lambda p: p.name.lower())
        for p in dirs:
            entries.append((p.name + "/", f"{p.name}/index.html", True, None))

        # Hide generated viewer helper pages (we link to them from the real file row)
        viewer_suffixes = (".csv.html", ".xlsx.html")
        files = [p for p in files if not p.name.lower().endswith(viewer_suffixes)]

        for p in files:
            if p.suffix.lower() in TABULAR_EXTS:
                # Clicking "Name" opens viewer; "download" fetches the raw file.
                entries.append((p.name, f"{p.name}.html", False, p.name))
            else:
                entries.append((p.name, p.name, False, None))

        rel_root = str(Path(*([".."] * len(d.relative_to(docs_dir).parts)))) or "."
        # title relative to docs/
        title = f"Index of /{d.relative_to(docs_dir).as_posix()}"
        _write_text(d / "index.html", _render_dir_index(title=title, rel_root=rel_root, entries=entries))


def _render_csv_viewer_html(filename: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  {ROBOTS_META}
  <title>View CSV: {html.escape(filename)}</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif; margin: 20px; }}
    a {{ color: #0b57d0; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .bar {{ display: flex; gap: 12px; flex-wrap: wrap; align-items: center; margin: 10px 0 14px; }}
    .meta {{ color: #555; font-size: 13px; }}
    table {{ border-collapse: collapse; width: 100%; font-size: 13px; }}
    th, td {{ border: 1px solid #eee; padding: 6px 8px; vertical-align: top; }}
    th {{ position: sticky; top: 0; background: #fafafa; }}
    code {{ background: #f6f6f6; padding: 1px 4px; border-radius: 4px; }}
    .warn {{ color: #a14; }}
  </style>
</head>
<body>
  <div class="bar">
    <a href="index.html">Back to folder</a>
    <a href="{html.escape(filename)}" download>Download</a>
    <span class="meta"><code>{html.escape(filename)}</code></span>
    <span id="status" class="meta">Loading…</span>
  </div>
  <div id="note" class="meta"></div>
  <div id="table"></div>
  <script>
    // Minimal CSV parser (handles quoted fields, commas, CRLF).
    function parseCSV(text) {{
      const rows = [];
      let row = [];
      let field = '';
      let i = 0;
      let inQuotes = false;
      while (i < text.length) {{
        const c = text[i];
        if (inQuotes) {{
          if (c === '\"') {{
            if (text[i+1] === '\"') {{ field += '\"'; i += 2; continue; }}
            inQuotes = false; i++; continue;
          }}
          field += c; i++; continue;
        }}
        if (c === '\"') {{ inQuotes = true; i++; continue; }}
        if (c === ',') {{ row.push(field); field = ''; i++; continue; }}
        if (c === '\\r') {{ i++; continue; }}
        if (c === '\\n') {{ row.push(field); rows.push(row); row = []; field = ''; i++; continue; }}
        field += c; i++;
      }}
      if (field.length || row.length) {{ row.push(field); rows.push(row); }}
      return rows;
    }}

    function esc(s) {{
      return String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
    }}

    async function main() {{
      const status = document.getElementById('status');
      const note = document.getElementById('note');
      const out = document.getElementById('table');
      const url = {json.dumps(filename)};
      const res = await fetch(url);
      if (!res.ok) {{
        status.textContent = 'Failed to load CSV';
        note.innerHTML = '<span class="warn">HTTP ' + res.status + '</span>';
        return;
      }}
      const text = await res.text();
      const rows = parseCSV(text);
      if (!rows.length) {{
        status.textContent = 'Empty CSV';
        return;
      }}
      const maxRows = 2000;
      const shown = rows.slice(0, maxRows);
      if (rows.length > maxRows) {{
        note.textContent = 'Showing first ' + maxRows + ' rows of ' + rows.length + '. Download for full file.';
      }}
      const headers = shown[0];
      let html = '<table><thead><tr>';
      for (const h of headers) html += '<th>' + esc(h) + '</th>';
      html += '</tr></thead><tbody>';
      for (let r = 1; r < shown.length; r++) {{
        html += '<tr>';
        const row = shown[r];
        for (let c = 0; c < headers.length; c++) {{
          html += '<td>' + esc(row[c] ?? '') + '</td>';
        }}
        html += '</tr>';
      }}
      html += '</tbody></table>';
      out.innerHTML = html;
      status.textContent = 'Loaded';
    }}
    main().catch(e => {{
      document.getElementById('status').textContent = 'Error';
      document.getElementById('note').innerHTML = '<span class="warn">' + (e?.message || String(e)) + '</span>';
    }});
  </script>
</body>
</html>
"""


def _render_xlsx_viewer_html(filename: str) -> str:
    # Client-side parse using SheetJS via CDN.
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  {ROBOTS_META}
  <title>View XLSX: {html.escape(filename)}</title>
  <script src="https://cdn.jsdelivr.net/npm/xlsx/dist/xlsx.full.min.js"></script>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif; margin: 20px; }}
    a {{ color: #0b57d0; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .bar {{ display: flex; gap: 12px; flex-wrap: wrap; align-items: center; margin: 10px 0 14px; }}
    .meta {{ color: #555; font-size: 13px; }}
    #sheet {{ padding: 6px 8px; }}
    table {{ border-collapse: collapse; width: 100%; font-size: 13px; }}
    th, td {{ border: 1px solid #eee; padding: 6px 8px; vertical-align: top; }}
    code {{ background: #f6f6f6; padding: 1px 4px; border-radius: 4px; }}
    .warn {{ color: #a14; }}
    .sheetwrap {{ overflow-x: auto; }}
  </style>
</head>
<body>
  <div class="bar">
    <a href="index.html">Back to folder</a>
    <a href="{html.escape(filename)}" download>Download</a>
    <span class="meta"><code>{html.escape(filename)}</code></span>
    <span id="status" class="meta">Loading…</span>
    <label class="meta">Sheet:
      <select id="sheet"></select>
    </label>
  </div>
  <div id="note" class="meta"></div>
  <div class="sheetwrap" id="out"></div>
  <script>
    const fileUrl = {json.dumps(filename)};
    async function main() {{
      const status = document.getElementById('status');
      const note = document.getElementById('note');
      const out = document.getElementById('out');
      const sel = document.getElementById('sheet');

      const res = await fetch(fileUrl);
      if (!res.ok) {{
        status.textContent = 'Failed to load XLSX';
        note.innerHTML = '<span class="warn">HTTP ' + res.status + '</span>';
        return;
      }}
      const buf = await res.arrayBuffer();
      const wb = XLSX.read(buf, {{ type: 'array' }});
      sel.innerHTML = wb.SheetNames.map(n => '<option>' + n.replaceAll('&','&amp;').replaceAll('<','&lt;') + '</option>').join('');

      function renderSheet(name) {{
        const ws = wb.Sheets[name];
        if (!ws) return;
        // Use SheetJS HTML generator (table only)
        const html = XLSX.utils.sheet_to_html(ws, {{ id: 'sheetTable', editable: false }});
        out.innerHTML = html;
        status.textContent = 'Loaded';
      }}

      sel.addEventListener('change', () => renderSheet(sel.value));
      renderSheet(wb.SheetNames[0]);
    }}
    main().catch(e => {{
      document.getElementById('status').textContent = 'Error';
      document.getElementById('note').innerHTML = '<span class="warn">' + (e?.message || String(e)) + '</span>';
    }});
  </script>
</body>
</html>
"""


def _write_tabular_viewers(out_phases_dir: Path) -> None:
    """
    For each *.csv/*.xlsx in docs/phases, write a sibling viewer page:
      foo.csv.html, foo.xlsx.html
    """
    for p in sorted(out_phases_dir.rglob("*")):
        if not p.is_file():
            continue
        if p.name in SKIP_NAMES:
            continue
        ext = p.suffix.lower()
        if ext not in TABULAR_EXTS:
            continue
        viewer = p.with_name(p.name + ".html")
        if ext == ".csv":
            _write_text(viewer, _render_csv_viewer_html(p.name))
        else:
            _write_text(viewer, _render_xlsx_viewer_html(p.name))


def _build_outline_html(*, repo_root: Path, docs_dir: Path) -> None:
    """
    Generate a standalone HTML version of the main Markdown outline under:
      docs/outline/index.html
    """
    src = repo_root / "EV Charging Project Plan Outline.md"
    out_dir = docs_dir / "outline"
    out_html = out_dir / "index.html"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Pandoc's default HTML template uses a very narrow max-width (36em) and large padding.
    # Provide a light override: readable, but not edge-to-edge.
    css_path = out_dir / "outline.css"
    _write_text(
        css_path,
        """
/* EEIntake outline HTML tweaks (overrides Pandoc defaults) */
html { background-color: #fff; }
body {
  max-width: 1100px;
  margin: 0 auto;
  padding: 28px 20px;
  line-height: 1.45;
}
@media (min-width: 1400px) {
  body { max-width: 1200px; }
}
@media (max-width: 600px) {
  body { padding: 14px 12px; }
}
table { width: 100%; }
pre { padding: 10px 12px; border-radius: 8px; background: #f6f6f6; }
code { background: #f6f6f6; padding: 1px 4px; border-radius: 4px; }
""".lstrip(),
    )

    meta_path = out_dir / "meta.html"
    _write_text(meta_path, ROBOTS_META + "\n")

    cmd = [
        "pandoc",
        str(src),
        "--from",
        "markdown+pipe_tables+table_captions",
        "--to",
        "html",
        "--standalone",
        "--metadata",
        "title=EV Charging Project Plan Outline",
        "--css",
        "outline.css",
        "--include-in-header",
        "meta.html",
        "--resource-path",
        ".",
        "-o",
        str(out_html),
    ]
    # Run with cwd set to output dir so the css href is local.
    # Use absolute paths for input/output so this still works.
    subprocess.run(cmd, check=True, cwd=str(out_dir))


def _write_robots_txt(docs_dir: Path) -> None:
    # Disallow all crawling for the entire Pages site.
    _write_text(
        docs_dir / "robots.txt",
        "User-agent: *\nDisallow: /\n",
    )


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
    _write_robots_txt(docs_dir)

    artifacts = _copy_tree_excluding(phases_dir, out_phases_dir)

    galleries: list[Gallery] = []
    for zip_path in sorted(phases_dir.rglob("*.zip")):
        if zip_path.name in SKIP_NAMES:
            continue
        g = _extract_zip_images_to_gallery(phases_dir=phases_dir, zip_path=zip_path, galleries_dir=galleries_dir)
        if g is not None:
            galleries.append(g)

    # In-browser viewers for CSV/XLSX to avoid forced downloads.
    _write_tabular_viewers(out_phases_dir)

    # Directory listing indexes for phases artifacts
    _write_directory_indexes(docs_dir=docs_dir, out_root=out_phases_dir)

    # HTML version of the outline (not at site root)
    _build_outline_html(repo_root=_repo_root(), docs_dir=docs_dir)

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

