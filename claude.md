# Jupyter Notebook Redesign

## Overview

Personal website redesigned with Jupyter notebook-inspired interface for technical aesthetic while maintaining excellent readability.

**Branch:** `redesign`
**Status:** Ready for production (Steps 1-2 complete)

---

## Current State

### Completed

**Step 1 - Notebook pages (homepage + list pages):**
- ✅ Notebook header with `maksym_sherman.ipynb` branding
- ✅ Cell-based layout with execution counts (`In [n]:`, `Out[n]:`)
- ✅ Python syntax highlighting in code cells
- ✅ Navigation links styled as notebook output
- ✅ DataFrame output for personal info
- ✅ Substack newsletter embed in widget cell
- ✅ List pages (blog/books/articles/contact) with notebook cells

**Step 2 - Blog posts:**
- ✅ Notebook header added to all blog posts
- ✅ Original typography and 55ch reading width preserved
- ✅ No notebook cells (optimal reading experience)

**Testing completed:**
- ✅ Desktop browser testing (1080px viewport, Chrome)
- ✅ Mobile browser testing (375px viewport, Chrome)
- ✅ All navigation pages verified
- ✅ 4 blog posts tested (various content types)
- ✅ Link colors, typography, and layout confirmed

### Not Yet Done

**Cross-browser testing:**
- [ ] Safari (desktop and iOS)
- [ ] Firefox
- [ ] Edge

**Device testing:**
- [ ] iPhone (actual device, not just viewport)
- [ ] Android devices
- [ ] iPad/tablets

**Optional polish (Step 3):**
- [ ] Hover state refinements
- [ ] Spacing fine-tuning
- [ ] Contrast checks (current colors pass WCAG AA)
- [ ] 404 page with notebook theme

---

## Architecture

### File Structure

```
hugo-site/
├── hugo.toml                     # Hugo configuration
├── layouts/
│   ├── _default/
│   │   ├── baseof.html           # Conditional CSS loading
│   │   ├── single.html           # Blog posts (has header)
│   │   └── notebook.html         # List pages layout
│   ├── partials/
│   │   └── notebook-header.html  # Shared header component
│   └── index.html                # Homepage with full notebook UI
├── static/
│   ├── shared.css                # Fonts, variables, header styles
│   ├── notebook.css              # Notebook UI (cells, syntax, layouts)
│   └── main.css                  # Blog post typography (unchanged)
└── content/
    ├── _index.html               # Homepage
    ├── blog.html                 # List pages (notebook layout)
    ├── books.html
    ├── articles.html
    ├── contact.html
    └── posts/                    # Blog posts (16 files)
```

### CSS Loading Strategy

**Conditional loading in baseof.html:**
- All pages load: `shared.css` (fonts, header, variables)
- Notebook pages load: `notebook.css` (homepage, blog/books/articles/contact)
- Blog posts load: `main.css` (original typography)

**Critical:** Never load `main.css` and `notebook.css` together to prevent style conflicts.

### Key Design Decisions

1. **Notebook pages (homepage + lists):** Full cell-based layout with 700px max-width
2. **Blog posts:** Header only, no cells, 55ch reading width preserved
3. **Typography:** Blog posts use proven `main.css` styles for optimal readability
4. **Colors:** Golden yellow links (#ffcc00), VS Code dark theme palette
5. **Header:** Fixed positioning, always visible on scroll
6. **Manual content:** All list pages remain hand-curated (no auto-generation)

---

## Color Scheme

### Background
- Primary: `#1e1e1e` (dark), gradient: `linear-gradient(#2a2a29, #1c1c1c)`
- Cell backgrounds: `#2d2d2d`
- Header: `#252526`

### Text
- Primary: `#e0e0e0` (light gray)
- Secondary: `#a0a0a0` (medium gray)
- Blog posts: `#f0e7d5` (warm cream)

### Accents
- Links: `#ffcc00` (golden yellow)
- Link hover: `#ffeb9b` (lighter golden)
- Blue (execution counts): `#4fc3f7`
- Green (kernel dot): `#81c784`
- Purple (keywords): `#b39ddb`
- Yellow (functions): `#fff176`

### Book Ratings
- Green: `#a8e6a0` (9-10/10)
- Blue: `#64b5f6` (7-8/10)
- Gray: `#b0b0b0` (5-6/10)

---

## Cell Types

### Code Cells
Display Python-style code with syntax highlighting:
```html
<div class="cell code-cell">
  <div class="cell-content">
    <div class="cell-gutter">
      <span class="bracket">In [</span>1<span class="bracket">]:</span>
    </div>
    <div class="cell-body">
      <div class="code-input"><span class="keyword">from</span> <span class="variable">world</span>...</div>
    </div>
  </div>
</div>
```

### Output Cells
Display execution results (DataFrames, lists, navigation):
- DataFrame output: Table with borders, monospace font
- Navigation output: Vertical list of links with icons and metadata
- List content: 55ch max-width for readability

### Markdown Cells
Formatted text without execution counts (empty gutter)

### Widget Cells
External embeds (Substack newsletter)

---

## Critical Implementation Details

### Code Cell Formatting
**MUST** place code content on same line as opening tag to prevent whitespace misalignment:

```html
<!-- CORRECT -->
<div class="code-input"><span class="variable">me</span>.<span class="function">list_posts</span>()</div>

<!-- WRONG - creates whitespace -->
<div class="code-input">
  <span class="variable">me</span>.<span class="function">list_posts</span>()
</div>
```

### Header Fixed Positioning
- Header uses `position: fixed` (not sticky)
- Body has `padding-top: 40px` to prevent content hiding
- Header links to homepage (/)

### Manual Counts
Navigation card counts must be updated manually:
- Blog posts: Update in `content/_index.html`
- Books: Currently 160
- Articles: Currently 70

---

## Testing Locally

```bash
cd hugo-site
hugo server --noHTTPCache --disableFastRender
```

Visit: http://localhost:1313/

**Hard refresh to clear cache:**
- Mac: `Cmd + Shift + R`
- Windows/Linux: `Ctrl + F5`

---

## Deployment

**Platform:** GitHub Pages via GitHub Actions

**Process:**
1. Merge `redesign` branch to `main`
2. GitHub Actions automatically builds and deploys
3. Verify live site at https://msherman.xyz/

**GitHub Actions workflow:** `.github/workflows/hugo.yml`
- Builds from `hugo-site/` directory
- Uses Hugo v0.154.0 (extended)
- Deploys on push to `main`

---

## Known Issues & Solutions

### Issue: Code cell text misalignment
**Cause:** HTML newlines after `<div class="code-input">` create whitespace
**Solution:** Keep code on same line as opening tag (see Critical Implementation Details)

### Issue: Header jumps during scroll
**Cause:** Using `position: sticky`
**Solution:** Changed to `position: fixed` with `left: 0, right: 0, width: 100%`

---

## Future Enhancement Ideas

Optional improvements (not required for launch):

- [ ] Add Python execution (via Pyodide) for interactive demos
- [ ] Implement code folding for long snippets
- [ ] Add "copy code" buttons to code cells
- [ ] Create notebook-themed 404 page
- [ ] Add search functionality styled as code input
- [ ] Implement light theme toggle
- [ ] Add animations for cell execution
- [ ] RSS feed styled as Python import
- [ ] Additional hover state polish
- [ ] Spacing and contrast micro-adjustments

---

## Quick Reference

### Manual Updates Needed

**Adding a new blog post:**
1. Create HTML file in `hugo-site/content/posts/`
2. Update count in `hugo-site/content/_index.html` navigation
3. Add link to `hugo-site/content/blog.html`

**Adding a new book:**
1. Add entry to `hugo-site/content/books.html`
2. Use inline style for color: `style="color: var(--book-green)"`
3. Update count in `hugo-site/content/_index.html` if needed

**Typography rules:**
- Notebook pages: 16px base, line-height 1.6
- Blog posts: 16px base (from main.css)
- Code cells: 14px monospace
- Max-width: 700px for notebook container, 55ch for reading text

---

## Design Philosophy

**Core principle:** Notebook metaphor creates authentic technical aesthetic for navigation, but steps back for blog posts to prioritize reading experience.

**Why Jupyter notebooks?**
- Familiar to technical audiences (data scientists, developers)
- Cell-based layout organizes content naturally
- Code aesthetic signals technical credibility
- Interactive, exploratory feel

**Why simplify blog posts?**
- Reading long-form content in cells is exhausting
- Original typography is proven and readable
- Notebook header provides enough branding
- Focus on ideas, not interface

---

**Last Updated:** 2026-01-02
**Branch:** redesign
**Status:** Production-ready (Steps 1-2 complete, Step 3 optional)
