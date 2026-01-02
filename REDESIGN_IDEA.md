# Jupyter Notebook Redesign - Complete Design Document

## Overview

Transform the personal website into a Jupyter notebook-inspired interface that appeals to technical audiences (data professionals, potential employers in tech) while maintaining excellent readability for long-form content.

**Core Philosophy:** The notebook metaphor creates an authentic, technical aesthetic for the homepage and navigation, but steps back for blog posts to prioritize reading experience.

---

## Visual Identity

### The Notebook Header

Every page features a **persistent notebook header** at the top:

```
📓 maksym_sherman.ipynb     ● Maksym Sherman (active)
```

**Structure:**
- Icon: `&#128211;` (📓 notebook emoji)
- Filename: `maksym_sherman.ipynb`
- Kernel indicator: Green dot (`●`) + "Maksym Sherman (active)"

**Styling:**
- Background: `#252526` (dark gray)
- Border bottom: `1px solid #3c3c3c`
- Font: SF Mono, Fira Code, Consolas (monospace)
- Position: Sticky (stays visible on scroll)
- Height: ~40px with 8px vertical padding

---

## Color Scheme

Inspired by VS Code's dark theme, optimized for readability:

### Background Colors
- Primary background: `#1e1e1e` (almost black)
- Secondary background: `#252526` (header, table headers)
- Cell background: `#2d2d2d` (notebook cells)
- Cell hover: `#323232` (subtle interaction feedback)
- Code input: `#1e1e1e` (matches primary)

### Text Colors
- Primary text: `#e0e0e0` (light gray, main content)
- Secondary text: `#a0a0a0` (medium gray, descriptions)
- Muted text: `#6a6a6a` (dark gray, metadata)
- Execution counts: `#7c7c7c` (gutter numbers)

### Accent Colors
- Blue: `#4fc3f7` (links, execution brackets, hover accents)
- Green: `#81c784` (kernel indicator, strings in code)
- Orange: `#ffb74d` (file icon, bold text in cells)
- Purple: `#b39ddb` (Python keywords)
- Yellow: `#fff176` (function names)

### Border & UI
- Border color: `#3c3c3c` (subtle dividers)
- Link color: `#64b5f6` (clickable links in notebook cells)

### Blog Post Colors (from main.css)
- Background: Gradient `linear-gradient(#2a2a29, #1c1c1c)`
- Text: `#f0e7d5` (warm cream, easier on eyes for reading)
- Links: `#ffcc00` (yellow)
- Link hover: `#ffeb9b` (lighter yellow)
- Headings: `#e8e8e8` (off-white)
- Subheadings (h3, h5): `#b6b6b6` (gray)
- Blockquote border: `#ffcc00` (yellow, 3px left border)

### Book Rating Colors
- Green books: `#a8e6a0` (9-10/10 ratings)
- Blue books: `#64b5f6` (7-8/10 ratings)
- Gray books: `#b0b0b0` (5-6/10 ratings)

---

## Typography

### Font Families
- **Sans-serif:** Inter (loaded via @font-face from `/assets/fonts/InterVariable.woff2`)
- **Monospace:** SF Mono, Fira Code, Consolas
- **Font features:** `'liga' 1, 'calt' 1` (ligatures enabled)

### Font Sizes - Notebook UI

**Code cells:**
- Input: `14px` (monospace)
- Comments: `14px` italic, muted color

**Markdown cells (homepage):**
- H1: `28px`, weight 600
- H2: `22px`, weight 600, bottom border
- H3: `16px`, weight 600, secondary color
- Paragraph: `15px`, line-height 1.6

**Navigation cards:**
- Icon: `32px` (desktop), `28px` (mobile)
- Title: `18px` (desktop), `16px` (mobile), weight 500
- Description: `14px`, secondary color
- Count: `24px`, weight 600, blue accent

**Execution counts:**
- Gutter: `12px` (desktop), `11px` (mobile), monospace

### Font Sizes - Blog Posts (from main.css)

**Desktop:**
- Base: `16px` (set explicitly on `html` element)
- H1: `28px`, line-height 1.2
- H2: `24px`, line-height 1.2
- H3: `18px`, line-height 1.3, color `#b6b6b6`
- H4: `17px`, line-height 1.4
- H5: `15px`, line-height 1.4, color `#b6b6b6`
- H6: `13px`, line-height 1.4
- Body text: Inherits 16px from html
- Code inline: `13px`, monospace

**Mobile (max-width: 768px):**
- Base paragraph: `16px` (explicit)
- H1: `28px`
- H2: `24px`
- H3: `20px`
- H4: `18px`
- H5: `16px`
- H6: `14px`

---

## Layout Structure

### Cell-Based Layout

Every interactive element is a "cell" with:

1. **Cell gutter** (left side, 50px wide on desktop, 35px mobile)
   - Execution count: `In [n]:` or `Out[n]:`
   - Colored brackets: `[` and `]` in blue (`--accent-blue`)
   - Right-aligned, monospace font
   - Non-selectable (user-select: none)

2. **Cell body** (main content area)
   - Flexible width, fills remaining space
   - Padding: `10-12px` vertical, `0-16px` horizontal

3. **Cell container**
   - Minimal border (transparent by default)
   - Hover state: `1px solid --border-color` + `3px blue left accent`
   - Border radius: `4px`
   - Margin between cells: `8px`

### Page Layouts

**Homepage:**
- Max width: `900px`
- Centered with `margin: 0 auto`
- Padding: `20px 16px 60px` (desktop), `20px 12px 40px` (mobile)

**Blog Posts:**
- Max width: `650px` (matches original site's `.wrapper` and `section`)
- Centered with `margin: 0 auto`
- Padding: `30px 20px 50px` (desktop), `20px 10px 50px` (mobile)
- Mobile: `80%` max-width for narrower screens

**List Pages (blog, books, articles, contact):**
- Max width: `900px` (same as homepage)
- Uses cell-based layout
- Code cell shows method call (e.g., `me.list_posts(by="year")`)
- Output cell contains formatted list content

---

## Cell Types

### 1. Code Cells

**Purpose:** Display Python-style code snippets

**Structure:**
```html
<div class="cell code-cell">
  <div class="cell-content">
    <div class="cell-gutter">
      <span class="bracket">In [</span>1<span class="bracket">]:</span>
    </div>
    <div class="cell-body">
      <div class="code-input">
        <span class="keyword">from</span>
        <span class="variable">world</span>
        <span class="keyword">import</span>
        <span class="function">Person</span>
      </div>
    </div>
  </div>
</div>
```

**Syntax Highlighting Classes:**
- `.keyword` → Purple (`#b39ddb`) - Python keywords (from, import, def, class, etc.)
- `.function` → Yellow (`#fff176`) - Function/class names
- `.string` → Green (`#81c784`) - String literals
- `.variable` → Blue (`#4fc3f7`) - Variable names
- `.comment` → Muted (`#6a6a6a`), italic - Comments starting with `#`
- `.number` → Green (`#81c784`) - Numeric literals
- `.operator` → Secondary (`#a0a0a0`) - Operators (+, -, =, etc.)
- `.builtin` → Blue (`#4fc3f7`) - Built-in functions

**Styling:**
- Background: `#1e1e1e` (dark)
- Border radius: `4px`
- Font: Monospace, `14px`
- Line height: `1.5`
- Preserves whitespace: `white-space: pre-wrap`

### 2. Markdown Cells

**Purpose:** Display formatted text, headings, intro paragraphs

**Structure:**
```html
<div class="cell markdown-cell">
  <div class="cell-content">
    <div class="cell-gutter"></div>
    <div class="cell-body">
      <h1>Hi, I'm Maksym!</h1>
      <p>I believe in great work, ambition, and obsessiveness...</p>
    </div>
  </div>
</div>
```

**Characteristics:**
- No execution count (empty gutter)
- Padding: `12px 16px 12px 0`
- Bold text: Orange color (`#ffb74d`), weight 500
- Links: Blue (`#64b5f6`), underline on hover

### 3. Output Cells

**Purpose:** Display execution results (DataFrames, lists, navigation)

**Structure:**
```html
<div class="cell output-cell">
  <div class="cell-content">
    <div class="cell-gutter">
      <span class="bracket">Out[</span>2<span class="bracket">]:</span>
    </div>
    <div class="cell-body">
      <!-- Content varies: DataFrames, nav cards, lists -->
    </div>
  </div>
</div>
```

**Output Types:**

#### DataFrame Output
```html
<div class="dataframe-output">
  <table class="dataframe">
    <thead>
      <tr><th></th><th>status</th><th>description</th></tr>
    </thead>
    <tbody>
      <tr>
        <td class="index">currently</td>
        <td>Economic consulting</td>
        <td>Focused on data work</td>
      </tr>
    </tbody>
  </table>
</div>
```

**Styling:**
- Monospace font, `13px` (desktop), `11px` (mobile)
- Borders: `1px solid --border-color`
- Header background: `#252526`, text: `#a0a0a0`, weight 600
- Cell padding: `8px 12px` (desktop), `6px 8px` (mobile)
- Row hover: Background `#2d2d2d`

#### Navigation Output (Homepage)

Grid of clickable cards:

```html
<div class="nav-output">
  <a href="blog.html" class="nav-link">
    <span class="nav-icon">&#128221;</span>
    <div class="nav-content">
      <div class="nav-title">blog <span class="nav-arrow">→</span></div>
      <div class="nav-desc">Essays on economics, technology, and ideas</div>
    </div>
    <div class="nav-meta">16 posts</div>
  </a>
  <!-- Repeat for books, articles, contact -->
</div>
```

**Note:** HTML uses `nav-link` class but CSS should style as `nav-card` (implementation detail to fix)

**Icons:**
- Blog: `&#128221;` (📝)
- Books: `&#128218;` (📚)
- Articles: `&#128279;` (🔗)
- Contact: `&#128231;` (📧)

**Grid:**
- Desktop: `repeat(auto-fit, minmax(200px, 1fr))`
- Mobile: `1fr` (single column)
- Gap: `16px`

**Card Styling:**
- Background: `#2d2d2d`
- Border: `1px solid #3c3c3c`, radius `6px`
- Padding: `20px` (desktop), `16px` (mobile)
- Transition: `all 0.2s ease`

**Hover Effects:**
- Background → `#323232`
- Border color → `#4fc3f7` (blue)
- Transform: `translateX(4px)` (slides right)
- Box shadow: `0 4px 12px rgba(79, 195, 247, 0.2)` (blue glow)
- Title: Underline
- Arrow: `translateX(4px)` (moves right), opacity 0.6 → 1

#### List Content Output (List Pages)

Used for blog/books/articles/contact pages:

```html
<div class="list-content">
  <h1>Blog</h1>
  <h3>2025</h3>
  <p><a href="...">Post Title</a></p>
  <!-- More posts -->
</div>
```

**Styling:**
- Font size: `15px`
- H2: `20px`, bottom border, margin-top `24px`
- H3: `16px`, secondary color, margin-top `20px`
- Links: Blue (`#64b5f6`), underline on hover
- Lists: No bullet points, minimal padding

### 4. Widget Cells

**Purpose:** Embed external content (Substack newsletter)

**Structure:**
```html
<div class="cell widget-cell">
  <div class="cell-content">
    <div class="cell-gutter">
      <span class="bracket">Out[</span>4<span class="bracket">]:</span>
    </div>
    <div class="cell-body">
      <div class="widget-container">
        <iframe src="https://msherman.substack.com/embed" ...></iframe>
      </div>
    </div>
  </div>
</div>
```

**Styling:**
- Widget container: Centered with flexbox
- Padding: `20px 0`
- Iframe: Border `1px solid --border-color`, radius `4px`

---

## Homepage Structure

### Cell Sequence

1. **Cell 1 - Code:** `In [1]:` Import Person, create `me` instance
2. **Cell 2 - Markdown:** Introduction ("Hi, I'm Maksym!")
3. **Cell 3 - Code:** `In [2]:` Call `me.describe()`
4. **Cell 3 - Output:** `Out[2]:` DataFrame with current/previous/always status
5. **Cell 4 - Code:** `In [3]:` Call `me.get_sections()` with comment "# Explore my work"
6. **Cell 4 - Output:** `Out[3]:` Navigation cards (blog, books, articles, contact)
7. **Cell 5 - Code:** `In [4]:` Call `me.subscribe()` with comment "# Get notified of new posts"
8. **Cell 5 - Output:** `Out[4]:` Substack newsletter embed

### Dynamic Content

- Blog post count: `{{ len (where .Site.RegularPages "Section" "posts") }}`
- Books count: Hard-coded `160` (manual update)
- Articles count: Hard-coded `70` (manual update)

---

## List Pages Structure

All list pages (blog.html, books.html, articles.html, contact.html) follow this pattern:

### Front Matter
```yaml
---
title: "Blog"
layout: notebook
---
```

### Cell Structure

**Code Cell:**
```html
<div class="cell code-cell">
  <div class="cell-content">
    <div class="cell-gutter">
      <span class="bracket">In [</span>1<span class="bracket">]:</span>
    </div>
    <div class="cell-body">
      <div class="code-input">
        <span class="variable">me</span>.<span class="function">list_posts</span>(by=<span class="string">"year"</span>)
      </div>
    </div>
  </div>
</div>
```

**Output Cell:**
```html
<div class="cell output-cell">
  <div class="cell-content">
    <div class="cell-gutter">
      <span class="bracket">Out[</span>1<span class="bracket">]:</span>
    </div>
    <div class="cell-body">
      <div class="list-content">
        <!-- List content here -->
      </div>
    </div>
  </div>
</div>
```

### Page-Specific Methods

- **blog.html:** `me.list_posts(by="year")`
- **books.html:** `me.list_books(by="year", with_ratings=True)`
- **articles.html:** `me.list_articles(by="rating")`
- **contact.html:** `me.get_contact_info()`

---

## Blog Post Structure

**Design Decision:** Blog posts use a simplified layout - notebook header for branding, but standard typography for maximum readability.

### Template (single.html)

```html
<header class="notebook-header">
  <div class="notebook-toolbar">
    <div class="notebook-title">
      <span class="icon">&#128211;</span>
      <span>maksym_sherman.ipynb</span>
    </div>
    <div class="kernel-indicator">
      <span class="kernel-dot"></span>
      <span>Maksym Sherman (active)</span>
    </div>
  </div>
</header>

<div class="blog-wrapper">
  <main class="blog-container">
    <article class="blog-post-content">
      {{ .Content }}
    </article>
  </main>
</div>
```

### Styling Approach

**Typography comes from main.css**, notebook.css only provides:
- Header styling
- Layout containers (`.blog-wrapper`, `.blog-container`)
- HR styling (uses original `hr.gif` background)

**Key constraint:** `.blog-container { max-width: 650px }` for optimal reading line length

---

## CSS Architecture

### Two-File System

**main.css** (378 lines) - Base typography and colors
- All heading styles (h1-h6)
- Paragraph, link, code, blockquote styles
- Table styling
- Mobile responsive font sizes
- Original site colors and backgrounds
- 650px max-width for sections
- Base font-size: `16px` on html element

**notebook.css** (570 lines) - Notebook theme UI only
- CSS variables for notebook colors
- Notebook header/toolbar
- Cell structure (gutters, bodies, containers)
- Code cell syntax highlighting
- Output cell styling
- Navigation cards
- DataFrame tables
- List content styling
- Widget containers
- Mobile responsiveness for notebook elements

**Load Order (in baseof.html):**
```html
<link rel="stylesheet" href="/main.css">
<link rel="stylesheet" href="/notebook.css">
```

**Important:** Do NOT add universal reset (`* { margin: 0; padding: 0 }`) to notebook.css as it will override main.css spacing.

---

## Templates

### baseof.html
Base template for all pages:
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <!-- Analytics: Google tag, Umami -->
  <link rel="stylesheet" href="/main.css">
  <link rel="stylesheet" href="/notebook.css">
  <title>{{ .Title | default .Site.Title }}</title>
</head>
<body>
  {{- block "main" . }}{{- end }}
</body>
</html>
```

### index.html
Homepage layout with full notebook cells (see "Homepage Structure" above)

### single.html
Blog post layout with notebook header only (see "Blog Post Structure" above)

### notebook.html
List page layout for blog/books/articles/contact:
```html
{{ define "main" }}
<header class="notebook-header">
  <!-- Same header as everywhere -->
</header>

<main class="notebook list-page">
  {{ .Content }}
</main>
{{ end }}
```

### list.html
Standard Hugo list template (currently unused, prefer notebook.html)

---

## Mobile Responsiveness

### Breakpoints

**768px and below:**
- Blog container: `max-width: 80%`, reduced padding
- Notebook: Reduced padding `20px 12px 40px`
- Navigation: Single column grid
- Font sizes: Explicit sizes for all headings (see Typography section)

**640px and below:**
- Notebook toolbar: Wraps, hides status indicator
- Cell gutter: `35px` width (down from 50px)
- Code input: `13px` font
- Output content: `12px` font
- Navigation cards: Reduced padding `16px`, smaller icons `28px`, smaller titles `16px`
- DataFrames: `11px` font, reduced cell padding

---

## Known Issues & Design Decisions

### Fixed
- ✅ Blog post centering (removed `width: 100%` from container, use `margin: 0 auto`)
- ✅ List pages implemented with notebook aesthetic
- ✅ Consistent notebook header across all pages
- ✅ Two-file CSS system for cleaner separation

### Current Issues
1. **Width constraints:** Some experimentation needed with `650px` vs `55ch` for optimal reading
2. **HTML/CSS mismatch:** Homepage uses `nav-link` class but CSS defines `nav-card` - need to align
3. **Font rendering:** May appear smaller than expected due to cascade issues - ensure `font-size: 16px` is set on `html` element in main.css

### Important Decisions

1. **No notebook cells for blog posts:** The cell wrapper adds friction for long-form reading. Just use the header for branding.

2. **Authentic but not literal:** Use real Jupyter patterns (execution counts, syntax highlighting, DataFrames) but don't force them where they don't fit.

3. **Mobile-first navigation:** Cards stack vertically on mobile, ensuring all content is accessible.

4. **Sticky header:** Notebook header stays visible on scroll for constant branding.

5. **Original typography for blogs:** Reading experience > aesthetic consistency. Blog posts use proven readable type.

---

## Assets Required

### Fonts
- `/assets/fonts/InterVariable.woff2` (regular)
- `/assets/fonts/InterVariable-Italic.woff2` (italic)

### Images
- `/assets/images/hr.gif` (horizontal rule background for blog posts)
- `/assets/images/nav-bg.gif` (if needed for original header styles)

### Hugo Configuration
- Ensure `hugo.toml` is properly configured
- Blog posts live in `content/posts/`
- Static assets in `hugo-site/static/`

---

## Implementation Checklist

Starting from main branch, implement in this order:

### 1. Setup CSS Files
- [ ] Create `hugo-site/static/notebook.css` with variables and base styles
- [ ] Ensure `hugo-site/static/main.css` has `font-size: 16px` on html element
- [ ] Update `baseof.html` to load both stylesheets in order

### 2. Create Notebook Header Component
- [ ] Add notebook header HTML to all templates
- [ ] Style header (sticky, dark background, proper spacing)
- [ ] Test on all page types

### 3. Build Homepage
- [ ] Implement cell structure (gutters, bodies, containers)
- [ ] Create code cells with syntax highlighting
- [ ] Add markdown cell for intro
- [ ] Build DataFrame output for status
- [ ] Create navigation cards with hover effects
- [ ] Add newsletter widget embed
- [ ] Test mobile responsive layout

### 4. Implement List Pages
- [ ] Create `notebook.html` layout template
- [ ] Update blog.html with code/output cell structure
- [ ] Update books.html (with color-coded ratings)
- [ ] Update articles.html (organized by rating)
- [ ] Update contact.html
- [ ] Test list content styling in output cells

### 5. Simplify Blog Posts
- [ ] Keep only notebook header in `single.html`
- [ ] Ensure blog content uses main.css typography
- [ ] Test 650px max-width constraint
- [ ] Verify mobile responsive fonts
- [ ] Test with real blog posts

### 6. Polish & Test
- [ ] Verify all hover states work smoothly
- [ ] Test on actual mobile devices
- [ ] Ensure consistent spacing throughout
- [ ] Check color contrast for accessibility
- [ ] Fix any HTML/CSS class mismatches
- [ ] Verify dynamic counts display correctly

### 7. Documentation
- [ ] Update CLAUDE.md with final state
- [ ] Document any deviations from this plan
- [ ] Note any issues encountered

---

## File Structure

```
hugo-site/
├── hugo.toml
├── content/
│   ├── _index.html              # Homepage content (empty, uses index.html layout)
│   ├── blog.html                # Blog list page
│   ├── books.html               # Books list page (160 books)
│   ├── articles.html            # Articles list page (70 articles)
│   ├── contact.html             # Contact page
│   └── posts/                   # Blog posts
│       ├── post-1.html
│       └── ...
├── layouts/
│   ├── _default/
│   │   ├── baseof.html          # Base template (loads both CSS files)
│   │   ├── single.html          # Blog post layout
│   │   ├── notebook.html        # List page layout
│   │   └── list.html            # (unused)
│   └── index.html               # Homepage layout
├── static/
│   ├── main.css                 # Original site typography (378 lines)
│   ├── notebook.css             # Notebook UI theme (570 lines)
│   └── assets/
│       ├── fonts/
│       │   ├── InterVariable.woff2
│       │   └── InterVariable-Italic.woff2
│       └── images/
│           └── hr.gif
└── public/                      # Build output (gitignored)
```

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

**Platform:** GitHub Pages (configured in main branch)

**Process:**
1. Merge redesign branch to main when ready
2. GitHub Actions automatically builds and deploys
3. Verify live site at https://msherman.xyz/

---

## Design Inspiration & Rationale

**Why Jupyter notebooks?**
- Familiar to technical audiences (data scientists, researchers, developers)
- Interactive, exploratory feel matches the personal site's purpose
- Cell-based layout naturally organizes different content types
- Execution counts provide visual rhythm and progression
- Code aesthetic signals technical credibility

**Why simplify blog posts?**
- Reading long-form content in cell wrappers is exhausting
- Original typography is proven and optimized for readability
- Notebook header provides enough branding
- Users want to focus on ideas, not fight the interface

**Why dark theme?**
- Matches technical aesthetic (VS Code, Jupyter, developer tools)
- Reduces eye strain for long reading sessions
- Creates modern, sophisticated look
- Differentiates from typical personal sites

**Target audience considerations:**
- Data professionals appreciate authentic notebook styling
- Potential employers see technical credibility
- General readers benefit from clean, readable blog posts
- Mobile users need functional, not fancy

---

## Future Enhancements (Optional)

- [ ] Add actual Python execution (via Pyodide) for interactive demos
- [ ] Implement code folding for long snippets
- [ ] Add "copy code" buttons to code cells
- [ ] Create custom 404 page with notebook theme
- [ ] Add search functionality styled as code input
- [ ] Implement light theme toggle (respect prefers-color-scheme)
- [ ] Add animations for cell execution (progressive reveal)
- [ ] Create RSS feed styled as Python import

---

## Credits & References

- **Jupyter Notebook:** https://jupyter.org/
- **VS Code Theme Colors:** https://code.visualstudio.com/
- **Inter Font:** https://rsms.me/inter/
- **Hugo Static Site Generator:** https://gohugo.io/

---

**Last Updated:** 2026-01-02
**Branch:** redesign
**Status:** Implementation complete, refinement in progress
