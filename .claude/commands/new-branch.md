---
description: Create and checkout a new git branch from the current branch
argument-hint: [branch-name]
allowed-tools: Bash(git checkout:*), Bash(git branch:*), Bash(git rev-parse:*)
---

# Create New Branch

Create a new git branch and check it out for development.

## Usage

```
/new-branch feature/notebook-dark-mode
/new-branch bugfix/mobile-header
/new-branch docs/update-contributing
```

## What happens

1. Creates a new branch from your current branch
2. Automatically checks you out to the new branch
3. Confirms the operation completed

## Branch naming suggestions

- Feature: `feature/description`
- Bug fix: `bugfix/description`
- Documentation: `docs/description`
- Refactoring: `refactor/description`
