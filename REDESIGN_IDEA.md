# Jupyter Notebook Redesign - Complete Design Document

## Overview

Transform the personal website into a Jupyter notebook-inspired interface that appeals to technical audiences (data professionals, potential employers in tech) while maintaining excellent readability for long-form content.

**Core Philosophy:** The notebook metaphor creates an authentic, technical aesthetic for the homepage and navigation, but steps back for blog posts to prioritize reading experience.

**Status:** Planning only. Implementation is not complete yet.

## Scope & Sequencing (must follow)

1) **Step 1 — Notebook pages only.** Build the notebook UI for the homepage and list pages (blog/books/articles/contact). Do **not** modify blog post templates or blog post typography in this step (global CSS loading changes are OK only if blog post appearance remains unchanged).
2) **Step 2 — Blog posts.** Add the notebook header to blog posts while keeping the existing 55ch reading width and `main.css` typography.
3) **Step 3 — Polish.** Hover states, spacing, contrast checks, and minor refinements only after Steps 1–2 land cleanly.

## Locked Decisions (current)

- Blog posts keep `55ch` line length (`main.css` stays the source of truth).
- List pages stay fully manual (no auto-generated lists).
- Substack embed stays at `https://maksymsherman.substack.com/embed`.
- CSS is separated by page type: notebook pages load `notebook.css`, blog posts load `main.css`, and a shared stylesheet is always loaded for fonts/vars/header.

## Risks & Watchouts

1. **CSS bleed:** Never load `main.css` and `notebook.css` together. Use conditional loading in `baseof.html`.
2. **Plain CSS only:** Avoid SCSS nesting in `notebook.css` or styles will silently fail.
3. **Manual counts drift:** Blog/books/articles counts must be updated by hand.
4. **Class alignment:** Ensure the HTML class names match the CSS (e.g., `nav-card` vs `nav-link`).

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

**Note on CSS Variable Conflicts:** main.css defines different book color values (`#00FF00`, `#00FFFF`, `#9E9E9E`). Move these variables into `shared.css` and remove them from main.css so there is a single source of truth.

### Background Colors
- **All pages:** Keep main.css gradient `linear-gradient(#2a2a29, #1c1c1c)` on html element
- The gradient works well for both notebook UI and blog reading
- notebook.css cell backgrounds (`#2d2d2d`) provide sufficient contrast against the gradient

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
- Paragraph: `16px`, line-height 1.6 (matches current site)
- Max-width: `55ch` on `.cell-body` for reading content

**Navigation cards:**
- Icon: `32px` (desktop), `28px` (mobile)
- Title: `18px` (desktop), `16px` (mobile), weight 500
- Description: `14px`, secondary color
- Count: `24px`, weight 600, blue accent

**Execution counts:**
- Gutter: `12px` (desktop), `11px` (mobile), monospace

### Font Sizes - Blog Posts (from main.css)

**Desktop:**
- Base: `16px` (browser default; do not override in Step 1)
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
- Max width: `55ch` (~500px, matches your current site's reading width)
- Centered with `margin: 0 auto`
- Padding: `30px 20px 50px` (desktop), `20px 10px 50px` (mobile)
- Mobile: `80%` max-width (same as current site)

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
  <a href="blog.html" class="nav-card">
    <span class="nav-card-icon">&#128221;</span>
    <div class="nav-card-title">blog <span class="nav-card-arrow">→</span></div>
    <div class="nav-card-description">Essays on economics, technology, and ideas</div>
    <div class="nav-card-count">16 posts</div>
  </a>
  <a href="books.html" class="nav-card">
    <span class="nav-card-icon">&#128218;</span>
    <div class="nav-card-title">books <span class="nav-card-arrow">→</span></div>
    <div class="nav-card-description">Reading list with ratings</div>
    <div class="nav-card-count">160 books</div>
  </a>
  <a href="articles.html" class="nav-card">
    <span class="nav-card-icon">&#128279;</span>
    <div class="nav-card-title">articles <span class="nav-card-arrow">→</span></div>
    <div class="nav-card-description">Best articles I've read</div>
    <div class="nav-card-count">70 links</div>
  </a>
  <a href="contact.html" class="nav-card">
    <span class="nav-card-icon">&#128231;</span>
    <div class="nav-card-title">contact <span class="nav-card-arrow">→</span></div>
    <div class="nav-card-description">Get in touch</div>
  </a>
</div>
```

**Class naming convention:** Use `nav-card-*` prefix consistently (matches notebook.css)

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
- **Max-width: `55ch`** (~500px, matches your current site's narrow reading width)
- Font size: `16px` (same as current site)
- H2: `20px`, bottom border, margin-top `24px`
- H3: `16px`, secondary color, margin-top `20px`
- Links: Blue (`#64b5f6`), underline on hover
- Lists: No bullet points, minimal padding
- Line-height: `1.6` for comfortable reading

**Key CSS addition for notebook.css:**
```css
.list-content {
  max-width: 55ch;  /* Narrow, readable line length */
  font-size: 16px;
  line-height: 1.6;
}
```

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
        <iframe src="https://maksymsherman.substack.com/embed" ...></iframe>
      </div>
    </div>
  </div>
</div>
```

**Styling:**
- Widget container: Centered with flexbox
- Padding: `20px 0`
- Iframe: Border `1px solid --border-color`, radius `4px`

**Migration Note:** Current blog posts use inline-styled iframes:
```html
<!-- BEFORE (current) -->
<iframe src="https://maksymsherman.substack.com/embed"
  style="border:1px solid #434343; background:#252525; width: 100%; max-width: 480px; height: 320px;">
</iframe>

<!-- AFTER (notebook style) -->
<div class="cell widget-cell">
  <div class="cell-content">
    <div class="cell-gutter">
      <span class="bracket">Out[</span>4<span class="bracket">]:</span>
    </div>
    <div class="cell-body">
      <div class="widget-container">
        <iframe src="https://maksymsherman.substack.com/embed"
          width="480" height="320" frameborder="0"></iframe>
      </div>
    </div>
  </div>
</div>
```

For blog posts, keep the simple inline iframe (no cell wrapper) since blog posts don't use notebook cells.

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

### Manual Counts

- Blog post count: manual number in the nav card
- Books count: manual number (`160`)
- Articles count: manual number (`70`)

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

**Note:** These code snippets are purely decorative; list content remains manual HTML.

---

## Blog Post Structure

**Design Decision:** Blog posts use a simplified layout - notebook header for branding, but standard typography for maximum readability. This is **Step 2 only**.

### Template (single.html)

```html
<header class="notebook-header">
  <div class="notebook-toolbar">
    <a href="/" class="notebook-title">
      <span class="icon">&#128211;</span>
      <span>maksym_sherman.ipynb</span>
    </a>
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

**Typography comes from main.css**, while **shared.css** provides:
- Notebook header styling
- Blog layout containers (`.blog-wrapper`, `.blog-container`)
- HR styling (already in `main.css`, unchanged)

**Key constraint:** `.blog-container { max-width: 55ch }` for optimal reading line length (matches your current site)

---

## CSS Architecture

### Separated Stylesheets (simple + low-risk)

**shared.css** - Loaded on every page
- Inter font-face declarations
- Shared CSS variables (book colors)
- Notebook header styles (used on notebook pages now; blog posts in Step 2)
- Blog wrapper/container layout helpers

**main.css** - Blog posts only
- Existing typography, colors, and 55ch width
- No notebook UI here

**notebook.css** - Notebook pages only
- Cell layout, gutters, syntax colors
- Output grids (nav cards, DataFrames, lists, widgets)
- Reading width constraints (`55ch` on text content, `900px` on decorative containers)

**Load Logic (in baseof.html):**
```html
<link rel="stylesheet" href="/shared.css">
{{ if or .IsHome (eq .Params.layout "notebook") }}
  <link rel="stylesheet" href="/notebook.css">
{{ else }}
  <link rel="stylesheet" href="/main.css">
{{ end }}
```

**Important:**
- Do NOT add universal resets to `notebook.css`.
- Do NOT use SCSS nesting in `notebook.css` (plain CSS only).

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
  <link rel="stylesheet" href="/shared.css">
  {{ if or .IsHome (eq .Params.layout "notebook") }}
    <link rel="stylesheet" href="/notebook.css">
  {{ else }}
    <link rel="stylesheet" href="/main.css">
  {{ end }}
  <title>{{ .Title | default .Site.Title }}</title>
</head>
<body>
  {{- block "main" . }}{{- end }}
</body>
</html>
```

### partials/notebook-header.html
Reusable notebook header shared by the homepage and list pages (and later blog posts).

### index.html
Homepage layout. Update `layouts/index.html` with the complete notebook structure:

```html
{{ define "main" }}
{{ partial "notebook-header.html" . }}

<main class="notebook">
  <!-- Cell 1: Import -->
  <div class="cell code-cell">
    <div class="cell-content">
      <div class="cell-gutter"><span class="bracket">In [</span>1<span class="bracket">]:</span></div>
      <div class="cell-body">
        <div class="code-input"><span class="keyword">from</span> <span class="variable">world</span> <span class="keyword">import</span> <span class="function">Person</span>
<span class="variable">me</span> = <span class="function">Person</span>(<span class="string">"Maksym Sherman"</span>)</div>
      </div>
    </div>
  </div>

  <!-- Cell 2: Intro (markdown) -->
  <div class="cell markdown-cell">
    <div class="cell-content">
      <div class="cell-gutter"></div>
      <div class="cell-body">
        <h1>Hi, I'm Maksym!</h1>
        <p>I believe in great work, ambition, and obsessiveness. I seek to understand the world through better explanations.</p>
      </div>
    </div>
  </div>

  <!-- Cell 3: Describe -->
  <div class="cell code-cell">
    <div class="cell-content">
      <div class="cell-gutter"><span class="bracket">In [</span>2<span class="bracket">]:</span></div>
      <div class="cell-body">
        <div class="code-input"><span class="variable">me</span>.<span class="function">describe</span>()</div>
      </div>
    </div>
  </div>

  <div class="cell output-cell">
    <div class="cell-content">
      <div class="cell-gutter"><span class="bracket">Out[</span>2<span class="bracket">]:</span></div>
      <div class="cell-body">
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
              <tr>
                <td class="index">previously</td>
                <td>OurNetwork, college endowment</td>
                <td>Crypto data newsletter, investing</td>
              </tr>
              <tr>
                <td class="index">always</td>
                <td>Looking to connect</td>
                <td>Curious people and ideas</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

  <!-- Cell 4: Navigation -->
  <div class="cell code-cell">
    <div class="cell-content">
      <div class="cell-gutter"><span class="bracket">In [</span>3<span class="bracket">]:</span></div>
      <div class="cell-body">
        <div class="code-input"><span class="variable">me</span>.<span class="function">get_sections</span>()  <span class="comment"># Explore my work</span></div>
      </div>
    </div>
  </div>

  <div class="cell output-cell">
    <div class="cell-content">
      <div class="cell-gutter"><span class="bracket">Out[</span>3<span class="bracket">]:</span></div>
      <div class="cell-body">
        <div class="nav-output">
          <a href="blog.html" class="nav-card">
            <span class="nav-card-icon">&#128221;</span>
            <div class="nav-card-title">blog <span class="nav-card-arrow">→</span></div>
            <div class="nav-card-description">Essays on economics, technology, and ideas</div>
            <div class="nav-card-count">16 posts</div>
          </a>
          <a href="books.html" class="nav-card">
            <span class="nav-card-icon">&#128218;</span>
            <div class="nav-card-title">books <span class="nav-card-arrow">→</span></div>
            <div class="nav-card-description">Reading list with ratings</div>
            <div class="nav-card-count">160 books</div>
          </a>
          <a href="articles.html" class="nav-card">
            <span class="nav-card-icon">&#128279;</span>
            <div class="nav-card-title">articles <span class="nav-card-arrow">→</span></div>
            <div class="nav-card-description">Best articles I've read</div>
            <div class="nav-card-count">70 links</div>
          </a>
          <a href="contact.html" class="nav-card">
            <span class="nav-card-icon">&#128231;</span>
            <div class="nav-card-title">contact <span class="nav-card-arrow">→</span></div>
            <div class="nav-card-description">Get in touch</div>
          </a>
        </div>
      </div>
    </div>
  </div>

  <!-- Cell 5: Newsletter -->
  <div class="cell code-cell">
    <div class="cell-content">
      <div class="cell-gutter"><span class="bracket">In [</span>4<span class="bracket">]:</span></div>
      <div class="cell-body">
        <div class="code-input"><span class="variable">me</span>.<span class="function">subscribe</span>()  <span class="comment"># Get notified of new posts</span></div>
      </div>
    </div>
  </div>

  <div class="cell widget-cell">
    <div class="cell-content">
      <div class="cell-gutter"><span class="bracket">Out[</span>4<span class="bracket">]:</span></div>
      <div class="cell-body">
        <div class="widget-container">
          <iframe src="https://maksymsherman.substack.com/embed" width="480" height="320" frameborder="0"></iframe>
        </div>
      </div>
    </div>
  </div>
</main>
{{ end }}
```

### single.html
Blog post layout with notebook header only. Update `layouts/_default/single.html`:

```html
{{ define "main" }}
{{ partial "notebook-header.html" . }}

<div class="blog-wrapper">
  <main class="blog-container">
    <article class="blog-post-content">
      {{ .Content }}
    </article>
  </main>
</div>
{{ end }}
```

Blog posts use main.css typography (not notebook cells) for optimal reading.

### notebook.html
List page layout for blog/books/articles/contact. Create at `layouts/_default/notebook.html`:
```html
{{ define "main" }}
{{ partial "notebook-header.html" . }}

<main class="notebook list-page">
  {{ .Content }}
</main>
{{ end }}
```

Content files (blog.html, books.html, etc.) contain the cell HTML structure directly. Example for blog.html:
```html
---
title: "Blog"
layout: notebook
---
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

<div class="cell output-cell">
  <div class="cell-content">
    <div class="cell-gutter">
      <span class="bracket">Out[</span>1<span class="bracket">]:</span>
    </div>
    <div class="cell-body">
      <div class="list-content">
        <h3>2025</h3>
        <p><a href="p/striking_while_the_iron_is_hot.html">Lyndon Johnson and Robert Caro</a></p>
        <!-- ... more posts ... -->
      </div>
    </div>
  </div>
</div>
```

### list.html
Keep as simple fallback (currently unused):

---

## Mobile Responsiveness

### Breakpoints

**768px and below:**
- Blog container: `max-width: 80%`, reduced padding
- Notebook: Reduced padding `20px 12px 40px`
- Navigation: Single column grid
- Font sizes: Explicit sizes for all headings (see Typography section)

**640px and below:**
- Notebook toolbar: Wraps, hides kernel indicator text (keep green dot)
- Cell gutter: `35px` width (down from 50px)
- Code input: `13px` font
- Output content: `12px` font
- Navigation cards: Reduced padding `16px`, smaller icons `28px`, smaller titles `16px`
- DataFrames: `11px` font, reduced cell padding

---

## Readability Guidelines

The notebook aesthetic must not compromise readability. **Core principle: decorative elements can be wide, but text people actually read must be narrow with large fonts.**

### Width Strategy (Critical)

Your current site uses `max-width: 55ch` (~500px) which is excellent for reading. Preserve this:

| Element | Max Width | Rationale |
|---------|-----------|-----------|
| **Notebook container** | `900px` | Decorative - holds cards, code cells, tables |
| **Reading text** (list content, paragraphs) | `55ch` (~500px) | Matches current site, optimal line length |
| **Blog posts** | `55ch` | Same narrow width for consistency |
| **Navigation cards grid** | `900px` | Decorative, visual element |
| **DataFrames** | `100%` of container | Tables can be wider, they're scannable |

**Implementation:**
```css
/* Notebook container can be wide */
.notebook {
  max-width: 900px;
}

/* But reading content inside stays narrow */
.list-content,
.markdown-cell .cell-body,
.blog-container {
  max-width: 55ch;  /* ~500px - matches your current site */
}
```

### Font Sizes (Match Current Site)
Your current site uses good sizes. Preserve or increase:
- **Body text:** 16px minimum (your current mobile size)
- **Paragraphs:** 16px with `line-height: 1.6`
- **Code cells:** 14px (monospace appears smaller, so slightly larger)
- **DataFrames:** 13px desktop, 12px mobile
- **Execution counts:** 12px (decorative, can be smaller)

### Color Contrast (WCAG AA)
| Text | Background | Ratio | Status |
|------|------------|-------|--------|
| `#e0e0e0` (primary) | `#1e1e1e` (bg) | 11.6:1 | ✅ |
| `#a0a0a0` (secondary) | `#1e1e1e` (bg) | 5.9:1 | ✅ |
| `#6a6a6a` (muted) | `#1e1e1e` (bg) | 2.9:1 | ⚠️ decorative only |
| `#64b5f6` (links) | `#1e1e1e` (bg) | 6.8:1 | ✅ |
| `#f0e7d5` (blog text) | `#1c1c1c` (blog bg) | 12.4:1 | ✅ |

### Mobile Width
On mobile, keep notebook containers slightly inset from the edges:
```css
@media (max-width: 768px) {
  .notebook {
    max-width: 90%;  /* Slight padding from edges */
  }
  .list-content,
  .markdown-cell .cell-body {
    max-width: 100%;  /* Fill the 90% container */
  }
}
```

### Touch Targets
- Navigation cards: Minimum 44x44px tap area
- Links in lists: 8px+ vertical spacing between items

### What Can Be Wide (Decorative)
- Notebook header (full width OK)
- Cell gutters with execution counts
- Navigation card grid
- DataFrame tables (with horizontal scroll)
- Code cell backgrounds

### What Must Be Narrow (Reading)
- Paragraph text in markdown cells
- List items (blog titles, book titles, article titles)
- Blog post content
- Contact information

---

## Implementation Notes

1. **No notebook cells for blog posts:** The cell wrapper adds friction for long-form reading. Use only the header in Step 2.
2. **Authentic but not literal:** Use real Jupyter patterns (execution counts, syntax highlighting, DataFrames) but don't force them where they don't fit.
3. **Mobile-first navigation:** Cards stack vertically on mobile, ensuring all content is accessible.
4. **Sticky header:** Notebook header stays visible on scroll for constant branding.
5. **Original typography for blogs:** Reading experience > aesthetic consistency. Blog posts use proven readable type.
6. **Header links to homepage:** Clicking "maksym_sherman.ipynb" navigates to `/` (index).
7. **Execution counts reset per page:** Each page starts at `In [1]:`. No global counter.
8. **Book colors stay inline:** `books.html` keeps inline `style="color: var(--book-green)"` for simplicity.
9. **404 page design (optional):**
   ```
   In [1]: me.find_page("/missing")
   Out[1]: PageNotFoundError: The requested page does not exist.
   ```

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

## Implementation Checklist (Step-by-step)

### Step 1 — Notebook pages only (DO NOT touch blog posts)
- [ ] Create `hugo-site/static/shared.css` for fonts + shared variables + notebook header + blog container helpers
- [ ] Create `hugo-site/static/notebook.css` with all notebook UI styles
- [ ] Update `hugo-site/layouts/_default/baseof.html` to conditionally load `notebook.css` or `main.css`
- [ ] Add `hugo-site/layouts/partials/notebook-header.html`
- [ ] Add `hugo-site/layouts/_default/notebook.html` (list pages)
- [ ] Update `hugo-site/layouts/index.html` with notebook header + cells
- [ ] Add `layout: notebook` to `hugo-site/content/blog.html`, `books.html`, `articles.html`, `contact.html`
- [ ] Wrap list-page content in code/output cells (manual content stays)
- [ ] Ensure Substack embed uses `https://maksymsherman.substack.com/embed`
- [ ] Smoke-check homepage + list pages only

### Step 2 — Blog posts (after Step 1 is merged)
- [ ] Update `hugo-site/layouts/_default/single.html` to add the notebook header
- [ ] Keep `main.css` typography and `55ch` width unchanged
- [ ] Check a few existing posts for layout regressions

### Step 3 — Polish
- [ ] Refine hover states, spacing, and mobile breakpoints
- [ ] Fix any HTML/CSS class mismatches (e.g., `nav-card` vs `nav-link`)
- [ ] Optional: add notebook-themed 404 and other extras

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
│   │   ├── baseof.html          # Base template (conditional CSS load)
│   │   ├── single.html          # Blog post layout
│   │   ├── notebook.html        # List page layout
│   │   └── list.html            # (unused)
│   └── index.html               # Homepage layout
│   └── partials/
│       └── notebook-header.html # Shared notebook header
├── static/
│   ├── shared.css               # Fonts + shared vars + header helpers
│   ├── main.css                 # Blog post typography (unchanged)
│   ├── notebook.css             # Notebook UI theme
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

## Current State Summary

**What already exists:**
- `hugo-site/static/main.css` - blog typography and base styles (keep for posts)
- `hugo-site/layouts/_default/baseof.html` - base template (needs conditional CSS load)
- `hugo-site/layouts/index.html` - homepage layout (needs notebook cells)
- `hugo-site/layouts/_default/single.html` - blog post layout (Step 2 header only)
- All content files exist but use plain HTML (need notebook cell structure for list pages)

**What needs to be created:**
- `hugo-site/static/shared.css` - fonts + shared vars + header helpers
- `hugo-site/static/notebook.css` - notebook UI styles
- `hugo-site/layouts/_default/notebook.html` - list page layout
- `hugo-site/layouts/partials/notebook-header.html` - shared header

**What needs to be updated:**
- baseof.html: conditional CSS load (`shared.css` + `notebook.css` or `main.css`)
- index.html: add full notebook cell structure
- blog/books/articles/contact content: wrap in notebook cell structure + `layout: notebook`
- single.html (Step 2): add notebook header only

---

## Known Issues

### Step 1 Implementation Issues

~~1. **Code cell text alignment:** Code input text within cells may appear visually centered instead of left-aligned despite `text-align: left` being set. This is a visual rendering issue that needs further investigation.~~

**RESOLVED (2026-01-02):** The alignment issue was caused by HTML whitespace. List pages (blog.html, books.html, articles.html, contact.html) had newlines after the `<div class="code-input">` opening tag, creating unwanted whitespace that misaligned the code with the "In [1]:" gutter labels. Fixed by placing code content on the same line as the opening tag, matching the structure in index.html.

**Critical formatting rule for code cells:**
```html
<!-- CORRECT - code on same line as opening tag -->
<div class="code-input"><span class="variable">me</span>.<span class="function">list_posts</span>()</div>

<!-- WRONG - newline creates whitespace and misalignment -->
<div class="code-input">
  <span class="variable">me</span>.<span class="function">list_posts</span>()
</div>
```

---

## Implementation Notes - Step 1 (Completed 2026-01-02)

### Changes from Original Design Doc

1. **Navigation cards → Navigation links:** Changed from vertical card layout to horizontal list-style links for cleaner appearance
   - Structure: Icon (left) → Title (middle) → Count (right)
   - Removed descriptions for simpler design
   - Changed classes from `nav-card-*` to `nav-link`, `nav-icon`, `nav-content`, `nav-title`, `nav-desc`, `nav-meta`

2. **Notebook container width:** Reduced from 900px to 700px for narrower, more readable layout matching live site feel

3. **Cell hover behavior:** Set `border-left: 3px solid transparent` on default state to prevent 2px shift on hover (was changing from 1px to 3px)

4. **DataFrame "previously" row:** Simplified content
   - Status: `OurNetwork` (removed ", college endowment")
   - Description: `Crypto data newsletter` (removed ", investing")

5. **Kernel indicator position:** Kept on the right side of header (changed from initial left-side experiment)

### Files Created
- `hugo-site/static/shared.css` (fonts, variables, header, blog helpers)
- `hugo-site/static/notebook.css` (notebook UI)
- `hugo-site/layouts/partials/notebook-header.html`
- `hugo-site/layouts/_default/notebook.html`

### Files Modified
- `hugo-site/layouts/_default/baseof.html` (conditional CSS loading)
- `hugo-site/layouts/index.html` (full notebook structure)
- `hugo-site/content/blog.html` (notebook cells + layout)
- `hugo-site/content/books.html` (notebook cells + layout)
- `hugo-site/content/articles.html` (notebook cells + layout)
- `hugo-site/content/contact.html` (notebook cells + layout)

---

**Last Updated:** 2026-01-02
**Branch:** redesign
**Status:** Step 1 Complete; Step 2 Pending
