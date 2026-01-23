from __future__ import annotations

import re
from pathlib import Path


def shift_phase_refs(text: str) -> str:
    """
    Shift human-facing phase numbers up by +1:
      Phase 0 -> Phase 1 ... Phase 7 -> Phase 8
    Handles common patterns like 'phases (0–7)' -> '(1–8)'.
    Does NOT touch phases/P0/P1 deliverable IDs.
    """

    # Ranges first: phases (0–7) or phases 0-7 etc
    text = re.sub(r"\bphases\s*\(\s*0\s*[–-]\s*7\s*\)", "phases (1–8)", text, flags=re.IGNORECASE)
    text = re.sub(r"\bphases\s+0\s*[–-]\s*7\b", "phases 1–8", text, flags=re.IGNORECASE)

    def repl(m: re.Match[str]) -> str:
        n = int(m.group(1))
        return f"Phase {n + 1}"

    # Single phase mentions
    text = re.sub(r"\bPhase\s+([0-7])\b", repl, text)
    return text


def main() -> None:
    path = Path("EV Charging Project Plan Outline.md")
    lines = path.read_text(encoding="utf-8").splitlines()

    out: list[str] = []

    # Remove visible pagebreak commands from Markdown readability.
    for line in lines:
        if line.strip() == r"\newpage":
            continue
        out.append(line)

    text = "\n".join(out)

    # Remove numbering from Overview heading (and de-number its immediate Phase Overview heading block)
    text = re.sub(r"^##\s+3\s+Overview\s*$", "## Overview", text, flags=re.MULTILINE)
    text = re.sub(
        r"^###\s+3\.1\s+Phase Overview \(Deliverables by Phase\)\s*$",
        "### Phase Overview (Deliverables by Phase)",
        text,
        flags=re.MULTILINE,
    )

    # De-number the Overview phase list headings (3.1.x -> none) while shifting Phase numbers.
    def repl_overview_phase(m: re.Match[str]) -> str:
        phase_n = int(m.group(1))
        title = m.group(2).strip()
        return f"#### Phase {phase_n + 1}: {title}"

    text = re.sub(
        r"^####\s+3\.1\.\d+\s+Phase\s+([0-7]):\s*(.+)$",
        repl_overview_phase,
        text,
        flags=re.MULTILINE,
    )

    # Reindex phase anchors and headings:
    # <a id="phase-0"></a> + '## 4 Phase 0 (P0): X' -> phase-1 and '## 1 Phase 1: X (P0)'
    def repl_phase_block(m: re.Match[str]) -> str:
        old_anchor = int(m.group("anchor"))
        old_section = int(m.group("section"))  # 4..11
        old_phase = int(m.group("phase"))      # 0..7
        pcode = int(m.group("pcode"))          # 0..7
        title = m.group("title").strip()

        new_phase = old_phase + 1
        new_section = old_section - 3  # 4->1 ... 11->8
        new_anchor = old_anchor + 1

        # Keep P-code mapping explicit (Phase 1 corresponds to P0, etc)
        return (
            f'<a id="phase-{new_anchor}"></a>\n'
            f"## {new_section} Phase {new_phase}: {title} (P{pcode})"
        )

    text = re.sub(
        r'^<a id="phase-(?P<anchor>[0-7])"></a>\s*\n'
        r"##\s+(?P<section>(?:4|5|6|7|8|9|10|11))\s+Phase\s+(?P<phase>[0-7])\s+\(P(?P<pcode>[0-7])\):\s+(?P<title>.+)\s*$",
        repl_phase_block,
        text,
        flags=re.MULTILINE,
    )

    # Renumber all subsection prefixes under phase sections: 4.x -> 1.x, 5.x -> 2.x, ... 11.x -> 8.x
    def repl_section_prefix(m: re.Match[str]) -> str:
        hashes = m.group("hashes")
        lead = int(m.group("lead"))
        rest = m.group("rest")
        new_lead = lead - 3
        return f"{hashes} {new_lead}.{rest}"

    text = re.sub(
        r"^(?P<hashes>#{3,6})\s+(?P<lead>4|5|6|7|8|9|10|11)\.(?P<rest>\d+(?:\.\d+)*\s+.+)$",
        repl_section_prefix,
        text,
        flags=re.MULTILINE,
    )

    # Update TOC links (phase-0 -> phase-1 ... phase-7 -> phase-8)
    for i in range(7, -1, -1):
        text = text.replace(f"](#phase-{i})", f"](#phase-{i+1})")

    # Shift narrative "Phase X" references throughout (Phase 0 -> Phase 1, etc)
    text = shift_phase_refs(text)

    path.write_text(text.rstrip() + "\n", encoding="utf-8")
    print("Reindexed phases to start at 1:", path)


if __name__ == "__main__":
    main()

