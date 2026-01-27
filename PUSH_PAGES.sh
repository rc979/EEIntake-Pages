#!/bin/bash
# Quick script to push gh-pages-ready to GitHub Pages repo
# Run this in Terminal (outside Cursor)

cd ~/Downloads
git clone https://github.com/rc979/EEIntake-Pages.git
cd EEIntake-Pages
cp -r "/Users/rc/Library/Mobile Documents/com~apple~CloudDocs/!DevProjects/EEIntake/gh-pages-ready"/* .
git add .
git commit -m "Deploy GitHub Pages site"
git push origin main

echo ""
echo "✅ Pushed! Now enable Pages:"
echo "https://github.com/rc979/EEIntake-Pages/settings/pages"
echo "Source: GitHub Actions (or Deploy from branch: main, /)"
