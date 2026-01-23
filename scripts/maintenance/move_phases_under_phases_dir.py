from __future__ import annotations

import re
import shutil
from pathlib import Path


def rewrite_paths_in_markdown(md_path: Path) -> int:
    """
    Rewrite evidence pointer paths like:
      phases/P4/Outputs/...  -> phases/phases/P4/Outputs/...
      phases/P0/Inputs/...   -> phases/phases/P0/Inputs/...
    Avoid touching tokens like P0-I01 (no slash).
    """
    s = md_path.read_text(encoding="utf-8")
    s2, n = re.subn(r"(?<![A-Za-z0-9])P([0-7])/", r"phases/P\1/", s)
    if n:
        md_path.write_text(s2, encoding="utf-8")
    return n


def rewrite_paths_in_scripts(scripts_dir: Path) -> int:
    """
    Update generator scripts to output into phases/P# instead of P# at repo root.
    Conservative: only rewrite string literals containing 'P#/...' patterns.
    """
    total = 0
    for path in scripts_dir.rglob("*.py"):
        s = path.read_text(encoding="utf-8")
        s2, n = re.subn(r"(?<![A-Za-z0-9])P([0-7])/", r"phases/P\1/", s)
        if n:
            path.write_text(s2, encoding="utf-8")
            total += n
    return total


def main() -> None:
    root = Path(".").resolve()
    phases_dir = root / "phases"
    phases_dir.mkdir(exist_ok=True)

    # Move P0..P7 into phases/
    moved = 0
    for i in range(0, 8):
        src = root / f"P{i}"
        dst = phases_dir / f"P{i}"
        if src.exists() and src.is_dir() and not dst.exists():
            shutil.move(str(src), str(dst))
            moved += 1

    md_path = root / "EV Charging Project Plan Outline.md"
    md_rewrites = rewrite_paths_in_markdown(md_path)

    scripts_rewrites = rewrite_paths_in_scripts(root / "scripts")

    print(f"Moved phase dirs: {moved}")
    print(f"Markdown path rewrites: {md_rewrites}")
    print(f"Script path rewrites: {scripts_rewrites}")


if __name__ == "__main__":
    main()

