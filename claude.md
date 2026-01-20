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

## Agent Coordination Tools

This project uses the Dicklesworthstone stack for multi-agent coordination, task management, and workflow automation. These tools work alongside the project-specific documentation above.

### Core Rules

**RULE 1 – ABSOLUTE (DO NOT EVER VIOLATE THIS)**

You may NOT delete any file or directory unless I explicitly give the exact command **in this session**.

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

---

### Using bv as an AI sidecar

bv is a graph-aware triage engine for Beads projects (.beads/beads.jsonl). Instead of parsing JSONL or hallucinating graph traversal, use robot flags for deterministic, dependency-aware outputs with precomputed metrics (PageRank, betweenness, critical path, cycles, HITS, eigenvector, k-core).

**Scope boundary:** bv handles *what to work on* (triage, priority, planning). For agent-to-agent coordination (messaging, work claiming, file reservations), use MCP Agent Mail, which should be available to you as an MCP server (if it's not, then flag to the user; they might need to start Agent Mail using the `am` alias or by running `cd "<directory_where_they_installed_agent_mail>/mcp_agent_mail" && bash scripts/run_server_with_token.sh)` if the alias isn't available or isn't working.

**⚠️ CRITICAL: Use ONLY `--robot-*` flags. Bare `bv` launches an interactive TUI that blocks your session.**

#### The Workflow: Start With Triage

**`bv --robot-triage` is your single entry point.** It returns everything you need in one call:
- `quick_ref`: at-a-glance counts + top 3 picks
- `recommendations`: ranked actionable items with scores, reasons, unblock info
- `quick_wins`: low-effort high-impact items
- `blockers_to_clear`: items that unblock the most downstream work
- `project_health`: status/type/priority distributions, graph metrics
- `commands`: copy-paste shell commands for next steps

```bash
bv --robot-triage        # THE MEGA-COMMAND: start here
bv --robot-next          # Minimal: just the single top pick + claim command
```

#### Other bv Commands

**Planning:**
| Command | Returns |
|---------|---------|
| `--robot-plan` | Parallel execution tracks with `unblocks` lists |
| `--robot-priority` | Priority misalignment detection with confidence |

**Graph Analysis:**
| Command | Returns |
|---------|---------|
| `--robot-insights` | Full metrics: PageRank, betweenness, HITS (hubs/authorities), eigenvector, critical path, cycles, k-core, articulation points, slack |
| `--robot-label-health` | Per-label health: `health_level` (healthy\|warning\|critical), `velocity_score`, `staleness`, `blocked_count` |
| `--robot-label-flow` | Cross-label dependency: `flow_matrix`, `dependencies`, `bottleneck_labels` |
| `--robot-label-attention [--attention-limit=N]` | Attention-ranked labels by: (pagerank × staleness × block_impact) / velocity |

**History & Change Tracking:**
| Command | Returns |
|---------|---------|
| `--robot-history` | Bead-to-commit correlations: `stats`, `histories` (per-bead events/commits/milestones), `commit_index` |
| `--robot-diff --diff-since <ref>` | Changes since ref: new/closed/modified issues, cycles introduced/resolved |

**Other Commands:**
| Command | Returns |
|---------|---------|
| `--robot-burndown <sprint>` | Sprint burndown, scope changes, at-risk items |
| `--robot-forecast <id\|all>` | ETA predictions with dependency-aware scheduling |
| `--robot-alerts` | Stale issues, blocking cascades, priority mismatches |
| `--robot-suggest` | Hygiene: duplicates, missing deps, label suggestions, cycle breaks |
| `--robot-graph [--graph-format=json\|dot\|mermaid]` | Dependency graph export |
| `--export-graph <file.html>` | Self-contained interactive HTML visualization |

#### Scoping & Filtering

```bash
bv --robot-plan --label backend              # Scope to label's subgraph
bv --robot-insights --as-of HEAD~30          # Historical point-in-time
bv --recipe actionable --robot-plan          # Pre-filter: ready to work (no blockers)
bv --recipe high-impact --robot-triage       # Pre-filter: top PageRank scores
bv --robot-triage --robot-triage-by-track    # Group by parallel work streams
bv --robot-triage --robot-triage-by-label    # Group by domain
```

#### Understanding Robot Output

**All robot JSON includes:**
- `data_hash` — Fingerprint of source beads.jsonl (verify consistency across calls)
- `status` — Per-metric state: `computed|approx|timeout|skipped` + elapsed ms
- `as_of` / `as_of_commit` — Present when using `--as-of`; contains ref and resolved SHA

**Two-phase analysis:**
- **Phase 1 (instant):** degree, topo sort, density — always available immediately
- **Phase 2 (async, 500ms timeout):** PageRank, betweenness, HITS, eigenvector, cycles — check `status` flags

**For large graphs (>500 nodes):** Some metrics may be approximated or skipped. Always check `status`.

#### jq Quick Reference

```bash
bv --robot-triage | jq '.quick_ref'                        # At-a-glance summary
bv --robot-triage | jq '.recommendations[0]'               # Top recommendation
bv --robot-plan | jq '.plan.summary.highest_impact'        # Best unblock target
bv --robot-insights | jq '.status'                         # Check metric readiness
bv --robot-insights | jq '.Cycles'                         # Circular deps (must fix!)
bv --robot-label-health | jq '.results.labels[] | select(.health_level == "critical")'
```

**Performance:** Phase 1 instant, Phase 2 async (500ms timeout). Prefer `--robot-plan` over `--robot-insights` when speed matters. Results cached by data hash.

Use bv instead of parsing beads.jsonl—it computes PageRank, critical paths, cycles, and parallel tracks deterministically.

---

### Morph Warp Grep — AI-Powered Code Search

Use `mcp__morph-mcp__warp_grep` for "how does X work?" discovery across the codebase.

When to use:

- You don't know where something lives.
- You want data flow across multiple files (layout → partial → CSS).
- You want all touchpoints of a cross-cutting concern.

Example:

```
mcp__morph-mcp__warp_grep(
  repoPath: "/data/projects/maksym-site",
  query: "How is the Jupyter notebook interface implemented?"
)
```

Warp Grep:

- Expands a natural-language query to multiple search patterns.
- Runs targeted greps, reads code, follows imports, then returns concise snippets with line numbers.
- Reduces token usage by returning only relevant slices, not entire files.

When **not** to use Warp Grep:

- You already know the function/identifier name; use `rg`.
- You know the exact file; just open it.
- You only need a yes/no existence check.

Comparison:

| Scenario | Tool |
| ---------------------------------- | ---------- |
| "How is auth session validated?" | warp_grep |
| "Where is `handleSubmit` defined?" | `rg` |
| "Replace `var` with `let`" | `ast-grep` |

---

### cass — Cross-Agent Search

`cass` indexes prior agent conversations (Claude Code, Codex, Cursor, Gemini, ChatGPT, etc.) so we can reuse solved problems.

Rules:

- Never run bare `cass` (TUI). Always use `--robot` or `--json`.

Examples:

```bash
cass health
cass search "authentication error" --robot --limit 5
cass view /path/to/session.jsonl -n 42 --json
cass expand /path/to/session.jsonl -n 42 -C 3 --json
cass capabilities --json
cass robot-docs guide
```

Tips:

- Use `--fields minimal` for lean output.
- Filter by agent with `--agent`.
- Use `--days N` to limit to recent history.

stdout is data-only, stderr is diagnostics; exit code 0 means success.

Treat cass as a way to avoid re-solving problems other agents already handled.

---

### Memory System: cass-memory

The Cass Memory System (cm) is a tool for giving agents an effective memory based on the ability to quickly search across previous coding agent sessions across an array of different coding agent tools (e.g., Claude Code, Codex, Gemini-CLI, Cursor, etc) and projects (and even across multiple machines, optionally) and then reflect on what they find and learn in new sessions to draw out useful lessons and takeaways; these lessons are then stored and can be queried and retrieved later, much like how human memory works.

The `cm onboard` command guides you through analyzing historical sessions and extracting valuable rules.

#### Quick Start

```bash
# 1. Check status and see recommendations
cm onboard status

# 2. Get sessions to analyze (filtered by gaps in your playbook)
cm onboard sample --fill-gaps

# 3. Read a session with rich context
cm onboard read /path/to/session.jsonl --template

# 4. Add extracted rules (one at a time or batch)
cm playbook add "Your rule content" --category "debugging"
# Or batch add:
cm playbook add --file rules.json

# 5. Mark session as processed
cm onboard mark-done /path/to/session.jsonl
```

Before starting complex tasks, retrieve relevant context:

```bash
cm context "<task description>" --json
```

This returns:
- **relevantBullets**: Rules that may help with your task
- **antiPatterns**: Pitfalls to avoid
- **historySnippets**: Past sessions that solved similar problems
- **suggestedCassQueries**: Searches for deeper investigation

#### Protocol

1. **START**: Run `cm context "<task>" --json` before non-trivial work
2. **WORK**: Reference rule IDs when following them (e.g., "Following b-8f3a2c...")
3. **FEEDBACK**: Leave inline comments when rules help/hurt:
   - `// [cass: helpful b-xyz] - reason`
   - `// [cass: harmful b-xyz] - reason`
4. **END**: Just finish your work. Learning happens automatically.

#### Key Flags

| Flag | Purpose |
|------|---------|
| `--json` | Machine-readable JSON output (required!) |
| `--limit N` | Cap number of rules returned |
| `--no-history` | Skip historical snippets for faster response |

stdout = data only, stderr = diagnostics. Exit 0 = success.

---

### UBS Quick Reference for AI Agents

UBS stands for "Ultimate Bug Scanner": **The AI Coding Agent's Secret Weapon: Flagging Likely Bugs for Fixing Early On**

**Golden Rule:** `ubs <changed-files>` before every commit. Exit 0 = safe. Exit >0 = fix & re-run.

**Commands:**
```bash
ubs file.ts file2.py                    # Specific files (< 1s) — USE THIS
ubs $(git diff --name-only --cached)    # Staged files — before commit
ubs --only=js,python src/               # Language filter (3-5x faster)
ubs --ci --fail-on-warning .            # CI mode — before PR
ubs --help                              # Full command reference
ubs sessions --entries 1                # Tail the latest install session log
ubs .                                   # Whole project (ignores things like .venv and node_modules automatically)
```

**Output Format:**
```
⚠️  Category (N errors)
    file.ts:42:5 – Issue description
    💡 Suggested fix
Exit code: 1
```
Parse: `file:line:col` → location | 💡 → how to fix | Exit 0/1 → pass/fail

**Fix Workflow:**
1. Read finding → category + fix suggestion
2. Navigate `file:line:col` → view context
3. Verify real issue (not false positive)
4. Fix root cause (not symptom)
5. Re-run `ubs <file>` → exit 0
6. Commit

**Speed Critical:** Scope to changed files. `ubs src/file.ts` (< 1s) vs `ubs .` (30s). Never full scan for small edits.

**Bug Severity:**
- **Critical** (always fix): Null safety, XSS/injection, async/await, memory leaks
- **Important** (production): Type narrowing, division-by-zero, resource leaks
- **Contextual** (judgment): TODO/FIXME, console logs

**Anti-Patterns:**
- ❌ Ignore findings → ✅ Investigate each
- ❌ Full scan per edit → ✅ Scope to file
- ❌ Fix symptom (`if (x) { x.y }`) → ✅ Root cause (`x?.y`)

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

---

### RU Quick Reference for AI Agents

RU (Repo Updater) is a multi-repo sync tool with **AI-driven commit automation**.

**Common Commands:**
```bash
ru sync                        # Clone missing + pull updates for all repos
ru sync --parallel 4           # Parallel sync (4 workers)
ru status                      # Check repo status without changes
ru status --fetch              # Fetch + show ahead/behind
ru list --paths                # List all repo paths
```

**Agent Sweep (commit automation):**
```bash
ru agent-sweep --dry-run       # Preview dirty repos to process
ru agent-sweep --parallel 4    # AI-driven commits in parallel
ru agent-sweep --with-release  # Include version tag + release
```

**Exit Codes:**
- `0` = Success
- `1` = Partial failure (some repos failed)
- `2` = Conflicts exist (manual resolution needed)
- `5` = Interrupted (use `--resume`)

**Best Practices:**
- Use `ru status` before `ru sync` to preview changes
- Use `ru agent-sweep --dry-run` before full automation
- Scope with `--repos=pattern` for targeted operations

---

### giil Quick Reference for AI Agents

giil (Get Image from Internet Link) downloads **cloud-hosted images** to the terminal for visual debugging.

**Usage:**
```bash
giil "https://share.icloud.com/..."       # Download iCloud photo
giil "https://www.dropbox.com/s/..."      # Download Dropbox image
giil "https://photos.google.com/..."      # Download Google Photos image
giil "..." --output ~/screenshots         # Custom output directory
giil "..." --json                         # JSON metadata output
giil "..." --all                          # Download all photos from album
```

**Supported Platforms:**
- iCloud (share.icloud.com)
- Dropbox (dropbox.com/s/, dl.dropbox.com)
- Google Photos (photos.google.com)
- Google Drive (drive.google.com)

**Exit Codes:**
- `0` = Success
- `10` = Network error
- `11` = Auth required (not publicly shared)
- `12` = Not found (expired link)
- `13` = Unsupported type (video, doc)

**Visual Debugging Workflow:**
1. User screenshots bug on phone
2. Shares iCloud/Dropbox link with agent
3. `giil "<url>"` downloads to working directory
4. Agent analyzes the image

---

### csctf Quick Reference for AI Agents

csctf (Chat Shared Conversation to File) converts **AI chat share links** to Markdown/HTML.

**Usage:**
```bash
csctf "https://chatgpt.com/share/..."      # ChatGPT conversation
csctf "https://gemini.google.com/share/..." # Gemini conversation
csctf "https://claude.ai/share/..."         # Claude conversation
csctf "..." --md-only                       # Markdown only (no HTML)
csctf "..." --json                          # JSON metadata output
csctf "..." --publish-to-gh-pages --yes     # Publish to GitHub Pages
```

**Output:**
- `<slug>.md` — Clean Markdown with code blocks
- `<slug>.html` — Static HTML with syntax highlighting

**Use Cases:**
- Archive important AI conversations for reference
- Build searchable knowledge base
- Share solutions with team members
- Document debugging sessions for future learning

---

**Last Updated:** 2026-01-20

### Recent Changes

**2026-01-20** - Dicklesworthstone Stack Integration
- Added comprehensive Agent Coordination Tools section
- Documented core rules (RULE 1: no deletions, irreversible actions protocol)
- Added landing the plane (session completion) workflow
- Comprehensive tool documentation: br, bv, cass, cm, ubs, dcg, ru, giil, csctf
- Established multi-agent coordination protocols
- Beads issue tracking with ms prefix for this project



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
