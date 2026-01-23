from __future__ import annotations

import re
from pathlib import Path


HEADING_WITH_PCODE = re.compile(
    r"^(?P<hashes>#{2,6})\s+(?P<section>\d+(?:\.\d+)*)\s+(?P<pcode>P[0-7]\.\d+)\s+(?P<rest>.+)$"
)


def main() -> None:
    path = Path("EV Charging Project Plan Outline.md")
    lines = path.read_text(encoding="utf-8").splitlines()

    out: list[str] = []
    changed = 0

    for line in lines:
        m = HEADING_WITH_PCODE.match(line)
        if not m:
            out.append(line)
            continue

        hashes = m.group("hashes")
        section = m.group("section")
        rest = m.group("rest").strip()

        # Drop the P0.4/P1.2/etc token from headings; keep section number.
        out.append(f"{hashes} {section} {rest}")
        changed += 1

    path.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
    print(f"Updated headings: removed P-codes from {changed} heading(s)")


if __name__ == "__main__":
    main()

