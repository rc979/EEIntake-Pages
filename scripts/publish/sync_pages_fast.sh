#!/bin/bash
# Fast sync to GitHub Pages using GitHub Actions workflow
# This triggers a workflow that syncs from the main repo

set -e

REPO_NAME="${1:-EEIntake-Pages}"
GITHUB_USER="${2:-rc979}"

echo "Triggering GitHub Actions workflow to sync Pages repo..."
gh workflow run sync-from-main.yml --repo ${GITHUB_USER}/${REPO_NAME}

echo ""
echo "✅ Workflow triggered!"
echo "Check status: https://github.com/${GITHUB_USER}/${REPO_NAME}/actions"
echo ""
echo "The workflow will:"
echo "1. Checkout the Pages repo"
echo "2. Checkout the main EEIntake repo"
echo "3. Copy files from gh-pages-ready/ to Pages repo"
echo "4. Commit and push automatically"
echo ""
echo "Site: https://${GITHUB_USER}.github.io/${REPO_NAME}/"
