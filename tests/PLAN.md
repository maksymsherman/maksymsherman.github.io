# Test Plan: Additional Automated Checks

This document describes all planned automated tests beyond the existing link checker (`check_links.py`).

## Tests Overview

| # | Check | File | When it runs |
|---|-------|------|-------------|
| 1 | Hugo build emits no warnings | `check-links.yml` (workflow) | After Hugo build |
| 2 | All posts have required front matter | `check_build.py` | Before build (content only) |
| 3 | JSON-LD blocks are valid JSON | `check_build.py` | After build (public/) |
| 4 | Markdown alternates exist for all posts | `check_build.py` | After build (public/) |
| 5 | RSS feed contains all posts | `check_build.py` | After build (public/) |
| 6 | OG share image exists for all posts | `check_build.py` | Before build (static/) |

---

## Check 1: Hugo Build Warnings

**Why:** Hugo exits 0 even when templates error silently (e.g. missing partial, bad variable). WARN lines in build output indicate real problems.

**Implementation:** In `check-links.yml`, capture Hugo stdout/stderr and fail if any `WARN` lines appear:
```bash
hugo --gc --minify ... 2>&1 | tee /tmp/hugo_build.log
grep -qE "^WARN" /tmp/hugo_build.log && echo "Hugo emitted warnings:" && grep -E "^WARN" /tmp/hugo_build.log && exit 1 || true
```

---

## Check 2: Front Matter Completeness

**Why:** Missing `description` silently breaks `<meta name="description">`, OpenGraph description, and LLM hints. Missing `date` breaks RSS ordering.

**Required fields:** `title`, `date`, `description` in YAML front matter of every `content/posts/*.md` (except `_index.md`).

**Implementation:** Parse front matter between `---` delimiters with regex. No PyYAML needed.

**Currently:** All 16 posts have all three fields.

---

## Check 3: JSON-LD Validity

**Why:** JSON-LD blocks are hand-authored raw HTML inside Markdown. A missing quote or bracket is invisible at build time but breaks structured data for Google/LLMs.

**Pages with JSON-LD:**
- All blog posts (`BlogPosting` schema in `baseof.html` template)
- `blog/index.html` (`ItemList` schema in `blog.md` source)
- `index.html` (`WebSite` + `Person` schemas)

**Implementation:** Scan all `public/**/*.html` for `<script type="application/ld+json">` blocks, attempt `json.loads()` on each, report parse errors.

---

## Check 4: Markdown Alternates Exist

**Why:** Hugo is configured to output both `index.html` and `index.md` for every post (`page = ["html", "markdown"]` in `hugo.toml`). If the markdown template breaks, Hugo silently skips the `.md` file. LLM agents then get a 404 when they try to fetch the markdown version.

**Implementation:** For every directory in `public/p/*/`, verify both `index.html` and `index.md` exist.

---

## Check 5: RSS Feed Coverage

**Why:** If Hugo silently fails to process a post (e.g. bad front matter date format), the post won't appear in `public/index.xml`. This is invisible from the built HTML.

**Implementation:** Parse `public/index.xml` with `xml.etree.ElementTree` (stdlib), count `<item>` elements, compare to count of `content/posts/*.md` (excluding `_index.md`). Fail if counts differ.

---

## Check 6: OG Share Image Exists

**Why:** The template in `baseof.html` generates `<meta property="og:image" content=".../images/share/{slug}.png">` for every post. If the file doesn't exist, social sharing silently shows a broken image.

**Implementation:** For every `content/posts/*.md` (excluding `_index.md`), verify `static/images/share/{slug}.png` exists.

**Currently:** All 16 posts have share images.

---

## Files Changed

- **New:** `tests/check_build.py` — implements checks 2–6
- **Updated:** `.github/workflows/check-links.yml` — adds check 1 (warning grep) + calls `check_build.py`

---

## Running Locally

```bash
# Build first (required for checks 3, 4, 5)
cd hugo-site && hugo --gc --minify && cd ..

# Run all build checks
python3 tests/check_build.py

# Run link checks (already exists)
python3 tests/check_links.py
```
