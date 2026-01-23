from __future__ import annotations

import re
from pathlib import Path


def main() -> None:
    path = Path("EV Charging Project Plan Outline.md")
    lines = path.read_text(encoding="utf-8").splitlines()

    out: list[str] = []
    inserted_blank_before_list = 0
    fixed_nested_bullets = 0
    fixed_excerpt_spacing = 0

    i = 0
    while i < len(lines):
        line = lines[i]

        # Fix "( excerpt)" -> "(excerpt)"
        if "( excerpt)" in line:
            line = line.replace("( excerpt)", "(excerpt)")
            fixed_excerpt_spacing += 1

        out.append(line)

        # Ensure a blank line before lists when they follow normal text.
        # Pandoc markdown-to-DOCX is picky: without a blank line, a '-' list can be flattened
        # into the prior paragraph (seen in "Excerpted ... fields" blocks).
        if i + 1 < len(lines):
            nxt = lines[i + 1]
            looks_like_list = (
                nxt.startswith("- ")
                or nxt.startswith("* ")
                or re.match(r"^\s{2,}-\s", nxt)
                or re.match(r"^\s{2,}\*\s", nxt)
            )

            prev_is_blank = len(line.strip()) == 0
            prev_is_list = re.match(r"^\s*[-*]\s", line) is not None
            prev_is_table = line.startswith("|")
            prev_is_heading = re.match(r"^#{1,6}\s", line) is not None

            if looks_like_list and not prev_is_blank and not prev_is_list and not prev_is_table and not prev_is_heading:
                out.append("")
                inserted_blank_before_list += 1

        # Fix bullets that start with exactly one leading space (" - item")
        # - If they follow any bullet, treat as nested under that bullet.
        # - Otherwise, treat as a top-level bullet (remove the stray leading space).
        if i + 1 < len(lines):
            nxt = lines[i + 1]
            if re.match(r"^ - ", nxt):
                if re.match(r"^\s*- ", line):
                    # Match indentation level of the current bullet line.
                    indent = len(line) - len(line.lstrip(" "))
                    indent = max(indent, 2)  # nested bullets should have at least 2 spaces
                    lines[i + 1] = (" " * indent) + nxt.lstrip()
                else:
                    lines[i + 1] = nxt.lstrip()
                fixed_nested_bullets += 1

        i += 1

    path.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
    print(
        "Inserted blank lines before lists:",
        inserted_blank_before_list,
        "| Fixed nested bullets:",
        fixed_nested_bullets,
        "| Fixed '(excerpt)' spacing:",
        fixed_excerpt_spacing,
    )


if __name__ == "__main__":
    main()

