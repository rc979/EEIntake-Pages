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

**Recommended Method - Git Subtree Push (Fast & Simple):**

From the main EEIntake repo directory:

```bash
# 1. Prepare files (updates links, regenerates HTML, etc.)
./scripts/publish/prepare_gh_pages.sh EEIntake-Pages rc979

# 2. Commit the gh-pages-ready folder to main repo
git add gh-pages-ready/
git commit -m "Update Pages site files"
git push

# 3. Push to Pages repo using git subtree (single fast operation!)
SPLIT_SHA=$(git subtree split --prefix=gh-pages-ready 2>/dev/null)
sleep 1
git push pages-repo $SPLIT_SHA:main --force
```

**Why this is recommended:**
- ✅ Uses regular git push (no API calls)
- ✅ Single operation (not 170+ API calls)
- ✅ Fast (~5-10 seconds)
- ✅ Works reliably (verified method)

**Alternative Method - GitHub Actions Workflow:**

If you prefer automated syncing:

```bash
# 1. Prepare files
./scripts/publish/prepare_gh_pages.sh EEIntake-Pages rc979

# 2. Commit and push to main repo
git add gh-pages-ready/
git commit -m "Update Pages site files"
git push

# 3. Trigger the sync workflow
gh workflow run sync-from-main.yml --repo rc979/EEIntake-Pages
```

Or manually trigger:
- Go to: https://github.com/rc979/EEIntake-Pages/actions
- Click "Sync from Main Repo" → "Run workflow" → "Run workflow"

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
