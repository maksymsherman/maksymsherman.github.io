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
- Notebook pages: 16px base with 1.6 line-height, 55ch max-width
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

## LLM Optimization Implementation Plan

### Goal
Optimize msherman.xyz for LLM consumption by adding JSON-LD structured data, semantic HTML, and machine-readable metadata while preserving the Jupyter notebook aesthetic.

### Current State Analysis
- **No metadata**: Missing meta descriptions, OpenGraph tags, structured data
- **Disabled features**: RSS and sitemap explicitly disabled in `hugo.toml` line 7
- **Minimal front matter**: Blog posts only have `title`, missing dates and descriptions
- **Dates in content**: Embedded as `<h5>July 13th, 2025</h5>` text, not machine-readable
- **No semantic HTML**: Missing `<article>`, `<time>`, proper metadata tags
- **16 blog posts** need manual front matter updates

### Implementation Steps

#### Step 1: Enable RSS & Sitemap
**File**: `hugo-site/hugo.toml`

Change line 7 from:
```toml
disableKinds = ['RSS', 'sitemap', 'taxonomy', 'term']
```

To:
```toml
disableKinds = ['taxonomy', 'term']
```

Add site-wide metadata after line 10:
```toml
[params]
  author = "Maksym Sherman"
  description = "Personal website of Maksym Sherman - exploring great work, ambition, and explanations."
```

#### Step 2: Add Base Metadata to All Pages
**File**: `hugo-site/layouts/_default/baseof.html`

Insert after line 6 (after viewport meta tag):
```html
<meta name="description" content="{{ if .Description }}{{ .Description }}{{ else if .IsHome }}{{ .Site.Params.description }}{{ else }}{{ .Summary | plainify | truncate 160 }}{{ end }}">
<meta name="author" content="{{ .Site.Params.author }}">
<link rel="canonical" href="{{ .Permalink }}">
```

#### Step 3: Add JSON-LD Structured Data
**File**: `hugo-site/layouts/_default/baseof.html`

Insert before closing `</head>` tag (after line 33):

```html
<!-- Structured Data -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "{{ .Site.Title }}",
  "url": "{{ .Site.BaseURL }}",
  "author": {
    "@type": "Person",
    "name": "{{ .Site.Params.author }}",
    "url": "{{ .Site.BaseURL }}"
  }
}
</script>

{{ if .IsHome }}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Maksym Sherman",
  "url": "{{ .Site.BaseURL }}",
  "jobTitle": "Data Consultant",
  "description": "I believe in great work, ambition, and obsessiveness. I seek to understand the world through better explanations."
}
</script>
{{ end }}

{{ if and (not .IsHome) (eq .Type "posts") }}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": {{ .Title | jsonify }},
  "author": {
    "@type": "Person",
    "name": "{{ .Site.Params.author }}",
    "url": "{{ .Site.BaseURL }}"
  },
  {{ with .Params.date }}
  "datePublished": "{{ .Format "2006-01-02T15:04:05Z07:00" }}",
  {{ end }}
  {{ with .Params.description }}
  "description": {{ . | jsonify }},
  {{ else }}
  "description": {{ .Summary | plainify | truncate 160 | jsonify }},
  {{ end }}
  "url": "{{ .Permalink }}",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "{{ .Permalink }}"
  }
}
</script>
{{ end }}
```

**Why JSON-LD?**
- Preferred structured data format for LLMs
- Enables semantic understanding of content
- Separate from display HTML (no visual changes)
- Uses `jsonify` filter to properly escape strings

#### Step 4: Add Semantic HTML to Blog Posts
**File**: `hugo-site/layouts/_default/single.html`

Replace lines 1-5 with:
```html
{{ define "main" }}
{{ partial "notebook-header.html" . }}

<article itemscope itemtype="https://schema.org/BlogPosting">
  <meta itemprop="headline" content="{{ .Title }}">
  <meta itemprop="author" content="{{ .Site.Params.author }}">
  {{ with .Params.date }}<meta itemprop="datePublished" content="{{ .Format "2006-01-02" }}">{{ end }}
  {{ with .Description }}<meta itemprop="description" content="{{ . }}">{{ end }}

  {{ .Content }}
</article>
{{ end }}
```

**Note**:
- `<meta>` tags are hidden (no visual change)
- `<article>` tag is semantic wrapper
- Microdata provides in-page structured data

#### Step 5: Update All 16 Blog Posts with Front Matter
**Files**: All files in `hugo-site/content/posts/`

For each blog post:
1. Extract date from `<h5>` tag (e.g., "July 13th, 2025")
2. Add to front matter in ISO 8601 format
3. Add description (use first paragraph or write custom, max 160 chars)
4. Wrap date in `<time>` tag for semantic HTML

**Example - unpredictable.html**:

Change front matter from:
```yaml
---
title: "Unpredictable"
---
```

To:
```yaml
---
title: "Unpredictable"
date: 2025-07-13
description: "Human creativity makes even our most well-reasoned long-term forecasts fundamentally unreliable."
---
```

Change date in content from:
```html
<h5>July 13th, 2025</h5>
```

To:
```html
<h5><time datetime="2025-07-13">July 13th, 2025</time></h5>
```

**Repeat for all 16 posts**:
- unpredictable.html
- striking_while_the_iron_is_hot.html
- boi-favorite-book.html
- soulbound(less)-tokens.html
- art-clustering-in-renaissance-florence.html
- knowledge-without-explanation.html
- reasoning-by-inertia.html
- live-nation.html
- some-thoughts.html
- men-and-rubber.html
- newsletter-publishing-platforms.html
- 7powers-vs-blockchain.html
- beyond-blockchain-marketplaces.html
- the-known-world.html
- perverse-incentives-and-airdrops.html
- to-the-lighthouse.html

#### Step 6: Create Post Archetype for Future Posts
**File**: `hugo-site/archetypes/posts.md` (create new file)

```yaml
---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
description: "Brief summary of the post (max 160 characters)"
---

<h1>{{ replace .Name "-" " " | title }}</h1>
<h5><time datetime="{{ .Date.Format "2006-01-02" }}">{{ .Date.Format "January 2nd, 2006" }}</time></h5>

<p>Your content here...</p>
```

### Testing & Validation

#### Build Test
```bash
cd hugo-site
hugo --noHTTPCache
```

#### Verify Generated Files
- `public/sitemap.xml` should exist
- `public/index.xml` (RSS feed) should exist

#### Visual Regression Test
Compare before/after screenshots to ensure zero visual changes:
- Homepage
- Blog list page
- Individual blog posts
- Mobile views

#### Structured Data Validation
1. View page source - verify no `{{` Hugo variables in output
2. Test with Google Rich Results Test: https://search.google.com/test/rich-results
3. Test with Schema.org validator: https://validator.schema.org/

#### LLM Consumption Test
- Ask LLM to extract publication date from blog post URL
- Ask LLM to identify author from homepage
- Verify sitemap lists all pages

### Critical Files to Modify

1. `hugo-site/hugo.toml` - Enable RSS/sitemap, add params
2. `hugo-site/layouts/_default/baseof.html` - Add metadata and JSON-LD
3. `hugo-site/layouts/_default/single.html` - Add semantic article wrapper
4. `hugo-site/content/posts/*.html` - Add front matter to all 16 posts

### Files to Create

1. `hugo-site/archetypes/posts.md` - Template for future posts

### Success Criteria

✓ Sitemap and RSS feed generated
✓ JSON-LD structured data on all pages
✓ Semantic `<article>` tags on blog posts
✓ All blog posts have machine-readable dates
✓ Meta descriptions on all pages
✓ Canonical URLs on all pages
✓ **Zero visual changes to notebook aesthetic**
✓ Passes structured data validation

### Implementation Notes

- Uses `jsonify` filter to properly escape JSON strings
- Falls back to `.Summary` for descriptions when front matter missing
- Preserves exact visual appearance (CSS classes unchanged)
- `<time>` and `<meta>` tags are semantically meaningful but invisible
- WebSite, Person, and BlogPosting schemas provide rich metadata for LLMs

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
- Max-width: 55ch for both notebook pages and blog posts (ensures consistent alignment when navigating between pages)

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

### Recent Changes (2026-01-02)
- Fixed mobile header overlap issue on blog posts
- Fixed "Out[1]:" text overlapping with content on mobile
- Standardized max-width to 55ch across all pages for consistent alignment
