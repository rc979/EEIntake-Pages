#!/usr/bin/env bash
set -euo pipefail

IN="EV Charging Project Plan Outline.md"
OUT="docs/outline/index.html"
CSS_OUT="docs/outline/outline.css"
MANIFEST="docs/publish_manifest.json"

# 1) Rewrite markdown links to point at published GitHub Pages URLs
# This edits the markdown in-place, so we work on a temp copy
TEMP_MD=$(mktemp)
cp "$IN" "$TEMP_MD"

python3 "scripts/publish/linkify_outline_public_urls.py" \
  --md "$TEMP_MD" \
  --manifest "$MANIFEST" \
  --base-url "https://rc979.github.io/EEIntake"

# 2) Pandoc export to HTML
pandoc "$TEMP_MD" \
  --from markdown+pipe_tables+table_captions \
  --to html5 \
  --standalone \
  --toc \
  --toc-depth=2 \
  --resource-path="." \
  --css="outline.css" \
  --metadata title="EV Charging Project Plan Outline" \
  -V "pagetitle=EV Charging Project Plan Outline" \
  -o "$OUT"

# 3) Inject robots meta tag (pandoc doesn't have a direct flag for this)
# We do this after pandoc because --metadata doesn't reliably inject meta tags
sed -i '' 's|<meta name="generator"|<meta name="robots" content="noindex, nofollow">\n  <meta name="generator"|' "$OUT"

# 4) Ensure CSS exists (pandoc will reference it)
if [ ! -f "$CSS_OUT" ]; then
  cat > "$CSS_OUT" <<'EOF'
/* Minimal outline styles */
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  line-height: 1.6;
  max-width: 900px;
  margin: 0 auto;
  padding: 24px;
}
h1, h2, h3, h4, h5, h6 {
  margin-top: 1.5em;
  margin-bottom: 0.5em;
}
table {
  border-collapse: collapse;
  width: 100%;
  margin: 1em 0;
}
th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}
th {
  background-color: #f5f5f5;
}
code {
  background: #f6f6f6;
  padding: 2px 4px;
  border-radius: 3px;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
}
a {
  color: #0b57d0;
  text-decoration: none;
}
a:hover {
  text-decoration: underline;
}
EOF
fi

# Cleanup temp file
rm -f "$TEMP_MD"

echo "Wrote: $OUT"
echo "CSS: $CSS_OUT"
