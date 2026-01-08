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
- Color-coded books (green: phenomenal, blue: particularly great, gray: other)

**Typography:**
- Notebook pages: 16px base with 1.6 line-height, 55ch max-width
- Blog posts: 16px base with 55ch reading width for optimal readability
- Code cells: 14px monospace (Menlo, Monaco, Consolas)

**Technical implementation:**
- Fixed header positioning for consistent branding across scroll
- Conditional CSS loading to prevent style conflicts
- Manual content curation (no auto-generated lists)

---

## Color Scheme

Based on VS Code dark theme with high-contrast golden yellow links.

**Backgrounds:** `#1e1e1e` (primary), `#2d2d2d` (cells), `#252526` (header)
**Text:** `#e0e0e0` (primary), `#a0a0a0` (secondary), `#f0e7d5` (blog posts - warm cream)
**Links:** `#ffcc00` (golden yellow), `#ffeb9b` (hover)
**Syntax:** `#4fc3f7` (blue/counts), `#81c784` (green/kernel), `#b39ddb` (purple/keywords), `#fff176` (yellow/functions)
**Books:** `#a8e6a0` (green - phenomenal), `#64b5f6` (blue - particularly great), `#b0b0b0` (gray - other)

---

## Cell Types

**Code Cells:** Python-style code with syntax highlighting and execution counts (In [1]:)
**Output Cells:** Execution results - DataFrames (tables), navigation lists, or markdown content
**Markdown Cells:** Formatted text without execution counts (empty gutter)
**Widget Cells:** External embeds (e.g., Substack newsletter)

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
- Body has `padding-top: 40px` to prevent content hiding (critical for mobile)
- Header links to homepage (/)

### Mobile Responsiveness Fixes
- **Mobile body padding:** Set to `40px 0 0 0` (not 20px) to prevent blog post titles from being cut off by fixed header
- **Mobile cell gutter:** Increased to `60px` width with `10px` font size to prevent "Out[1]:" from overlapping content
- **Consistent max-width:** Both notebook pages and blog posts use `55ch` to eliminate jarring horizontal shifts when navigating

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


- **Whenever you are testing the website in Chrome, verify that the server is running before attempted to do any Chrome checks.**


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

## LLM Optimization

Site is optimized for LLM consumption with JSON-LD structured data, semantic HTML, and machine-readable metadata (zero visual changes).

**Implemented Features:**
- RSS feed and sitemap generation (`/sitemap.xml`, `/index.xml`)
- Meta descriptions, author tags, canonical URLs on all pages
- OpenGraph and Twitter Card metadata
- JSON-LD schemas: WebSite (all pages), Person (homepage), BlogPosting (posts), ItemList (blog page)
- Semantic HTML: `<article>`, `<time datetime="...">`, `<nav aria-label="...">`
- All 16 blog posts have front matter with ISO 8601 dates and descriptions
- Post archetype template (`hugo-site/archetypes/posts.md`)
- robots.txt with sitemap reference

**Key Implementation:**
- Uses Hugo's `jsonify` filter for proper JSON escaping
- Falls back to auto-generated summaries when descriptions missing
- `<time>` tags provide machine-readable dates while preserving display format
- All metadata is invisible (no CSS changes)

**Validation:**
- Google Rich Results Test: https://search.google.com/test/rich-results
- Schema.org Validator: https://validator.schema.org/
- RSS Feed Validator: https://validator.w3.org/feed/

---

## Future Enhancements

**Testing & Quality Assurance:**
- Automated testing: Hugo build validation, HTML/link checking, JSON-LD validation
- GitHub Actions integration for PR validation
- Lighthouse audits (Performance, Accessibility, SEO)
- Visual regression testing
- Cross-browser testing (Safari, Firefox, Edge)

**UI:** Notebook-themed 404 page, hover refinements, spacing adjustments

**Interactive:** Python execution (Pyodide), code folding, copy code buttons, search functionality, execution animations

**Content:** Light theme toggle, tag/category filtering, reading time estimates

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
- Max-width: 55ch for both notebook pages and blog posts (ensures consistent alignment when navigating between pages)

---

## Design Philosophy

Uses Jupyter notebook metaphor for navigation pages (homepage, blog list, books, articles, contact) to create authentic technical aesthetic. Blog posts use only the notebook header with traditional typography for optimal long-form reading.

**Notebook navigation:** Familiar to technical audiences, cell-based organization, signals credibility
**Traditional blog typography:** Reading long-form content in cells is exhausting - focus on ideas, not interface

---

**Last Updated:** 2026-01-05

### Recent Changes

**2026-01-05** - LLM Optimization
- Added comprehensive JSON-LD structured data (WebSite, Person, BlogPosting, ItemList schemas)
- Added OpenGraph and Twitter Card metadata for rich social sharing
- Enabled RSS feed and sitemap generation
- Added semantic HTML (`<article>`, `<time>`, `<nav>` tags with aria-labels)
- Updated all 16 blog posts with front matter (date, description)
- Created post archetype template for future posts
- Created robots.txt with sitemap reference
- Zero visual changes - all metadata is machine-readable only

**2026-01-02** - Mobile Responsiveness
- Fixed mobile header overlap issue on blog posts
- Fixed "Out[1]:" text overlapping with content on mobile
- Standardized max-width to 55ch across all pages for consistent alignment
