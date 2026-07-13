---
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git add:*), Bash(git commit:*)
description: Create a conventional commit with auto-generated message
argument-hint: "[optional scope or message hint]"
---

## Context

- Current branch: !`git branch --show-current`
- Git status: !`git status --short`
- Staged changes: !`git diff --cached --stat`
- Staged diff: !`git diff --cached`
- Recent commits (for style reference): !`git log --oneline -5`

## Task

Based on the staged changes above, create a single git commit:

1. Analyze the staged diff to understand what changed
2. Generate a conventional commit message following the format:
   - `type(scope): description`
   - Types: feat, fix, docs, style, refactor, perf, test, chore
3. If no changes are staged, inform the user and suggest staging files
4. Execute the commit

$ARGUMENTS
