# EE Intake - GitHub Pages Site

This is the public GitHub Pages site for the EE Intake project artifacts.

**Live Site:** https://rc979.github.io/EEIntake-Pages/

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

To update the site with new content from the main EEIntake repo:

#### Option 1: Using GitHub Actions Workflow (Fastest - Recommended)

From the main EEIntake repo directory:

```bash
# 1. Prepare files (updates links, regenerates HTML, etc.)
./scripts/publish/prepare_gh_pages.sh EEIntake-Pages rc979

# 2. Commit and push the gh-pages-ready folder to main repo
git add gh-pages-ready/
git commit -m "Update Pages site files"
git push

# 3. Trigger the sync workflow (fast - runs on GitHub servers)
./scripts/publish/sync_pages_fast.sh EEIntake-Pages rc979
```

Or manually trigger the workflow:
- Go to: https://github.com/rc979/EEIntake-Pages/actions
- Click "Sync from Main Repo" workflow
- Click "Run workflow" → "Run workflow"

This is the fastest method because:
- Files are synced on GitHub's servers (no local upload)
- Handles all files in one operation
- Automatically commits and deploys

#### Option 2: Using the Upload Script (Slower - API method)

From the main EEIntake repo directory:

```bash
# 1. Prepare files
./scripts/publish/prepare_gh_pages.sh EEIntake-Pages rc979

# 2. Upload files via GitHub API (slower, uploads one by one)
python3 scripts/publish/upload_via_api.py
```

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
