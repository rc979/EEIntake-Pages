# EE Intake - GitHub Pages Site

This is the public GitHub Pages site for the EE Intake project artifacts.

## To Deploy:

1. Clone this repo (or initialize if empty):
   ```bash
   git clone https://github.com/rc979/EEIntake-Pages.git
   cd EEIntake-Pages
   ```

2. Copy all files from the `gh-pages-ready` folder to the repo root:
   ```bash
   cp -r /path/to/EEIntake/gh-pages-ready/* .
   ```

3. Commit and push:
   ```bash
   git add .
   git commit -m "Initial GitHub Pages deployment"
   git push origin main
   ```

4. Enable GitHub Pages:
   - Go to: https://github.com/rc979/EEIntake-Pages/settings/pages
   - Source: Deploy from a branch
   - Branch: main
   - Folder: / (root)
   - Click Save

Site will be available at: https://rc979.github.io/EEIntake-Pages
