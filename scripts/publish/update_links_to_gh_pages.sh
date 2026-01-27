#!/bin/bash
# Update all links in the markdown and HTML to point to GitHub Pages
# Usage: ./update_links_to_gh_pages.sh [repo-name] [github-user]

set -e

REPO_NAME="${1:-EEIntake-Pages}"
GITHUB_USER="${2:-rc979}"
GH_PAGES_URL="https://${GITHUB_USER}.github.io/${REPO_NAME}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "Updating links to GitHub Pages: $GH_PAGES_URL"

# Update markdown file
python3 "$SCRIPT_DIR/linkify_outline_public_urls.py" \
  --base-url "$GH_PAGES_URL" \
  --md "$PROJECT_ROOT/EV Charging Project Plan Outline.md"

# Regenerate HTML
cd "$PROJECT_ROOT"
./export_html.sh

echo "✅ Links updated to GitHub Pages URL"
