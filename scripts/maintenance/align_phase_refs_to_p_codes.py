from __future__ import annotations

import re
from pathlib import Path


# Patterns like:
#   Phase 2 / P1.1
#   Phase 3 (P2.1 NEC Load Calculation)
#   Phase 3 (P2.1/P2.2)
PHASE_SLASH_P = re.compile(r"\bPhase\s+(?P<phase>\d+)\s*/\s*P(?P<p>\d)\.(?P<sub>\d+)\b")
PHASE_PAREN_P = re.compile(r"\bPhase\s+(?P<phase>\d+)\s*\(\s*P(?P<p>\d)\.(?P<sub>\d+)")


def main() -> None:
    path = Path("EV Charging Project Plan Outline.md")
    s = path.read_text(encoding="utf-8")

    changed = 0

    def fix_slash(m: re.Match[str]) -> str:
        nonlocal changed
        p = int(m.group("p"))
        correct_phase = p + 1
        if int(m.group("phase")) != correct_phase:
            changed += 1
        return f"Phase {correct_phase} / P{p}.{m.group('sub')}"

    def fix_paren(m: re.Match[str]) -> str:
        nonlocal changed
        p = int(m.group("p"))
        correct_phase = p + 1
        if int(m.group("phase")) != correct_phase:
            changed += 1
        # keep rest of paren as-is
        return f"Phase {correct_phase} (P{p}.{m.group('sub')}"

    s2 = PHASE_SLASH_P.sub(fix_slash, s)
    s3 = PHASE_PAREN_P.sub(fix_paren, s2)

    path.write_text(s3, encoding="utf-8")
    print(f"Aligned Phase refs to P-codes; corrected {changed} occurrence(s).")


if __name__ == "__main__":
    main()

