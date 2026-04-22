---
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task
description: Run parallel code review across multiple directories or files. Uses N subagents simultaneously for faster analysis.
argument-hint: <directories or files to review in parallel, e.g., "src/auth src/api src/db">
---

# Parallel Code Review

Review `$ARGUMENTS` using parallel subagents for maximum speed.

## Process

1. **Parse Targets**: Split arguments into independent review targets
2. **Spawn Parallel Reviewers**: Launch one subagent per target
3. **Collect Results**: Retrieve all reviews via TaskOutput
4. **Synthesize**: Merge findings into prioritized report

## Execution Pattern

**CRITICAL**: Launch ALL Task calls in a SINGLE message for true parallelism.

For each independent target, spawn a subagent with `run_in_background: true`:

```
I'm launching N parallel code reviewers:

[Task 1]
description: "Review [target 1]"
prompt: "You are a code reviewer. Analyze [target 1] for:
- Code quality and best practices
- Potential bugs and edge cases
- Security vulnerabilities
- Performance issues
- Test coverage gaps

Provide findings with file:line references and severity levels."
run_in_background: true

[Task 2]
description: "Review [target 2]"
prompt: "You are a code reviewer. Analyze [target 2] for..."
run_in_background: true

[Task 3]
description: "Review [target 3]"
prompt: "You are a code reviewer. Analyze [target 3] for..."
run_in_background: true
```

After all complete, retrieve results:
```
TaskOutput: task_1_id
TaskOutput: task_2_id
TaskOutput: task_3_id
```

## Output Format

```markdown
## Parallel Review Results

### Summary
- **Targets reviewed**: N
- **Total findings**: X
- **Critical issues**: Y
- **Execution time**: ~Zs (parallel)

### [Target 1] Findings

#### Critical
- [Issue] at file:line - [Description]

#### Warnings
- [Issue] at file:line - [Description]

#### Suggestions
- [Improvement] at file:line - [Description]

### [Target 2] Findings
...

### Combined Priority List

1. **Critical** - [Target X] - [Issue description]
2. **Critical** - [Target Y] - [Issue description]
3. **High** - [Target Z] - [Issue description]
...

### Recommended Actions

1. Fix critical issues in [Target X] first
2. Address security concerns in [Target Y]
3. Consider performance optimizations in [Target Z]
```

## Example Usage

```
/project-starter:parallel-review src/auth src/api src/db
```

This spawns 3 parallel reviewers (one per directory), completing in ~1/3 the time of sequential review.

## When to Use

- Reviewing multiple independent modules
- Pre-merge comprehensive codebase review
- Analyzing different areas of a large PR
- Comparing implementation patterns across directories
