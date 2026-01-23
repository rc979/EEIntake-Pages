from __future__ import annotations

import re
from pathlib import Path


def strip_bold_heading(text: str) -> str:
    """
    Convert heading title like '**Foo**' to 'Foo' (and trim).
    """
    t = text.strip()
    # Common pattern: **Title**
    m = re.fullmatch(r"\*\*(.+?)\*\*", t)
    if m:
        return m.group(1).strip()
    return t


def main() -> None:
    path = Path("EV Charging Project Plan Outline.md")
    s = path.read_text(encoding="utf-8")
    lines = s.splitlines()

    out: list[str] = []

    # State for phase-local numbering
    current_phase_num: int | None = None  # 0..7
    current_section_counter = 0  # phase subsection counter (4.1, 4.2, ...)
    current_subsection_counter = 0  # subsub under current subsection (4.6.1, 4.6.2, ...)

    def phase_section_prefix() -> str:
        assert current_phase_num is not None
        return f"{4 + current_phase_num}."

    # For Overview phase list numbering (3.1.1 .. 3.1.8)
    overview_phase_counter = 0

    # Track if we already normalized the title heading
    title_done = False

    # Helper: are we inside overview block (before first Phase 0 section)
    in_overview = True

    for raw in lines:
        line = raw.rstrip("\n")

        # Drop blank headings like "# "
        if re.fullmatch(r"#{1,6}\s*", line):
            continue

        # Remove stray "## Main"
        if line.strip() == "## Main":
            continue

        # Promote doc title to H1 once.
        if not title_done and line.strip() == "## EV Charging Site Project Plan":
            out.append("# EV Charging Site Project Plan")
            title_done = True
            continue

        # Number top-level non-phase headings
        if line.strip() == "## Executive Summary":
            out.append("## 1 Executive Summary")
            continue
        if re.fullmatch(r"## Table of Contents\s*\{#table-of-contents\}\s*", line):
            out.append("## 2 Table of Contents {#table-of-contents}")
            continue
        if line.strip() == "## Overview":
            out.append("## 3 Overview")
            continue

        # Normalize Phase Overview heading under Overview
        if re.fullmatch(r"### Phase Overview \(Deliverables by Phase\)\s*\{#phase-overview\}\s*", line):
            out.append("### 3.1 Phase Overview (Deliverables by Phase) {#phase-overview}")
            continue

        # Within overview: phase mini-headings
        m_overview_phase = re.fullmatch(r"### Phase ([0-7]):\s*(.+)", line)
        if in_overview and m_overview_phase:
            overview_phase_counter += 1
            p = int(m_overview_phase.group(1))
            title = m_overview_phase.group(2).strip()
            out.append(f"#### 3.1.{overview_phase_counter} Phase {p}: {title}")
            continue

        # Detect start of a Phase section (main documentation blocks)
        m_phase = re.fullmatch(r"# Phase ([0-7]):\s*(.+?)\s*\{#phase-(\d)\}\s*", line)
        if m_phase:
            in_overview = False
            current_phase_num = int(m_phase.group(1))
            phase_title = m_phase.group(2).strip()
            anchor_n = m_phase.group(3)
            pn = f"P{current_phase_num}"
            out.append(f"## {4 + current_phase_num} Phase {current_phase_num} ({pn}): {phase_title} {{#phase-{anchor_n}}}")
            current_section_counter = 0
            current_subsection_counter = 0
            continue

        # Number Addenda headings
        if re.fullmatch(r"## Addendum A: Stable Filename Index \(by Phase\)\s*\{#addendum-a\}\s*", line):
            current_phase_num = None
            out.append("## 12 Addendum A: Stable Filename Index (by Phase) {#addendum-a}")
            continue
        if re.fullmatch(r"## Addendum B: Party Directory \(Roles \+ Contacts\)\s*\{#addendum-b\}\s*", line):
            current_phase_num = None
            out.append("## 13 Addendum B: Party Directory (Roles + Contacts) {#addendum-b}")
            continue

        # Number addendum subheadings of the form "### Phase X (PX) — ..."
        m_add_phase = re.fullmatch(r"### Phase ([0-7]) \(P\d\)\s+—\s+(.+)", line)
        if m_add_phase:
            # Determine which addendum we're in by scanning last emitted heading.
            last = next((x for x in reversed(out) if x.startswith("## ")), "")
            add_num = 12 if last.startswith("## 12 ") else 13 if last.startswith("## 13 ") else None
            if add_num is None:
                out.append(line)
            else:
                # Keep original text but add numbering prefix.
                p = int(m_add_phase.group(1))
                rest = m_add_phase.group(2).strip()
                # Use phase index as sub-number (1..8)
                out.append(f"### {add_num}.{p + 1} Phase {p} (P{p}) — {rest}")
            continue

        # Inside a Phase section: normalize pseudo-headings
        if current_phase_num is not None:
            # "## **Title**" -> "### <phase>.<n> Title"
            m_h2_bold = re.fullmatch(r"##\s+(.+)", line)
            if m_h2_bold:
                title = strip_bold_heading(m_h2_bold.group(1))
                current_section_counter += 1
                current_subsection_counter = 0
                out.append(f"### {phase_section_prefix()}{current_section_counter} {title}")
                continue

            # "# **Title**" or "# Title" inside phase -> "#### <phase>.<n>.<m> Title"
            m_h1_in_phase = re.fullmatch(r"#\s+(.+)", line)
            if m_h1_in_phase:
                title = strip_bold_heading(m_h1_in_phase.group(1))
                # If we haven't seen a subsection yet, create one.
                if current_section_counter == 0:
                    current_section_counter = 1
                current_subsection_counter += 1
                out.append(
                    f"#### {phase_section_prefix()}{current_section_counter}.{current_subsection_counter} {title}"
                )
                continue

        out.append(line)

    path.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
    print("Updated headings (first pass):", path)


if __name__ == "__main__":
    main()

