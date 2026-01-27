#!/bin/bash
# Prepare docs/ folder for GitHub Pages push
# This creates a ready-to-push directory you can manually sync

set -e

REPO_NAME="${1:-EEIntake-Pages}"
GITHUB_USER="${2:-rc979}"
GH_PAGES_URL="https://${GITHUB_USER}.github.io/${REPO_NAME}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DOCS_DIR="$PROJECT_ROOT/docs"
OUTPUT_DIR="$PROJECT_ROOT/gh-pages-ready"

echo "=========================================="
echo "Preparing GitHub Pages Files"
echo "=========================================="
echo "Repo: $REPO_NAME"
echo "GitHub User: $GITHUB_USER"
echo "Pages URL: $GH_PAGES_URL"
echo ""

# Clean and create output directory
if [ -d "$OUTPUT_DIR" ]; then
    echo "Cleaning existing output directory..."
    rm -rf "$OUTPUT_DIR"
fi
mkdir -p "$OUTPUT_DIR"

# Copy docs contents
echo "Copying docs/ contents..."
cp -r "$DOCS_DIR"/* "$OUTPUT_DIR/"

# Update links in HTML files
echo "Updating links to GitHub Pages URL..."
find "$OUTPUT_DIR" -name "*.html" -type f | while read -r file; do
    sed -i '' "s|https://heroic-sunburst-405f92.netlify.app|${GH_PAGES_URL}|g" "$file"
done

# Create README with instructions
cat > "$OUTPUT_DIR/README.md" <<EOF
# EE Intake - GitHub Pages Site

This is the public GitHub Pages site for the EE Intake project artifacts.

## To Deploy:

1. Clone this repo (or initialize if empty):
   \`\`\`bash
   git clone https://github.com/${GITHUB_USER}/${REPO_NAME}.git
   cd ${REPO_NAME}
   \`\`\`

2. Copy all files from the \`gh-pages-ready\` folder to the repo root:
   \`\`\`bash
   cp -r /path/to/EEIntake/gh-pages-ready/* .
   \`\`\`

3. Commit and push:
   \`\`\`bash
   git add .
   git commit -m "Initial GitHub Pages deployment"
   git push origin main
   \`\`\`

4. Enable GitHub Pages:
   - Go to: https://github.com/${GITHUB_USER}/${REPO_NAME}/settings/pages
   - Source: Deploy from a branch
   - Branch: main
   - Folder: / (root)
   - Click Save

Site will be available at: ${GH_PAGES_URL}
EOF

echo ""
echo "=========================================="
echo "✅ Files prepared!"
echo "=========================================="
echo ""
echo "Files ready in: $OUTPUT_DIR"
echo ""
echo "Next steps:"
echo "1. Open Terminal (outside Cursor/sandbox)"
echo "2. Run:"
echo "   cd ~/Downloads"
echo "   git clone https://github.com/${GITHUB_USER}/${REPO_NAME}.git"
echo "   cd ${REPO_NAME}"
echo "   cp -r \"$OUTPUT_DIR\"/* ."
echo "   git add ."
echo "   git commit -m 'Initial GitHub Pages deployment'"
echo "   git push origin main"
echo ""
echo "3. Enable GitHub Pages:"
echo "   https://github.com/${GITHUB_USER}/${REPO_NAME}/settings/pages"
echo ""
