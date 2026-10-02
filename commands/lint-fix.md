---
allowed-tools: Bash(npm:*), Bash(npx:*), Bash(yarn:*), Bash(pnpm:*), Bash(bun:*), Bash(python:*), Bash(go:*), Bash(cargo:*)
description: Auto-fix all linting and formatting issues
argument-hint: "[optional file or directory path]"
---

## Context

- Project root files (infer the project type and lint config from these): !`ls -a`
- Package scripts: !`cat package.json 2>/dev/null | grep -A 20 '"scripts"' | head -25 || echo "No package.json"`
- Staged files: !`git diff --name-only --cached 2>/dev/null`
- Files changed in the last commit: !`git diff --name-only HEAD~1 2>/dev/null | head -50`

## Task

Auto-fix all linting and formatting issues:

1. Detect the project type and available linters
2. Run formatters first (Prettier, Black, gofmt, rustfmt)
3. Run linters with auto-fix enabled:
   - JavaScript/TypeScript: `eslint --fix`
   - Python: `ruff check --fix` or `black` + `isort`
   - Go: `gofmt -w` + `go vet`
   - Rust: `cargo fmt` + `cargo clippy --fix`
4. Report what was fixed
5. List any remaining issues that require manual attention

Scope: $ARGUMENTS
