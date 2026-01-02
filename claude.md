# Hugo Migration Project

## Overview

**Goal:** Migrate from Jekyll to Hugo for faster builds, better templating, and more flexible hosting options.

**Note:** This is the `hugo-migration` branch - focused purely on Hugo migration. For notebook aesthetic redesign, see the `redesign` branch.

## Current State

**Branch:** `hugo-migration`

**Hugo migration:** ~98% complete
- All content migrated and synced
- Build system working and tested
- GitHub Actions deployment configured
- Ready for final testing and deployment

** Always run the server with --disableFastRender**

---

## Hugo Migration

### What's Done

- [x] Hugo installed and configured (`hugo-site/hugo.toml`)
- [x] All 16 blog posts migrated to `hugo-site/content/posts/`
- [x] All 5 navigation pages migrated (`_index.html`, `blog.html`, `books.html`, `articles.html`, `contact.html`)
- [x] 2025 books synced to Hugo version of `books.html`
- [x] Layouts created (`hugo-site/layouts/_default/`)
- [x] CSS and fonts copied to `hugo-site/static/`
- [x] Images and PDFs copied to `hugo-site/static/p/`
- [x] URLs preserved exactly (including `soulbound(less)-tokens.html` with parentheses)
- [x] Relative paths work correctly (images, PDFs)
- [x] Build artifacts added to `.gitignore` (hugo-site/public/, .hugo_build.lock)
- [x] Hugo build tested successfully (23 pages including 404, 32 static files)
- [x] Development server tested and working
- [x] All 16 blog posts tested (images, links, PDFs verified)
- [x] Blog navigation links fixed (all have .html extensions)
- [x] 404 page created (`hugo-site/layouts/404.html`)
- [x] GitHub Actions workflow configured (`.github/workflows/hugo.yml`)
- [x] Permalink configuration updated (deprecated :filename → :contentbasename)
- [x] Hugo output compared with live Jekyll site (content matches)

### Hugo Directory Structure

```
hugo-site/
├── hugo.toml                     # Hugo configuration
├── content/
│   ├── _index.html               # Homepage
│   ├── blog.html                 # Blog listing page
│   ├── books.html                # Books page (includes 2025 books)
│   ├── articles.html             # Articles page
│   ├── contact.html              # Contact page
│   └── posts/                    # Blog posts (16 files)
│       ├── art-clustering-in-renaissance-florence.html
│       ├── live-nation.html
│       ├── soulbound(less)-tokens.html
│       └── ... (13 more)
├── layouts/
│   ├── _default/
│   │   ├── baseof.html           # Base template (head, analytics, CSS)
│   │   ├── single.html           # Single page template (blog posts)
│   │   └── list.html             # List template (sections)
│   └── index.html                # Homepage layout
├── static/
│   ├── main.css                  # Site styles with CSS variables
│   ├── assets/
│   │   ├── fonts/                # Inter font files
│   │   └── images/               # Site images (hr.gif, etc.)
│   └── p/
│       ├── images/               # Blog post images
│       └── pdfs/                 # PDF files
└── public/                       # Build output (gitignored)
```

### Key Hugo Configuration (`hugo.toml`)

```toml
uglyURLs = true                   # Creates .html files, not directories
[permalinks]
  posts = '/p/:contentbasename'   # Blog posts at /p/filename.html
[markup.goldmark.renderer]
  unsafe = true                   # Allows raw HTML in content
```

### What's Left for Hugo Migration

- [ ] Verify mobile responsiveness on actual devices
- [ ] Enable GitHub Pages in repository settings (Settings → Pages → Source: GitHub Actions)
- [ ] Test deployment workflow on main branch
- [ ] Verify live site after deployment
- [ ] Clean up old Jekyll files from repo root after migration is confirmed working
- [ ] Optional: Add RSS feed if desired (currently disabled in hugo.toml)

### To Test Hugo Locally

```bash
cd hugo-site
hugo server
```

Visit http://localhost:1313/

### GitHub Actions Deployment

The site is configured to deploy automatically via GitHub Actions:

**Workflow file:** `.github/workflows/hugo.yml`

**How it works:**
1. Triggers on push to `main` branch or manual workflow dispatch
2. Builds Hugo site from `hugo-site/` directory
3. Uses Hugo v0.154.0 (extended) with minification
4. Deploys to GitHub Pages

**To enable:**
1. Go to repository Settings → Pages
2. Set Source to "GitHub Actions"
3. Merge `hugo-migration` branch to `main`
4. Workflow will automatically deploy

---

## Branch Structure

This repository has multiple branches for different purposes:

- **`main`** - Production Jekyll site (currently live at msherman.xyz)
- **`hugo-migration`** (this branch) - Hugo migration work only, no notebook styling
- **`redesign`** - Notebook aesthetic prototypes and styling (for future implementation)

---

## Files Changed from Main Branch

Key files modified/added on `hugo-migration` branch:

### New
- `hugo-site/` - Complete Hugo site structure
- `claude.md` - This documentation file
- `.gitignore` - Updated with Hugo build artifacts

### Modified in Root (from main branch updates)
- `books.html` - 2025 books added, CSS variables for colors
- `main.css` - CSS variables added for book colors
- `index.html` - Minor updates
- Several blog posts in `p/` directory

### To Clean Up After Migration
Once Hugo deployment is confirmed working, these Jekyll files can be removed from root:
- `_layouts/` - Jekyll layouts (if they exist)
- `_includes/` - Jekyll includes (if they exist)
- `_config.yml` - Jekyll config (if it exists)
- `Gemfile`, `Gemfile.lock` - Jekyll dependencies

---

## Quick Commands

```bash
# Test Hugo locally
cd hugo-site && hugo server

# Build Hugo site
cd hugo-site && hugo --cleanDestinationDir

# Check what Hugo generates
ls -la hugo-site/public/

# Compare with live site
open https://msherman.xyz/p/art-clustering-in-renaissance-florence.html
open http://localhost:1313/p/art-clustering-in-renaissance-florence.html
```

---

## Next Steps

Priority tasks for completing Hugo migration:

1. **Test all 16 blog posts thoroughly**
   - Verify images load correctly
   - Check PDF links work
   - Test internal and external links
   - Verify mobile responsiveness

2. **Set up GitHub Actions for deployment**
   - Hugo doesn't have native GitHub Pages support like Jekyll
   - Need workflow to build and deploy to gh-pages branch or custom hosting
   - Consider deployment options (GitHub Pages, Netlify, Vercel, etc.)

3. **Add 404 page**
   - Create `hugo-site/layouts/404.html`
   - Test 404 handling

4. **Final testing**
   - Compare Hugo output with live site
   - Mobile responsiveness check
   - Performance testing

5. **Switch to production**
   - Update deployment to use Hugo
   - Clean up old Jekyll files from root
   - Update main branch with Hugo site

## Future Work (Separate Branch)

For notebook aesthetic redesign, switch to the `redesign` branch which contains:
- `prototype-index.html` - Notebook UI prototype
- `notebook.css` - Notebook styling
- Implementation plan for applying notebook aesthetic to navigation pages
