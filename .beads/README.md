# Beads Issue Tracking

This project uses **Beads** for issue tracking. All beads live on the `beads-sync` branch to keep the main branch history clean and focused on code changes.

## What is Beads?

Beads is an AI-native, CLI-first issue tracking system that lives directly in your git repository. It stores issues as JSONL files in the `.beads/` directory, making them version-controlled, git-native, and perfect for AI coding agents.

**Official Repository:** [github.com/steveyegge/beads](https://github.com/steveyegge/beads)

## Where Are the Beads?

**All beads files live on the `beads-sync` branch**, not on `main`. This keeps the main branch clean while maintaining full issue tracking functionality.

To view the actual beads files:
```bash
git checkout beads-sync
ls -la .beads/
```

## How to Use Beads

You can interact with beads **from any branch** using the `bd` CLI. The beads commands automatically work with the `beads-sync` branch.

### Essential Commands

```bash
# View all issues (works from any branch)
bd list

# View specific issue details
bd show <issue-id>

# Create a new issue
bd create "Issue title here"

# Update issue status
bd update <issue-id> --status in_progress
bd update <issue-id> --status done

# Close an issue
bd close <issue-id> --reason "Completed successfully"

# Add comments to issues
bd comment <issue-id> "Your comment here"

# Search issues
bd list --status open
bd list --priority high
```

### Sync with Remote

```bash
# Manually sync beads with git remote
bd sync

# The daemon auto-syncs in the background (optional)
bd daemon --start
bd daemon --status
bd daemon --stop
```

## Project-Specific Configuration

This repository is configured with:
- **Sync branch:** `beads-sync` (all beads files live here)
- **Issue prefix:** `ms-` (all issue IDs start with "ms-")
- **Config location:** `.beads/config.yaml` on `beads-sync` branch

## Common Workflows for AI Agents

### Checking for Open Issues
```bash
# List all open issues
bd list --status open

# Show details of a specific issue
bd show ms-abc
```

### Creating Issues During Development
```bash
# Create a new issue for work discovered
bd create "Add user authentication to settings page"

# Set priority and type
bd update <new-issue-id> --priority high --type feature
```

### Updating Issue Status
```bash
# Start working on an issue
bd update <issue-id> --status in_progress

# Mark as complete
bd update <issue-id> --status done
bd close <issue-id> --reason "Implemented feature successfully"
```

### Viewing Issue History
```bash
# Show full issue details including comments and history
bd show <issue-id>

# List recently updated issues
bd list --sort updated
```

## How Beads Works

### File Structure
On the `beads-sync` branch, you'll find:
```
.beads/
├── config.yaml        # Repository configuration
├── metadata.json      # Repository metadata
├── issues.jsonl       # All issues (one JSON object per line)
└── .gitignore        # Beads-specific gitignore
```

### Git Integration
- Issues are stored as JSONL (JSON Lines) - one issue per line
- Changes to issues create commits on the `beads-sync` branch
- The `bd sync` command pushes/pulls beads from the remote
- Optional daemon can auto-sync issues in the background

### Why Separate Branch?
Keeping beads on `beads-sync` provides:
- **Clean main history:** No issue tracking commits cluttering your code history
- **No merge conflicts:** Issue changes don't interfere with code merges
- **Daemon-friendly:** Background sync doesn't rewrite files in your working tree
- **Clear separation:** Code changes on `main`, tracking on `beads-sync`

## Issue ID Format

All issues in this project use the `ms-` prefix:
- `ms-abc` - First issue
- `ms-d2d` - Another issue
- Pattern: `ms-<base36-id>`

## Beads Philosophy

Beads is designed to be:
- **AI-Native:** Works seamlessly with AI coding agents via CLI
- **Git-Native:** Issues are files, commits are history, branches are branches
- **Developer-Focused:** No web UI context switching, just terminal commands
- **Offline-Friendly:** Work on issues offline, sync when connected
- **Fast & Lightweight:** Minimal overhead, maximum productivity

## Quick Reference

| Task | Command |
|------|---------|
| List open issues | `bd list --status open` |
| Show issue details | `bd show <id>` |
| Create new issue | `bd create "Title"` |
| Start working on issue | `bd update <id> --status in_progress` |
| Complete issue | `bd close <id> --reason "Done"` |
| Add comment | `bd comment <id> "Comment text"` |
| Sync with remote | `bd sync` |
| View config | `cat .beads/config.yaml` (on beads-sync) |

## Getting Started with Beads

If you want to use Beads in other projects:

```bash
# Install Beads
curl -sSL https://raw.githubusercontent.com/steveyegge/beads/main/scripts/install.sh | bash

# Initialize in your repo
bd init

# Create your first issue
bd create "Try out Beads"
```

## Learn More

- **Documentation:** [github.com/steveyegge/beads/docs](https://github.com/steveyegge/beads/tree/main/docs)
- **Quick Start Guide:** Run `bd quickstart`
- **Help:** Run `bd --help` or `bd <command> --help`

---

**Remember:** Beads files live on `beads-sync`, but you can use `bd` commands from any branch!
