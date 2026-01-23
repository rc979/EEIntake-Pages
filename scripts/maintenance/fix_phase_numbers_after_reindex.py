from __future__ import annotations

import re
from pathlib import Path


PHASE_H2 = re.compile(r"^(##)\s+(\d+)\s+Phase\s+(\d+):\s+(.+)$")
OVERVIEW_H4 = re.compile(r"^(####)\s+Phase\s+(\d+):\s+(.+)$")


def main() -> None:
    path = Path("EV Charging Project Plan Outline.md")
    lines = path.read_text(encoding="utf-8").splitlines()

    out: list[str] = []

    # Fix H2 phase section headings: make phase number match section number.
    for line in lines:
        m = PHASE_H2.match(line)
        if m:
            hashes, sec, _phase, rest = m.groups()
            out.append(f"{hashes} {sec} Phase {sec}: {rest}")
        else:
            out.append(line)

    # Fix Overview phase list numbering to 1..8 in order.
    lines2 = out
    out2: list[str] = []

    in_overview_list = False
    counter = 0
    for line in lines2:
        if line.strip() == "### Phase Overview (Deliverables by Phase)":
            in_overview_list = True
            counter = 0
            out2.append(line)
            continue

        if in_overview_list:
            if line.startswith("<a id=\"phase-1\""):
                in_overview_list = False
                out2.append(line)
                continue

            m = OVERVIEW_H4.match(line)
            if m:
                hashes, _old, rest = m.groups()
                counter += 1
                out2.append(f"{hashes} Phase {counter}: {rest}")
                continue

        out2.append(line)

    path.write_text("\n".join(out2).rstrip() + "\n", encoding="utf-8")
    print("Fixed phase numbers in headings:", path)


if __name__ == "__main__":
    main()

