---
allowed-tools: Bash(git:*), Bash(npm:*), Bash(npx:*), Bash(yarn:*), Bash(bun:*), Bash(pytest:*), Bash(go:*), Read, Write
description: Add tests for recently changed files or specified code
argument-hint: "[file path or function name]"
---

## Context

- Recently modified files: !`git diff --name-only HEAD~3 2>/dev/null | head -10`
- Project root files (infer the test framework from these): !`ls -a`
- Existing test files: !`git ls-files 2>/dev/null | grep -i -e test -e spec | head -10`
- Test directory structure: !`ls -la tests/ test/ __tests__/ spec/ 2>/dev/null | head -20`

## Task

Add tests for the specified target:

1. Identify the file/function to test
2. Find the corresponding test file (or create one following project conventions)
3. Analyze the code to understand:
   - Input/output behavior
   - Edge cases
   - Error conditions
4. Write comprehensive tests covering:
   - Happy path
   - Edge cases
   - Error handling
5. Run the tests to verify they pass

Target: $ARGUMENTS

If no target specified, focus on recently modified files that lack test coverage.
