# EE Intake - GitHub Pages Site

This is the public GitHub Pages site for the EE Intake project artifacts.

**Live Site:** https://rc979.github.io/EEIntake-Pages/

Last updated: 2026-01-26

## Deployment Instructions

### Initial Setup (One-time)

1. **Enable GitHub Pages:**
   - Go to: https://github.com/rc979/EEIntake-Pages/settings/pages
   - Source: **Deploy from a branch** (or **GitHub Actions** if using the workflow)
   - Branch: `main`
   - Folder: `/ (root)`
   - Click **Save**

2. **Wait for build:**
   - GitHub Pages will automatically build and deploy
   - Check status: https://github.com/rc979/EEIntake-Pages/actions
   - Site will be live at: https://rc979.github.io/EEIntake-Pages/

### Updating the Site

**Fastest Method - GitHub Actions Workflow (Recommended):**

From the main EEIntake repo directory:

```bash
# 1. Prepare files (updates links, regenerates HTML, etc.)
./scripts/publish/prepare_gh_pages.sh EEIntake-Pages rc979

# 2. Commit and push the gh-pages-ready folder to main repo
git add gh-pages-ready/
git commit -m "Update Pages site files"
git push

# 3. Trigger the sync workflow (runs on GitHub servers - FAST!)
gh workflow run sync-from-main.yml --repo rc979/EEIntake-Pages
```

Or manually trigger:
- Go to: https://github.com/rc979/EEIntake-Pages/actions
- Click "Sync from Main Repo" → "Run workflow" → "Run workflow"

**Why this is fastest:**
- ✅ Runs entirely on GitHub's servers (no local uploads)
- ✅ Handles all 170+ files in one operation
- ✅ Automatically commits and deploys
- ✅ Takes ~30 seconds total

**Alternative Methods (slower):**
- Manual git push (requires cloning locally)
- API upload script (uploads files one by one - slow)

#### Option 2: Manual Git Push

If you prefer using git directly:

```bash
# From the main EEIntake repo
cd ~/Downloads
git clone https://github.com/rc979/EEIntake-Pages.git
cd EEIntake-Pages

# Copy updated files
cp -r "/path/to/EEIntake/gh-pages-ready"/* .

# Commit and push
git add .
git commit -m "Update GitHub Pages site $(date +%Y-%m-%d)"
git push origin main
```

#### Option 3: Using the Quick Push Script

```bash
bash "/path/to/EEIntake/PUSH_PAGES.sh"
```

## File Structure

- `index.html` - Main landing page
- `outline/` - Project outline HTML export
- `phases/` - Phase artifacts (PDFs, XLSX, CSV)
- `galleries/` - Image galleries extracted from ZIP files
- `.github/workflows/deploy.yml` - GitHub Actions workflow for automatic deployment

## Features

- **XLSX Viewer:** XLSX files have built-in browser viewers (`.xlsx.html` pages)
- **CSV Viewer:** CSV files have built-in browser viewers (`.csv.html` pages)
- **Image Galleries:** ZIP photo sets are extracted into gallery pages
- **All links point to GitHub Pages URLs:** All file references use `https://rc979.github.io/EEIntake-Pages/`

## Troubleshooting

### Site not updating
- Check GitHub Actions: https://github.com/rc979/EEIntake-Pages/actions
- Verify Pages is enabled: https://github.com/rc979/EEIntake-Pages/settings/pages
- Wait a few minutes for GitHub to rebuild

### Files not uploading
- Check GitHub API rate limits
- Verify `gh` CLI is authenticated: `gh auth status`
- Check file paths don't contain invalid characters

### Links broken
- Run `./scripts/publish/prepare_gh_pages.sh` to regenerate files with correct links
- Verify base URL in `scripts/publish/linkify_outline_public_urls.py` is correct

## Related Repositories

- **Main Repo (Private):** https://github.com/rc979/EEIntake
- **Pages Repo (Public):** https://github.com/rc979/EEIntake-Pages
