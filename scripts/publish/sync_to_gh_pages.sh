#!/bin/bash
# Sync docs/ folder to a separate GitHub Pages repo
# Usage: ./sync_to_gh_pages.sh [repo-name] [github-user]

set -e

REPO_NAME="${1:-EEIntake-Pages}"
GITHUB_USER="${2:-rc979}"
GH_PAGES_URL="https://${GITHUB_USER}.github.io/${REPO_NAME}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DOCS_DIR="$PROJECT_ROOT/docs"
TEMP_DIR="/tmp/${REPO_NAME}-sync-$$"

echo "=========================================="
echo "Syncing to GitHub Pages Repo"
echo "=========================================="
echo "Repo: $REPO_NAME"
echo "GitHub User: $GITHUB_USER"
echo "Pages URL: $GH_PAGES_URL"
echo ""

# Check if docs directory exists
if [ ! -d "$DOCS_DIR" ]; then
    echo "Error: docs/ directory not found at $DOCS_DIR"
    exit 1
fi

# Clone or update the pages repo
if [ -d "$TEMP_DIR" ]; then
    echo "Cleaning up existing temp directory..."
    rm -rf "$TEMP_DIR"
fi

echo "Cloning GitHub Pages repo..."
git clone "https://github.com/${GITHUB_USER}/${REPO_NAME}.git" "$TEMP_DIR" || {
    echo "Error: Could not clone repo. Make sure:"
    echo "  1. The repo exists: https://github.com/${GITHUB_USER}/${REPO_NAME}"
    echo "  2. You have access to it"
    echo "  3. It's a public repo (required for free GitHub Pages)"
    exit 1
}

cd "$TEMP_DIR"

# Remove everything except .git
echo "Clearing existing files..."
find . -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +

# Copy docs contents
echo "Copying docs/ contents..."
cp -r "$DOCS_DIR"/* .

# Update links in HTML files to point to GitHub Pages
echo "Updating links to GitHub Pages URL..."
find . -name "*.html" -type f | while read -r file; do
    # Update Netlify URLs to GitHub Pages URLs
    sed -i '' "s|https://heroic-sunburst-405f92.netlify.app|${GH_PAGES_URL}|g" "$file"
done

# Commit and push
echo "Committing changes..."
git add -A
git commit -m "Update GitHub Pages site $(date +%Y-%m-%d)" || {
    echo "No changes to commit"
}

echo "Pushing to GitHub..."
git push origin main || {
    echo "Error: Could not push to GitHub"
    exit 1
}

# Cleanup
cd "$PROJECT_ROOT"
rm -rf "$TEMP_DIR"

echo ""
echo "=========================================="
echo "✅ Successfully synced to GitHub Pages!"
echo "=========================================="
echo ""
echo "Your site will be available at:"
echo "  $GH_PAGES_URL"
echo ""
echo "Note: It may take a few minutes for GitHub Pages to build."
echo "Check status at:"
echo "  https://github.com/${GITHUB_USER}/${REPO_NAME}/actions"
echo ""
