from __future__ import annotations

import re
from pathlib import Path


HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")


def strip_md_bold(s: str) -> str:
    t = s.strip()
    # Remove outer **...**
    m = re.fullmatch(r"\*\*(.+?)\*\*", t)
    if m:
        t = m.group(1).strip()
    # Also remove any remaining '**' used for emphasis inside headings
    t = t.replace("**", "")
    # Normalize whitespace
    t = re.sub(r"\s{2,}", " ", t).strip()
    return t


def strip_leading_section_number(title: str) -> str:
    # Remove leading "4.1 " or "3.1.2 " etc
    return re.sub(r"^\d+(?:\.\d+)*\s+", "", title).strip()


def is_phase_heading_line(title: str) -> re.Match[str] | None:
    # e.g. "4 Phase 0 (P0): Foo {#phase-0}"
    return re.fullmatch(r"\d+\s+Phase\s+([0-7])\s+\(P\d\):\s+(.+?)\s+\{#phase-(\d)\}\s*", title)


def normalize_phase_heading(section_num: int, phase_num: int, phase_title: str, anchor_n: str) -> str:
    return f"## {section_num} Phase {phase_num} (P{phase_num}): {phase_title} {{#phase-{anchor_n}}}"


def classify_minor_heading(title: str) -> bool:
    """
    Return True if this should be treated as a minor subsection under the current major.
    Heuristic: headings that are category/details under a parent (site plans, photos, etc).
    """
    t = title.lower()
    # Common sub-detail headings in the doc
    minor_starts = (
        "site plans",
        "panel schedules",
        "photos",
        "charger skus",
        "authority having jurisdiction",
        "package contents",
        "inputs used",
        "method",
        "system architecture proposal",
        "decision",
        "deficiency received",
        "rework package",
        "resubmission + approval",
        "as-built change log",
        "revision log",
        "how changes were crafted",
        "submission confirmation excerpt",
        "stamped set excerpt",
        "ahj comment themes excerpt",
        "revision summary excerpt",
        "ahj approval excerpt",
        "utility load letter excerpt",
        "utility submission receipt excerpt",
        "utility deficiency notice excerpt",
        "load calc summary excerpt",
        "independent check excerpt",
        "architecture decision excerpt",
        "one-line diagram excerpt",
        "site plan w/ evse locations excerpt",
        "conduit & trenching details excerpt",
        "drawing set compilation excerpt",
        "utility source and fault data",
        "panel and protection ratings",
        "feeder conductors",
        "wiring method",
        "grounding and bonding",
        "energy management system",
        "coordination and selectivity",
    )
    return any(t.startswith(x) for x in minor_starts)


def should_force_major(title: str, phase_num: int | None) -> bool:
    """
    Major subsections should include deliverables (P?.x), phase boundaries/purpose, logs, etc.
    """
    base = title.strip()
    if re.match(rf"^P{phase_num}\.\d+\b", base) if phase_num is not None else False:
        return True
    if base.startswith("P0.") or base.startswith("P1.") or base.startswith("P2.") or base.startswith("P3.") or base.startswith("P4.") or base.startswith("P5.") or base.startswith("P6.") or base.startswith("P7."):
        return True
    if base.startswith("Phase "):
        return True
    if base.startswith("IMPORTANT:"):
        return True
    if base in ("Next Steps", "Key Excerpts (Electrical-Only)", "Required Input Details", "Data Standardization Certification"):
        return True
    if "Evidence Index" in base or "Submission" in base or "Certification" in base or "Closeout" in base or "QA Log" in base or "Coordination Log" in base:
        return True
    return False


def main() -> None:
    path = Path("EV Charging Project Plan Outline.md")
    lines = path.read_text(encoding="utf-8").splitlines()

    out: list[str] = []

    # Track current top-level section (2nd-level headings)
    section_num = 0
    current_phase: int | None = None

    # Phase-local numbering
    major_idx = 0
    minor_idx = 0

    # Addendum numbering
    add_num: int | None = None
    add_phase_count = 0

    # Overview state
    in_overview = False
    in_overview_phase_list = False
    overview_phase_count = 0

    for raw in lines:
        m = HEADING_RE.match(raw)
        if not m:
            out.append(raw)
            continue

        level = len(m.group(1))
        title = m.group(2)

        # Title H1 stays as-is (but strip bold if present)
        if level == 1:
            out.append(f"# {strip_md_bold(strip_leading_section_number(title))}")
            continue

        # Normalize major document sections (level 2)
        if level == 2:
            t = strip_md_bold(strip_leading_section_number(title))

            # Reset section context
            current_phase = None
            major_idx = 0
            minor_idx = 0
            add_num = None
            in_overview_phase_list = False

            if t == "Executive Summary":
                section_num = 1
                out.append("## 1 Executive Summary")
                continue
            if t.startswith("Table of Contents"):
                section_num = 2
                # Preserve anchor if present
                anchor = "{#table-of-contents}" if "{#table-of-contents}" in title else ""
                out.append(f"## 2 Table of Contents {anchor}".rstrip())
                continue
            if t == "Overview":
                section_num = 3
                out.append("## 3 Overview")
                in_overview = True
                overview_phase_count = 0
                continue

            # Phase headings
            ph = is_phase_heading_line(title)
            if ph:
                current_phase = int(ph.group(1))
                section_num = 4 + current_phase
                phase_title = strip_md_bold(ph.group(2))
                out.append(normalize_phase_heading(section_num, current_phase, phase_title, ph.group(3)))
                major_idx = 0
                minor_idx = 0
                in_overview = False
                continue

            # Addenda
            if t.startswith("Addendum A:"):
                section_num = 12
                add_num = 12
                add_phase_count = 0
                out.append("## 12 Addendum A: Stable Filename Index (by Phase) {#addendum-a}")
                in_overview = False
                continue
            if t.startswith("Addendum B:"):
                section_num = 13
                add_num = 13
                add_phase_count = 0
                out.append("## 13 Addendum B: Party Directory (Roles + Contacts) {#addendum-b}")
                in_overview = False
                continue

            # Any other level-2 sections (fallback numbering)
            section_num += 1
            out.append(f"## {section_num} {t}")
            continue

        # Overview subsections numbering
        if level == 3 and strip_md_bold(strip_leading_section_number(title)).startswith("Phase Overview"):
            out.append("### 3.1 Phase Overview (Deliverables by Phase) {#phase-overview}")
            in_overview_phase_list = True
            continue

        # Overview phase list headings
        if in_overview and in_overview_phase_list and level == 4:
            t = strip_md_bold(strip_leading_section_number(title))
            m_ov = re.fullmatch(r"Phase\s+([0-7]):\s+(.+)", t)
            if m_ov:
                overview_phase_count += 1
                p = int(m_ov.group(1))
                rest = m_ov.group(2).strip()
                out.append(f"#### 3.1.{overview_phase_count} Phase {p}: {rest}")
                continue

        # Addendum subheads "Phase X (PX) — ..." number them
        if add_num is not None and level == 3:
            t = strip_md_bold(strip_leading_section_number(title))
            m_add = re.fullmatch(r"Phase\s+([0-7])\s+\(P\d\)\s+—\s+(.+)", t)
            if m_add:
                add_phase_count += 1
                p = int(m_add.group(1))
                rest = m_add.group(2).strip()
                out.append(f"### {add_num}.{add_phase_count} Phase {p} (P{p}) — {rest}")
                continue
            # Other addendum headings
            add_phase_count += 1
            out.append(f"### {add_num}.{add_phase_count} {t}")
            continue

        # Inside a Phase section: renumber headings consistently
        if current_phase is not None:
            t = strip_md_bold(strip_leading_section_number(title))
            sec_prefix = f"{section_num}."

            if level == 3:
                # Decide major vs minor
                if should_force_major(t, current_phase) and not classify_minor_heading(t):
                    major_idx += 1
                    minor_idx = 0
                    out.append(f"### {sec_prefix}{major_idx} {t}")
                else:
                    if major_idx == 0:
                        major_idx = 1
                    minor_idx += 1
                    out.append(f"#### {sec_prefix}{major_idx}.{minor_idx} {t}")
                continue

            if level >= 4:
                # Promote deliverable-like headings to major even if they were deeper
                if should_force_major(t, current_phase) and not classify_minor_heading(t):
                    major_idx += 1
                    minor_idx = 0
                    out.append(f"### {sec_prefix}{major_idx} {t}")
                else:
                    if major_idx == 0:
                        major_idx = 1
                    minor_idx += 1
                    # Keep at level-4 for consistency (avoid too-deep heading sizes)
                    out.append(f"#### {sec_prefix}{major_idx}.{minor_idx} {t}")
                continue

        # Non-phase headings (generic): strip bold but keep level
        t = strip_md_bold(strip_leading_section_number(title))
        out.append(f"{'#' * level} {t}")

    text = "\n".join(out).rstrip() + "\n"

    # Refresh Table of Contents labels to match the new numbering scheme
    toc_block = "\n".join(
        [
            "## 2 Table of Contents {#table-of-contents}",
            "",
            "- [3.1 Phase Overview (Deliverables by Phase)](#phase-overview)",
            "- [4 Phase 0 (P0): Project Initiation and Feasibility](#phase-0)",
            "- [5 Phase 1 (P1): Data Collection and Site Analysis](#phase-1)",
            "- [6 Phase 2 (P2): System Design and Load Calculation](#phase-2)",
            "- [7 Phase 3 (P3): Preliminary Drawing Set Production](#phase-3)",
            "- [8 Phase 4 (P4): Permitting Submission](#phase-4)",
            "- [9 Phase 5 (P5): Authority Review and Drawing Revision](#phase-5)",
            "- [10 Phase 6 (P6): Utility Coordination](#phase-6)",
            "- [11 Phase 7 (P7): Electrical Closeout and Handover](#phase-7)",
            "- [12 Addendum A: Stable Filename Index (by Phase)](#addendum-a)",
            "- [13 Addendum B: Party Directory (Roles + Contacts)](#addendum-b)",
            "",
            "",
        ]
    )
    text = re.sub(
        r"## 2 Table of Contents\s*\{#table-of-contents\}\s*\n(?:- .*\n)+\n",
        toc_block,
        text,
        flags=re.MULTILINE,
    )

    path.write_text(text, encoding="utf-8")
    print("Renumbered sections (first pass):", path)


if __name__ == "__main__":
    main()

