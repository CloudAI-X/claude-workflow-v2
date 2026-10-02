---
allowed-tools: Bash(git:*), Bash(npm:*), Bash(npx:*), Bash(yarn:*), Bash(bun:*), Bash(pytest:*), Bash(go:*), Read, Write
description: Add tests for recently changed files or specified code
argument-hint: "[file path or function name]"
---

## Context

- Recently modified files: !`git diff --name-only HEAD~3 2>/dev/null | grep -E '\.(ts|tsx|js|jsx|py|go|rs)$' | head -10 || echo "No recent changes"`
- Test framework detection: !`cat package.json 2>/dev/null | grep -E '"(jest|vitest|mocha)"' | head -1 || ls pytest.ini pyproject.toml 2>/dev/null | head -1 || echo "Unknown test framework"`
- Existing test files: !`find . -name "*test*" -o -name "*spec*" 2>/dev/null | grep -E '\.(ts|tsx|js|jsx|py|go)$' | head -10 || echo "No test files found"`
- Test directory structure: !`ls -la tests/ test/ __tests__/ spec/ 2>/dev/null | head -20 || echo "No standard test directory"`

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
