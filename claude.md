# Personal Website Documentation

## Overview

Personal website built with Hugo, featuring a Jupyter notebook-inspired interface for navigation pages while maintaining optimal reading experience for blog posts. The site combines technical aesthetic with excellent readability.

**Live site:** https://msherman.xyz/
**Deployment:** GitHub Pages via GitHub Actions

### Site Structure

- **Homepage:** Notebook-style interface with personal info (DataFrame output), navigation cards, and newsletter signup
- **List Pages:** Blog, Books, Articles, Contact - all using notebook cell layout
- **Blog Posts:** Individual posts with notebook header but traditional reading layout (no cells)
- **Static Assets:** CSS files for shared styles, notebook UI, and blog typography

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

**Two-tier design approach:**
- Navigation pages (homepage, blog list, books, articles, contact) use full notebook interface with code cells, execution counts, and DataFrame outputs
- Blog posts use only the notebook header, preserving traditional reading typography for long-form content

**Color scheme:**
- Based on VS Code dark theme with golden yellow links (#ffcc00) for high visibility
- Warm cream text (#f0e7d5) for blog posts to reduce eye strain
- Color-coded book ratings (green for 9-10/10, blue for 7-8/10, gray for 5-6/10)

**Typography:**
- Notebook pages: 16px base with 1.6 line-height, 700px max-width
- Blog posts: 16px base with 55ch reading width for optimal readability
- Code cells: 14px monospace (Menlo, Monaco, Consolas)

**Technical implementation:**
- Fixed header positioning for consistent branding across scroll
- Conditional CSS loading to prevent style conflicts
- Manual content curation (no auto-generated lists)

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

**Workflow:**
- Push changes to `main` branch
- GitHub Actions automatically builds from `hugo-site/` directory
- Site deploys to https://msherman.xyz/

**Configuration:** `.github/workflows/hugo.yml`
- Uses Hugo v0.154.0 (extended)
- Builds on every push to `main`
- Automatic deployment to GitHub Pages

---

## Future Ideas & Enhancements

### Additional Testing
- Cross-browser testing (Safari, Firefox, Edge)
- Device testing on actual devices (iPhone, Android, iPad/tablets)
- Accessibility audit (WCAG compliance verification)

### UI Polish
- Hover state refinements
- Spacing micro-adjustments
- Create notebook-themed 404 page
- Additional contrast checks

### Interactive Features
- Add Python execution (via Pyodide) for interactive demos
- Implement code folding for long snippets
- Add "copy code" buttons to code cells
- Add search functionality styled as code input
- Add animations for cell execution

### Content Features
- RSS feed styled as Python import
- Light theme toggle
- Tag/category filtering for blog posts
- Reading time estimates

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

The site uses a Jupyter notebook metaphor to create an authentic technical aesthetic for navigation while prioritizing reading experience for blog posts.

**Why Jupyter notebooks for navigation?**
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
