#!/usr/bin/env bash
set -euo pipefail

IN="EV Charging Project Plan Outline.md"
RAW_OUT="exports/EV Charging Project Plan Outline.raw.docx"
OUT="exports/EV Charging Project Plan Outline.docx"

# 1) Pandoc export (raw)
pandoc "$IN" \
  --from markdown+pipe_tables+table_captions \
  --to docx \
  --resource-path="." \
  -o "$RAW_OUT"

# 2) Post-process to enforce:
# - small printable margins (0.35")
# - keep headings with following text
# - repeat table header row across pages
python3 "postprocess_docx.py"

echo "Wrote: $OUT"
