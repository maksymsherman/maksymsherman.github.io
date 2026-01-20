# CLAUDE.md — Agent Instructions for maksym-site

This file contains agent-specific instructions for working on Maksym Sherman's personal website. This project uses the Dicklesworthstone stack for multi-agent coordination and task management.

---

## RULE 1 – ABSOLUTE (DO NOT EVER VIOLATE THIS)

You may NOT delete any file or directory unless I explicitly give the exact command **in this session**.

- This includes files you just created (tests, tmp files, scripts, etc.).
- You do not get to decide that something is "safe" to remove.
- If you think something should be removed, stop and ask. You must receive clear written approval **before** any deletion command is even proposed.

Treat "never delete files without permission" as a hard invariant.

---

## IRREVERSIBLE GIT & FILESYSTEM ACTIONS

Absolutely forbidden unless I give the **exact command and explicit approval** in the same message:

- `git reset --hard`
- `git clean -fd`
- `rm -rf`
- Any command that can delete or overwrite code/data

Rules:

1. If you are not 100% sure what a command will delete, do not propose or run it. Ask first.
2. Prefer safe tools: `git status`, `git diff`, `git stash`, copying to backups, etc.
3. After approval, restate the command verbatim, list what it will affect, and wait for confirmation.
4. When a destructive command is run, record in your response:
   - The exact user text authorizing it
   - The command run
   - When you ran it

If that audit trail is missing, then you must act as if the operation never happened.

---

## Project Overview

**Type:** Hugo static site (v0.154.0 extended)
**Deployment:** GitHub Pages via GitHub Actions
**Content:** Personal website with blog posts, book recommendations, and articles
**Python Tooling:** UV + Pillow for OpenGraph share image generation

### Key Directories

```
maksym-site/
├── hugo-site/              # Main Hugo site
│   ├── content/            # Markdown/HTML content
│   ├── layouts/            # Hugo templates
│   ├── assets/             # CSS, fonts, images
│   └── public/             # Build output (gitignored)
├── .beads/                 # Beads task management
├── .claude/commands/       # CLI skill definitions
└── claude.md               # Full project documentation
```

**Always read `claude.md` for comprehensive project-specific details before making changes.**

---

## Hugo Development Workflow

```bash
# Local development server
cd hugo-site && hugo server --noHTTPCache --disableFastRender

# Build site (output to public/)
cd hugo-site && hugo

# Deployment: Push to main → GitHub Actions builds and deploys
```

---

## Landing the Plane (Session Completion)

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create beads for anything that needs follow-up
2. **Run quality gates** (if code changed) - Hugo build, Python tests if applicable
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

---

## Issue Tracking with br (Beads)

All issue tracking goes through **Beads**. No other TODO systems.

**Note:** `br` is a convenience alias for the real Beads CLI: `bd`.
**Project prefix:** `ms` (e.g., ms-1, ms-2, etc.)

### Basics

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

- Run `br sync --flush-only` to export to `.beads/issues.jsonl` without git operations.
- Then run `git add .beads/ && git commit -m "Update beads"` to commit changes.

Never:

- Use markdown TODO lists.
- Use other trackers.
- Duplicate tracking.

---

## Using bv as an AI sidecar

bv is a graph-aware triage engine for Beads projects (.beads/beads.jsonl). Instead of parsing JSONL or hallucinating graph traversal, use robot flags for deterministic, dependency-aware outputs with precomputed metrics (PageRank, betweenness, critical path, cycles, HITS, eigenvector, k-core).

**Scope boundary:** bv handles *what to work on* (triage, priority, planning). For agent-to-agent coordination (messaging, work claiming, file reservations), use MCP Agent Mail.

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
```bash
bv --robot-plan          # Parallel execution tracks with unblocks lists
bv --robot-priority      # Priority misalignment detection
```

**Graph Analysis:**
```bash
bv --robot-insights      # Full metrics: PageRank, betweenness, HITS, etc.
bv --robot-label-health  # Per-label health scores
```

**History & Change Tracking:**
```bash
bv --robot-history       # Bead-to-commit correlations
bv --robot-diff --diff-since <ref>  # Changes since ref
```

#### jq Quick Reference

```bash
bv --robot-triage | jq '.quick_ref'                        # At-a-glance summary
bv --robot-triage | jq '.recommendations[0]'               # Top recommendation
bv --robot-plan | jq '.plan.summary.highest_impact'        # Best unblock target
bv --robot-insights | jq '.Cycles'                         # Circular deps (must fix!)
```

Use bv instead of parsing beads.jsonl—it computes PageRank, critical paths, cycles, and parallel tracks deterministically.

---

## MCP Agent Mail — Multi-Agent Coordination

Agent Mail is available as an MCP server for coordinating work across agents.

What Agent Mail gives:
- Identities, inbox/outbox, searchable threads.
- Advisory file reservations (leases) to avoid agents clobbering each other.
- Persistent artifacts in git (human-auditable).

Core patterns:

1. **Same repo**
   - Register identity:
     - `ensure_project` then `register_agent` with the repo's absolute path as `project_key`.
   - Reserve files before editing:
     - `file_reservation_paths(project_key, agent_name, ["hugo-site/content/**"], ttl_seconds=3600, exclusive=true)`.
   - Communicate:
     - `send_message(..., thread_id="FEAT-123")`.
     - `fetch_inbox`, then `acknowledge_message`.
   - Fast reads:
     - `resource://inbox/{Agent}?project=<abs-path>&limit=20`.
     - `resource://thread/{id}?project=<abs-path>&include_bodies=true`.

2. **Macros vs granular:**
   - Prefer macros when speed is more important than fine-grained control:
     - `macro_start_session`, `macro_prepare_thread`, `macro_file_reservation_cycle`, `macro_contact_handshake`.
   - Use granular tools when you need explicit behavior.

Common pitfalls:
- "from_agent not registered" → call `register_agent` with correct `project_key`.
- `FILE_RESERVATION_CONFLICT` → adjust patterns, wait for expiry, or use non-exclusive reservation.

**If Agent Mail is not available, notify the user to start it with the `am` alias.**

---

## Morph Warp Grep — AI-Powered Code Search

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

---

## cass — Cross-Agent Search

`cass` indexes prior agent conversations (Claude Code, Codex, Cursor, Gemini, ChatGPT, etc.) so we can reuse solved problems.

Rules:

- Never run bare `cass` (TUI). Always use `--robot` or `--json`.

Examples:

```bash
cass health
cass search "Hugo template syntax" --robot --limit 5
cass view /path/to/session.jsonl -n 42 --json
cass capabilities --json
```

Tips:

- Use `--fields minimal` for lean output.
- Filter by agent with `--agent`.
- Use `--days N` to limit to recent history.

Treat cass as a way to avoid re-solving problems other agents already handled.

---

## Memory System: cass-memory

The Cass Memory System (cm) gives agents memory by searching previous coding sessions and extracting lessons.

### Quick Start

```bash
# Check status and see recommendations
cm onboard status

# Get sessions to analyze
cm onboard sample --fill-gaps

# Read a session with rich context
cm onboard read /path/to/session.jsonl --template

# Add extracted rules
cm playbook add "Your rule content" --category "hugo"

# Mark session as processed
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

### Protocol

1. **START**: Run `cm context "<task>" --json` before non-trivial work
2. **WORK**: Reference rule IDs when following them (e.g., "Following b-8f3a2c...")
3. **FEEDBACK**: Leave inline comments when rules help/hurt:
   - `// [cass: helpful b-xyz] - reason`
   - `// [cass: harmful b-xyz] - reason`
4. **END**: Just finish your work. Learning happens automatically.

---

## UBS Quick Reference for AI Agents

UBS (Ultimate Bug Scanner): **Flag likely bugs before every commit**

**Golden Rule:** `ubs <changed-files>` before every commit. Exit 0 = safe. Exit >0 = fix & re-run.

**Commands:**
```bash
ubs file.html styles.css                # Specific files (< 1s) — USE THIS
ubs $(git diff --name-only --cached)    # Staged files — before commit
ubs --only=html,css hugo-site/          # Language filter (faster)
ubs --ci --fail-on-warning .            # CI mode — before PR
ubs --help                              # Full command reference
```

**Output Format:**
```
⚠️  Category (N errors)
    file.html:42:5 – Issue description
    💡 Suggested fix
Exit code: 1
```

**Fix Workflow:**
1. Read finding → category + fix suggestion
2. Navigate `file:line:col` → view context
3. Verify real issue (not false positive)
4. Fix root cause (not symptom)
5. Re-run `ubs <file>` → exit 0
6. Commit

**Speed Critical:** Scope to changed files. `ubs hugo-site/layouts/index.html` (< 1s) vs `ubs .` (30s).

---

## DCG Quick Reference for AI Agents

DCG (Destructive Command Guard) is a Claude Code hook that **blocks dangerous git and filesystem commands** before execution. Sub-millisecond latency, mechanical enforcement.

**Golden Rule:** DCG works automatically—you don't need to call it. When a dangerous command is blocked, use safer alternatives or ask the user to run it manually.

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

**Troubleshooting:**

| Issue | Solution |
|-------|----------|
| DCG blocks legitimate command | Ask user to run manually, or use allow-once code if provided |
| Hook not registered | Run `dcg install` |
| DCG not blocking anything | Run `dcg doctor` to verify hook is active |

---

## RU Quick Reference for AI Agents

RU (Repo Updater) is a multi-repo sync tool with **AI-driven commit automation**.

**Common Commands:**
```bash
ru sync                        # Clone missing + pull updates for all repos
ru sync --parallel 4           # Parallel sync (4 workers)
ru status                      # Check repo status without changes
ru status --fetch              # Fetch + show ahead/behind
```

**Agent Sweep (commit automation):**
```bash
ru agent-sweep --dry-run       # Preview dirty repos to process
ru agent-sweep --parallel 4    # AI-driven commits in parallel
```

---

## ntm — Named Tmux Manager

ntm is the agent cockpit for managing multiple coding agents in tmux sessions.

Use ntm to:
- Launch and manage multiple agents in parallel
- Switch between agent sessions
- View agent outputs side-by-side
- Coordinate multi-agent workflows

**If you need to coordinate with multiple agents, use ntm to launch and manage sessions.**

---

## Hugo-Specific Critical Rules

1. **All content changes happen in `hugo-site/` directory**
2. **Blog post front matter requires:**
   - ISO 8601 date format
   - Description field
   - Valid HTML or Markdown
3. **When adding blog posts:** Update count in `hugo-site/content/_index.html`
4. **CSS Rules:**
   - Never load `main.css` and `notebook.css` together
   - Max-width: 55ch for all pages
   - Code cells: content must be on same line as opening tag
5. **Mobile padding:** Body `40px 0 0 0` for fixed header
6. **Test builds:** Run `hugo` before committing to catch template errors
7. **Deployment:** Automatic on push to main via GitHub Actions

**Always consult `claude.md` for full project architecture and implementation details.**

---

## Quick Tool Reference

| Tool | Purpose | Usage |
|------|---------|-------|
| `br` | Beads task management | `br ready --json` |
| `bv` | Beads graph analysis | `bv --robot-triage` |
| `cass` | Agent session search | `cass search "query" --robot` |
| `cm` | Memory system | `cm context "task" --json` |
| `ubs` | Bug scanner | `ubs <files>` |
| `dcg` | Command guard | Automatic (no manual calls) |
| `ntm` | Tmux manager | Launch multiple agents |
| `hugo` | Static site generator | `cd hugo-site && hugo server` |

**For detailed tool usage, see the corresponding sections above.**
