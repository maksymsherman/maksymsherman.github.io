---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git diff:*), Bash(git commit:*), Bash(git push:*), Bash(git log:*), Bash(git branch:*), Bash(gh:*)
argument-hint: [pr-title] (optional)
description: Create a commit, push, and open a pull request
---

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits on this branch: !`git log --oneline -5`
- Git diff from main branch: !`git diff main...HEAD`

## Your task

1. **Create a commit:**
   - Analyze all the changes shown above
   - Stage all relevant files using `git add`
   - Create a meaningful commit message that:
     - Summarizes the nature of changes (feature, fix, refactor, etc.)
     - Focuses on the "why" rather than just the "what"
     - Ends with the standard co-authorship footer:
       ```
       🤖 Generated with [Claude Code](https://claude.com/claude-code)

       Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
       ```
   - Use a HEREDOC format for the commit message

2. **Push to remote:**
   - Push the current branch to origin
   - Use `-u` flag if the branch doesn't have an upstream yet

3. **Create a pull request:**
   - Use `gh pr create` with:
     - Title: Use $ARGUMENTS if provided, otherwise generate from commit message
     - Body format:
       ```markdown
       ## Summary
       <1-3 bullet points summarizing the changes>

       ## Test plan
       <Bulleted checklist of steps to test the PR>

       🤖 Generated with [Claude Code](https://claude.com/claude-code)
       ```
   - Use HEREDOC for the body
   - Return the PR URL when done

## Important notes

- Do NOT ask for permission to commit/push/create PR - this command implies consent
- Do NOT use the TodoWrite tool
- Be concise in your responses
- If there are no changes to commit, inform the user and stop
