#!/usr/bin/env bash
set -euo pipefail

IN="EV Charging Project Plan Outline.md"
OUT="exports/EV Charging Project Plan Outline.pdf"

pandoc "$IN" \
  --from markdown+pipe_tables+table_captions \
  --pdf-engine=xelatex \
  --toc \
  --toc-depth=2 \
  --resource-path="." \
  --include-in-header="scripts/pandoc/header.tex" \
  -V colorlinks=true \
  -V urlcolor=blue \
  -V linkcolor=blue \
  -V fontsize=10pt \
  -V mainfont="Arial" \
  -o "$OUT"

echo "Wrote: $OUT"

