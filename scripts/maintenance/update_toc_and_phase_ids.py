from __future__ import annotations

import re
from pathlib import Path


TOC_START = re.compile(r"^## Table of Contents\s*$", re.MULTILINE)


def replace_toc(md: str) -> str:
    # Replace from "## Table of Contents" up to (but not including) the next "## Overview"
    m_start = TOC_START.search(md)
    if not m_start:
        return md

    start_idx = m_start.start()
    m_overview = re.search(r"^## Overview\s*$", md[m_start.end() :], flags=re.MULTILINE)
    if not m_overview:
        return md

    overview_abs = m_start.end() + m_overview.start()

    toc_block = "\n".join(
        [
            "## Table of Contents",
            "",
            "- [Overview](#overview)",
            "- [Phase Overview (Deliverables by Phase)](#phase-overview)",
            "- [Phase 1: Project Initiation and Feasibility](#phase-1)",
            "- [Phase 2: Data Collection and Site Analysis](#phase-2)",
            "- [Phase 3: System Design and Load Calculation](#phase-3)",
            "- [Phase 4: Preliminary Drawing Set Production](#phase-4)",
            "- [Phase 5: Permitting Submission](#phase-5)",
            "- [Phase 6: Authority Review and Drawing Revision](#phase-6)",
            "- [Phase 7: Utility Coordination](#phase-7)",
            "- [Phase 8: Electrical Closeout and Handover](#phase-8)",
            "- [Addendum A: Stable Filename Index (by Phase)](#addendum-a)",
            "- [Addendum B: Party Directory (Roles + Contacts)](#addendum-b)",
            "",
            "",
        ]
    )

    return md[:start_idx] + toc_block + md[overview_abs:]


def ensure_overview_anchor(md: str) -> str:
    # Insert <a id="overview"></a> immediately before the Overview heading if missing.
    if re.search(r'^<a id="overview"></a>\s*\n## Overview\s*$', md, flags=re.MULTILINE):
        return md
    return re.sub(r"^## Overview\s*$", '<a id="overview"></a>\n## Overview', md, flags=re.MULTILINE)


def shift_internal_ids(md: str) -> str:
    """
    Shift internal ID prefixes P0-..P7- to phase-indexed IDs 1-..8-.
    Examples:
      P0-A01 -> 1-A01
      P6-W07 -> 7-W07
    Does not touch filenames like P1-I01_SitePlans... because underscore prevents word-boundary match.
    """

    def repl(m: re.Match[str]) -> str:
        p = int(m.group(1))
        kind = m.group(2)
        num = m.group(3)
        return f"{p + 1}-{kind}{num}"

    return re.sub(r"\bP([0-7])-(A|I|W)(\d+)\b", repl, md)


def remove_mixed_phase_p_refs(md: str) -> str:
    # Remove the confusing combined forms: "Phase X / Pn.m" → "Phase X"
    md = re.sub(r"\bPhase\s+(\d+)\s*/\s*P\d\.\d+\b", r"Phase \1", md)
    # Remove leading "P2.1" token inside parentheses when it's immediately after "Phase X ("
    md = re.sub(r"\b(Phase\s+\d+)\s*\(\s*P\d\.\d+\s*", r"\1 (", md)
    return md


def main() -> None:
    path = Path("EV Charging Project Plan Outline.md")
    md = path.read_text(encoding="utf-8")

    md2 = replace_toc(md)
    md2 = ensure_overview_anchor(md2)
    md2 = shift_internal_ids(md2)
    md2 = remove_mixed_phase_p_refs(md2)

    path.write_text(md2.rstrip() + "\n", encoding="utf-8")
    print("Updated TOC + shifted internal IDs + cleaned mixed phase refs:", path)


if __name__ == "__main__":
    main()

