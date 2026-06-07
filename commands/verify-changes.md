---
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task
description: Comprehensive verification after code changes. Uses Boris Cherny's multi-subagent adversarial approach.
---

# Verify Changes

Run comprehensive verification of recent code changes using multi-subagent adversarial approach.

## Phase 1: Gather Context

Run these commands to understand what changed:

```bash
git diff HEAD~1 --stat
git log -3 --oneline
git diff --name-only HEAD~1
```

Identify affected files and their corresponding test files.

## Phase 2: Spawn Verification Subagents (Parallel)

Use the Task tool with `run_in_background: true` to spawn subagents in parallel.

**CRITICAL**: Launch ALL subagents in a SINGLE message for true parallelism:

```
[All Task calls in ONE message]

Task 1: {
  description: "Syntax & Type Check",
  prompt: "Run language-specific type checker (tsc, mypy, go vet)...",
  run_in_background: true
}

Task 2: {
  description: "Test Runner",
  prompt: "Run tests for affected files first, then integration tests...",
  run_in_background: true
}

Task 3: {
  description: "Lint & Style Check",
  prompt: "Run project linter (eslint, ruff, golangci-lint)...",
  run_in_background: true
}

Task 4: {
  description: "Security Scan",
  prompt: "Grep for hardcoded secrets, check for vulnerabilities...",
  run_in_background: true
}

Task 5: {
  description: "Build Validator",
  prompt: "Run build command, verify artifacts exist...",
  run_in_background: true
}
```

Each subagent returns its result automatically when it completes — there is no
separate retrieval call. Read each verifier's report as it returns.

### Subagent Details

### Subagent 1: Syntax & Type Check

- Run language-specific type checker (tsc, mypy, go vet)
- Report any type errors or warnings
- Exit with list of issues found

### Subagent 2: Test Runner

- Run tests for affected files first
- Run related integration tests
- Report failures with file:line context

### Subagent 3: Lint & Style Check

- Run project linter (eslint, ruff, golangci-lint)
- Check for formatting issues
- Report violations with severity

### Subagent 4: Security Scan

- Grep for hardcoded secrets (passwords, API keys, tokens)
- Check for common vulnerabilities in new code
- Review any new dependencies

### Subagent 5: Build Validator

- Run build command
- Verify build artifacts exist
- Check for build warnings

## Phase 3: Adversarial Review

Spawn 3 adversarial subagents to review Phase 2 findings:

### Adversarial A: False Positive Filter

- Review each finding from Phase 2
- Determine if it's a real issue or false alarm
- Provide reasoning for each determination

### Adversarial B: Missing Issues Finder

- Look for issues the first pass might have missed
- Check edge cases in changed code
- Verify error handling is adequate

### Adversarial C: Context Validator

- Verify findings make sense in project context
- Check if "issues" are actually intentional patterns
- Consider project conventions

## Phase 4: Synthesize Results

Combine all subagent outputs into final report:

```
## Verification Results: [PASS/FAIL]

### Confirmed Issues
1. [Issue] - [Location] - [Why it's confirmed real]

### Warnings (Review Recommended)
1. [Warning] - [Location] - [Context]

### All Checks
- [ ] Type checking: [PASS/FAIL]
- [ ] Tests: [PASS/FAIL]
- [ ] Linting: [PASS/FAIL]
- [ ] Security: [PASS/FAIL]
- [ ] Build: [PASS/FAIL]

### Subagent Summary
- Initial findings: X issues
- After adversarial review: Y confirmed issues
- False positives filtered: Z
```

## Usage

This command ships with the project-starter plugin. Invoke with: `/project-starter:verify-changes`
