---
allowed-tools: Bash(npm:*), Bash(npx:*), Bash(yarn:*), Bash(pnpm:*), Bash(bun:*), Bash(python:*), Bash(pip:*), Bash(go:*), Read, Edit, Write
description: Quickly fix lint errors, type errors, or simple bugs
argument-hint: "[file or error description]"
---

## Context

- Package manager detection: !`ls package.json 2>/dev/null && echo "Node.js project" || ls requirements.txt pyproject.toml 2>/dev/null && echo "Python project" || ls go.mod 2>/dev/null && echo "Go project" || echo "Unknown"`
- Recent changes: !`git diff --name-only HEAD~1 2>/dev/null || git diff --name-only`
- TypeScript errors (if applicable): !`npx tsc --noEmit 2>&1 | head -30 || echo "No TypeScript"`
- ESLint errors (if applicable): !`npx eslint . --format compact 2>&1 | head -30 || echo "No ESLint"`
- Python lint (if applicable): !`python3 -m ruff check . 2>&1 | head -30 || python3 -m flake8 . 2>&1 | head -30 || echo "No Python linter"`

## Task

Fix the issue described below:

1. Identify the type of error (type error, lint, syntax, logic)
2. Locate the problematic file(s)
3. Apply the minimal fix needed
4. Verify the fix by re-running the relevant check
5. Report what was fixed

Target: $ARGUMENTS
