---
allowed-tools: Bash(git:*)
description: Sync current branch with main/master (fetch, rebase or merge)
argument-hint: "[merge|rebase] (default: rebase)"
---

## Context

- Current branch: !`git branch --show-current`
- Default branch: !`git remote show origin 2>/dev/null | grep 'HEAD branch' | cut -d' ' -f5 || echo "main"`
- Uncommitted changes: !`git status --porcelain`
- Commits ahead/behind: !`git rev-list --left-right --count origin/$(git remote show origin 2>/dev/null | grep 'HEAD branch' | cut -d' ' -f5 || echo "main")...HEAD 2>/dev/null || echo "unknown"`
- Current remote: !`git remote -v | head -2`

## Task

Safely sync the current branch with the default branch:

1. Check for uncommitted changes - if any, stash them
2. Fetch the latest from origin
3. Based on argument (default: rebase):
   - **rebase**: `git rebase origin/<default-branch>`
   - **merge**: `git merge origin/<default-branch>`
4. Handle any conflicts by reporting them clearly
5. If changes were stashed, pop them
6. Report the sync status

Strategy: $ARGUMENTS
