---
allowed-tools: Bash(npm:*), Bash(npx:*), Bash(yarn:*), Bash(pnpm:*), Bash(bun:*), Bash(python:*), Bash(python3:*), Bash(pip:*), Bash(go:*), Read, Edit, Write
description: Quickly fix lint errors, type errors, or simple bugs
argument-hint: "[file or error description]"
---

## Context

- Project root files (infer the project type from these): !`ls -a`
- Recent changes: !`git diff --name-only HEAD~1 2>/dev/null || git diff --name-only`

## Task

Fix the issue described below:

1. Identify the type of error (type error, lint, syntax, logic). If none was described, find it by running the checks the project has installed (for example `npx --no tsc --noEmit`, `npx --no eslint .`, `python3 -m ruff check .`) — never let `npx` download a tool
2. Locate the problematic file(s)
3. Apply the minimal fix needed
4. Verify the fix by re-running the relevant check
5. Report what was fixed

Target: $ARGUMENTS
