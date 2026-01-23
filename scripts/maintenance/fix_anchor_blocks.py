from __future__ import annotations

import re
from pathlib import Path


ANCHOR_LINE = re.compile(r'^<a id="[^"]+"></a>\s*$')


def main() -> None:
    path = Path("EV Charging Project Plan Outline.md")
    lines = path.read_text(encoding="utf-8").splitlines()

    out: list[str] = []
    inserted = 0

    for i, line in enumerate(lines):
        out.append(line)
        if ANCHOR_LINE.match(line):
            # If the next line exists and is not blank, insert a blank line to end the HTML block.
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            if nxt.strip() != "":
                out.append("")
                inserted += 1

    path.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
    print(f"Inserted {inserted} blank line(s) after anchor lines.")


if __name__ == "__main__":
    main()

