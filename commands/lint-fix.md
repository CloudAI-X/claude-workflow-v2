---
allowed-tools: Bash(npm:*), Bash(npx:*), Bash(yarn:*), Bash(pnpm:*), Bash(bun:*), Bash(python:*), Bash(go:*), Bash(cargo:*)
description: Auto-fix all linting and formatting issues
argument-hint: "[optional file or directory path]"
---

## Context

- Project type: !`ls package.json 2>/dev/null && echo "node" || ls pyproject.toml setup.py requirements.txt 2>/dev/null && echo "python" || ls go.mod 2>/dev/null && echo "go" || ls Cargo.toml 2>/dev/null && echo "rust" || echo "unknown"`
- Lint config files: !`ls .eslintrc* .prettierrc* eslint.config.* pyproject.toml .flake8 .golangci.yml rustfmt.toml 2>/dev/null || echo "No lint config found"`
- Package scripts: !`cat package.json 2>/dev/null | grep -A 20 '"scripts"' | head -25 || echo "No package.json"`
- Files to lint: !`git diff --name-only --cached 2>/dev/null || git diff --name-only HEAD~1 2>/dev/null || echo "all files"`

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
