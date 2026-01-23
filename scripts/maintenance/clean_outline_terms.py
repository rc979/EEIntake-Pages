from __future__ import annotations

import re
from pathlib import Path


def clean_text(s: str) -> str:
    # Remove "mock" (any case) as a standalone word.
    s = re.sub(r"\bmock\b", "", s, flags=re.IGNORECASE)

    # Remove leftover double spaces created by removal.
    s = re.sub(r"[ \t]{2,}", " ", s)

    # Clean common parenthetical remnants like "( )" or "(, )" that can appear after deleting "mock".
    s = re.sub(r"\(\s*\)", "", s)
    s = re.sub(r"\(\s*,\s*\)", "", s)

    # Fix spaces before punctuation.
    s = re.sub(r"\s+([,.;:])", r"\1", s)

    # Normalize some phrases that previously contained mock wording.
    s = s.replace("MOCK / EXAMPLE", "EXAMPLE")
    s = s.replace("Mock", "Example")

    return s


def main() -> None:
    path = Path("EV Charging Project Plan Outline.md")
    original = path.read_text(encoding="utf-8")
    cleaned = clean_text(original)

    # A few manual cleanups for common artifacts.
    cleaned = cleaned.replace(" ( )", "")
    cleaned = cleaned.replace("  \n", "\n")

    path.write_text(cleaned, encoding="utf-8")
    print("Cleaned terms in:", path)


if __name__ == "__main__":
    main()

