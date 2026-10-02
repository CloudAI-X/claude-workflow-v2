---
description: Simplifies code after implementation. Reviews recent changes and suggests/applies simplifications while preserving behavior.
---

# Code Simplifier

Simplify code after implementation. Find ways to make code cleaner and simpler without changing behavior.

## Philosophy

- Simpler is better
- Less code = fewer bugs
- Clarity over cleverness
- Don't change behavior, only structure
- Delete code when possible

## Phase 1: Identify Recent Changes

```bash
git diff HEAD~1 --name-only
git log -1 --stat
git diff HEAD~1
```

## Phase 2: Analyze for Simplification

Look for these patterns:

### 1. Duplicate Code

- Repeated logic that can be extracted
- Similar functions that can be merged
- Copy-pasted code with minor variations

### 2. Over-Engineering

- Abstractions used only once
- Unnecessary wrapper functions
- Over-parameterized functions (too many options)
- Premature generalization

### 3. Dead Code

- Unused variables
- Unreachable branches
- Commented-out code
- Unused imports/dependencies

### 4. Complex Conditionals

- Nested if-else chains (flatten with early returns)
- Complex boolean expressions (extract to named variables)
- Guard clauses that can be simplified

### 5. Long Functions

- Functions > 20 lines (consider splitting)
- Multiple responsibilities (single responsibility)
- Too many parameters (use objects)

### 6. Unnecessary Complexity

- Try-catch around code that can't fail
- Null checks on values that can't be null
- Defensive code for impossible cases

## Phase 3: Propose Simplifications

For each finding, present:

````
### Simplification: [Short description]

**Location**: `file:line`
**Type**: [Duplicate/Over-engineering/Dead code/etc.]

**Current** (X lines):
```[lang]
[code block]
```

**Simplified** (Y lines):
```[lang]
[code block]
```

**Benefit**: [Why this is better]
**Risk**: Low - behavior unchanged
````

## Phase 4: Apply Simplifications

After user approval:

1. Make one change at a time
2. Run tests after each change
3. Commit with clear message: `refactor: simplify [description]`
4. Move to next simplification

## Output Format

```
## Simplification Report

### Changes Analyzed

- Files: [count]
- Lines added: [count]
- Lines removed: [count]

### Simplification Opportunities

[List each opportunity with current/simplified code]

### Summary

- Simplifications found: X
- Estimated lines reducible: Y
- Complexity reduction: [High/Medium/Low]

### Recommended Actions

1. [ ] Apply simplification #1 (highest impact)
2. [ ] Apply simplification #2
       ...

### Tests to Run After

- [List of test commands to verify no behavior change]
```

## Safety Rules

1. **Never change behavior** - only structure
2. **Run tests after every change** - verify nothing broke
3. **Keep changes atomic** - one simplification per commit
4. **Document what was simplified** - clear commit messages
5. **Preserve public APIs** - internal refactoring only

## Usage

This command ships with the project-starter plugin. Invoke with: `/project-starter:code-simplifier`
