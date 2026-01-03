---
description: Create a commit and push to remote without opening a pull request
argument-hint: [-m "commit message"]
allowed-tools: Bash(git add:*), Bash(git commit:*), Bash(git push:*), Bash(git status:*), Bash(git diff:*), Bash(git log:*)
---

# Commit and Push

Create a git commit and push to the remote repository without opening a pull request. Useful for working directly on main or when changes are small.

## Usage

```
/commit-push
/commit-push -m "Fix typo in documentation"
```

## What happens

1. Shows current git status and changes
2. Reviews the diff to understand what changed
3. Creates a descriptive commit message (or uses your provided message)
4. Commits the changes
5. Pushes to the remote branch

## When to use this

- Working directly on the main branch
- Small fixes and updates that don't need review
- Documentation updates
- Quick bug fixes
- Deploying changes that trigger GitHub Actions

## Commit message format

All commits will include:
```
Your commit message

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```
