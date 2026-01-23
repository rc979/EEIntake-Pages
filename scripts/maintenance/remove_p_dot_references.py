from __future__ import annotations

import re
from pathlib import Path


PDOT = re.compile(r"\bP([0-7])\.(\d+)\b")


def main() -> None:
    path = Path("EV Charging Project Plan Outline.md")
    s = path.read_text(encoding="utf-8")

    def repl(m: re.Match[str]) -> str:
        phase = int(m.group(1)) + 1
        # Intentionally drop the sub-id; keep human-facing phase reference.
        return f"Phase {phase}"

    s2, n = PDOT.subn(repl, s)

    path.write_text(s2, encoding="utf-8")
    print(f"Removed P#.## references (converted to Phase N): {n} replacements")


if __name__ == "__main__":
    main()

