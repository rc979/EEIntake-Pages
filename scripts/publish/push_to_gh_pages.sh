#!/bin/bash
# Push gh-pages-ready folder to GitHub Pages repo
# This script should be run outside the sandbox (in regular Terminal)

set -e

REPO_NAME="${1:-EEIntake-Pages}"
GITHUB_USER="${2:-rc979}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PAGES_DIR="$PROJECT_ROOT/gh-pages-ready"

if [ ! -d "$PAGES_DIR" ]; then
    echo "Error: gh-pages-ready directory not found"
    echo "Run: ./scripts/publish/prepare_gh_pages.sh first"
    exit 1
fi

TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

echo "Cloning $REPO_NAME..."
git clone "https://github.com/${GITHUB_USER}/${REPO_NAME}.git" "$TEMP_DIR"

cd "$TEMP_DIR"

echo "Copying files..."
find . -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +
cp -r "$PAGES_DIR"/* .

echo "Committing..."
git add -A
git commit -m "Deploy GitHub Pages site $(date +%Y-%m-%d)" || echo "No changes"

echo "Pushing..."
git push origin main

echo ""
echo "✅ Pushed to GitHub!"
echo ""
echo "Now enable GitHub Pages:"
echo "1. Go to: https://github.com/${GITHUB_USER}/${REPO_NAME}/settings/pages"
echo "2. Source: Deploy from a branch"
echo "3. Branch: main"
echo "4. Folder: / (root)"
echo "5. Click Save"
echo ""
echo "Site will be at: https://${GITHUB_USER}.github.io/${REPO_NAME}/"
