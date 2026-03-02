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

---

## Testing Locally

**MANDATORY: Run tests before every commit.** Build the site and run both test scripts. All checks must pass before committing.

```bash
cd hugo-site && hugo --quiet && cd ..
python3 tests/check_build.py
python3 tests/check_links.py
```

If any check fails, fix the issue and re-run before committing.

**Dev server for visual testing:**

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
- Markdown alternate output for all pages (`/p/slug/index.md` alongside `/p/slug/`)

**Markdown Alternate Discovery:**
Every page that has a markdown output includes two machine-readable hints so LLM agents can find the clean version without needing `llms.txt` first:
1. `<link rel="alternate" type="text/markdown" href="...index.md">` in `<head>` (standard HTML alternate link)
2. `<!-- AI/LLM hint: ... Markdown-only version ... available at .../index.md -->` HTML comment at top of `<body>`

Configured via `page = ["html", "markdown"]` in `hugo.toml` `[outputs]`. The markdown template is `layouts/_default/single.md`. Homepage does not get markdown output (only html, rss, llmstxt).

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
1. Create file in `hugo-site/content/posts/`
2. Add link to `hugo-site/content/blog.md`

**Adding a new book:**
1. Add entry to `hugo-site/content/books.md` under the appropriate year section
2. Use inline style for color: `style="color: var(--book-green)"`

---

## Agent Coordination Tools

This project uses the Dicklesworthstone stack for multi-agent coordination, task management, and workflow automation. These tools work alongside the project-specific documentation above.

### Core Rules

**RULE 1 – ABSOLUTE (DO NOT EVER VIOLATE THIS)**

You may NOT delete any file or directory unless I explicitly give the exact command **in this session**.

**RULE 2 – BRANCH AND PR WORKFLOW (MANDATORY)**

Agents must NEVER merge branches. The user will manually merge all PRs in GitHub.

- Always work on feature branches (e.g., `feature/add-llm-discovery`, `fix/mobile-header`)
- Create a Pull Request when work is complete
- NEVER run `git merge` commands - the user merges all PRs manually in GitHub
- NEVER merge to main, even with explicit approval - always let user merge in GitHub UI

Workflow:
1. Create a new branch: `git checkout -b feature/your-feature-name`
2. Make changes and commit
3. Push branch: `git push -u origin feature/your-feature-name`
4. Open PR: `gh pr create --title "..." --body "..."`
5. STOP - user will merge in GitHub when ready

- This includes files you just created (tests, tmp files, scripts, etc.).
- You do not get to decide that something is "safe" to remove.
- If you think something should be removed, stop and ask. You must receive clear written approval **before** any deletion command is even proposed.

**Irreversible Git & Filesystem Actions**

Absolutely forbidden unless I give the **exact command and explicit approval** in the same message:

- `git reset --hard`
- `git clean -fd`
- `rm -rf`
- Any command that can delete or overwrite code/data

Rules:
1. If you are not 100% sure what a command will delete, do not propose or run it. Ask first.
2. Prefer safe tools: `git status`, `git diff`, `git stash`, copying to backups, etc.
3. After approval, restate the command verbatim, list what it will affect, and wait for confirmation.

### Landing the Plane (Session Completion)

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create beads for anything that needs follow-up
2. **Run quality gates** (if code changed) - Hugo build, UBS scan if applicable
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   br sync --flush-only
   git add .beads/
   git commit -m "Update beads"
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds

### Issue Tracking with br (Beads)

All issue tracking goes through **Beads**. No other TODO systems.

**Note:** `br` is a convenience alias (installed by `acfs/zsh/acfs.zshrc`) for the real Beads CLI: `bd`.
If `br` is unavailable (CI / non-interactive shells), use `bd` directly.

Key invariants:

- `.beads/` is authoritative state and **must always be committed** with code changes.
- Do not edit `.beads/*.jsonl` directly; only via `br` / `bd`.

#### Basics

Check ready work:

```bash
br ready --json
```

Create issues:

```bash
br create "Issue title" -t bug|feature|task -p 0-4 --json
br create "Issue title" -p 1 --deps discovered-from:ms-123 --json
```

Update:

```bash
br update ms-42 --status in_progress --json
br update ms-42 --priority 1 --json
```

Complete:

```bash
br close ms-42 --reason "Completed" --json
```

Types:

- `bug`, `feature`, `task`, `epic`, `chore`

Priorities:

- `0` critical (security, data loss, broken builds)
- `1` high
- `2` medium (default)
- `3` low
- `4` backlog

Agent workflow:

1. `br ready` to find unblocked work.
2. Claim: `br update <id> --status in_progress`.
3. Implement + test.
4. If you discover new work, create a new bead with `discovered-from:<parent-id>`.
5. Close when done.
6. Commit `.beads/` in the same commit as code changes.

Sync:

- Run `br sync --flush-only` (or `bd sync --flush-only`) to export to `.beads/issues.jsonl` without git operations.
- Then run `git add .beads/ && git commit -m "Update beads"` to commit changes.

Never:

- Use markdown TODO lists.
- Use other trackers.
- Duplicate tracking.

### Additional Tool References

For detailed documentation on bv, cass, cm, ubs, ru, giil, csctf, and Morph Warp Grep, see [AGENT_TOOLS.md](AGENT_TOOLS.md). Only consult that file when working on coordination tasks or using Beads issue tracking.

---

### DCG Quick Reference for AI Agents

DCG (Destructive Command Guard) is a Claude Code hook that **blocks dangerous git and filesystem commands** before execution. Sub-millisecond latency, mechanical enforcement.

**Golden Rule:** DCG works automatically—you don't need to call it. When a dangerous command is blocked, use safer alternatives or ask the user to run it manually.

**Commands:**
```bash
dcg test "<cmd>" [--explain]          # Test if a command would be blocked
dcg packs [--enabled] [--verbose]     # List packs
dcg pack <pack-id> [--patterns]       # Pack details + match patterns
dcg allow-once <code>                 # One-time bypass code
dcg allow <rule-id> --reason "..."    # Add allowlist entry (project/user)
dcg doctor [--fix] [--format json]    # Health check + auto-fix
dcg install [--force]                 # Register Claude Code hook
dcg uninstall [--purge]               # Remove hook (and optionally binary/config)
```

**Auto-Blocked Commands:**
```bash
git reset --hard               # Destroys uncommitted changes
git checkout -- <files>        # Discards file changes permanently
git restore <files>            # Same as checkout -- (not --staged)
git push --force / -f          # Overwrites remote history
git clean -f                   # Deletes untracked files
git branch -D                  # Force-deletes without merge check
git stash drop / clear         # Permanently deletes stashes
rm -rf <non-temp>              # Recursive deletion
```

**Always Allowed:**
```bash
git checkout -b <branch>       # Creates branch, doesn't touch files
git restore --staged           # Only unstages, safe
git clean -n                   # Dry-run, preview only
rm -rf /tmp/...                # Temp directories are ephemeral
git push --force-with-lease    # Safe force push variant
```

**When Blocked:**
- You'll see a clear reason explaining why
- Ask the user to run the command manually if truly needed
- Consider safer alternatives (git stash, --force-with-lease)

**Configuration:**
- Config file: `~/.config/dcg/config.toml`
- View available packs: `dcg packs` (shows all), `dcg packs --enabled` (shows active)
- Pack examples: `git`, `filesystem`, `database.postgresql`, `containers.docker`, `kubernetes`
```toml
# ~/.config/dcg/config.toml
[packs]
enabled = ["git", "filesystem", "database.postgresql", "containers.docker"]
```
- Allowlist management: `dcg allow <rule-id> --reason "..." --project <path>` (or `--user`)

**Common Scenarios:**
- **Blocked command** → Read the reason, prefer the safer alternative, or use `dcg allow-once <code>`.
- **Hook missing after updates** → `dcg install --force`.
- **Need to disable** → `dcg uninstall` (or `dcg uninstall --purge` for full removal).

**Troubleshooting:**

| Issue | Solution |
|-------|----------|
| DCG blocks legitimate command | Ask user to run manually, or use allow-once code if provided |
| Hook not registered | Run `dcg install` |
| DCG not blocking anything | Run `dcg doctor` to verify hook is active |
| False positive | Check if command matches safe patterns; report to GitHub if bug |
| Config not being read | Verify `~/.config/dcg/config.toml` format is valid TOML |

**Agent Integration Tips:**
- DCG is automatic—no need to call `dcg test` before commands
- When blocked, explain to user why the command is dangerous
- Suggest safer alternatives (e.g., `--force-with-lease` instead of `--force`)
- Never try to bypass DCG—ask user to run dangerous commands manually
- DCG has sub-millisecond latency, designed to not slow down your workflow
