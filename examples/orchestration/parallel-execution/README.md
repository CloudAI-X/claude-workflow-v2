# Parallel Execution Examples

Learn how to use parallel subagent execution for dramatic speed improvements.

## Overview

Parallel execution spawns multiple subagents simultaneously using the Agent tool (`Task` in older versions) with `run_in_background: true`. This enables N tasks to run concurrently instead of sequentially.

**Key Rule**: ALL Task calls MUST be in a SINGLE assistant message for true parallelism.

## Speed Comparison

| Approach | 5 Tasks @ 30s each | Total Time |
|----------|-------------------|------------|
| Sequential | 30s → 30s → 30s → 30s → 30s | ~150s |
| Parallel | All 5 simultaneously | ~30s |

**Result**: ~5x faster execution

## Parallel Execution Flow

```
           User Request
                │
                ▼
       ┌─────────────────┐
       │   Orchestrator  │
       │   (Creates Plan)│
       └────────┬────────┘
                │
    ┌───────────┼───────────┬───────────┬───────────┐
    │           │           │           │           │
    ▼           ▼           ▼           ▼           ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│ Task 1 │ │ Task 2 │ │ Task 3 │ │ Task 4 │ │ Task 5 │
│ Agent  │ │ Agent  │ │ Agent  │ │ Agent  │ │ Agent  │
└────┬───┘ └────┬───┘ └────┬───┘ └────┬───┘ └────┬───┘
     │          │          │          │          │
     │          │          │          │          │
     │    All run simultaneously    │          │
     │          │          │          │          │
     └──────────┴──────────┴──────────┴──────────┘
                          │
                          ▼
                  ┌───────────────┐
                  │    Results    │
                  │ (Auto-return) │
                  └───────┬───────┘
                          │
                          ▼
                  ┌───────────────┐
                  │   Synthesize  │
                  │    Results    │
                  └───────────────┘
```

## Example 1: Directory-Based Parallelization

Analyze multiple directories simultaneously.

**User prompt:**
```
Review the code in src/auth, src/api, and src/db for quality issues
```

**Orchestrator spawns 3 parallel subagents (ONE message):**

```markdown
I'm launching 3 parallel code reviewers:

[Task 1]
description: "Review src/auth"
prompt: "You are a code reviewer. Analyze the src/auth directory for code quality..."
subagent_type: general-purpose
run_in_background: true

[Task 2]
description: "Review src/api"
prompt: "You are a code reviewer. Analyze the src/api directory for code quality..."
subagent_type: general-purpose
run_in_background: true

[Task 3]
description: "Review src/db"
prompt: "You are a code reviewer. Analyze the src/db directory for code quality..."
subagent_type: general-purpose
run_in_background: true
```

**Result retrieval:**
```
# Results arrive automatically when each background subagent finishes (TaskOutput is deprecated)
```

## Example 2: Perspective-Based Parallelization

Analyze from multiple viewpoints simultaneously.

**User prompt:**
```
Analyze src/api from architecture, security, performance, and testing perspectives
```

**Orchestrator spawns 4 parallel subagents (ONE message):**

```markdown
I'm launching 4 parallel analysts:

[Task 1]
description: "Architecture analysis"
prompt: "You are a software architect. Analyze src/api for component structure..."
subagent_type: general-purpose
run_in_background: true

[Task 2]
description: "Security analysis"
prompt: "You are a security auditor. Check src/api for OWASP vulnerabilities..."
subagent_type: general-purpose
run_in_background: true

[Task 3]
description: "Performance analysis"
prompt: "You are a performance engineer. Look for bottlenecks in src/api..."
subagent_type: general-purpose
run_in_background: true

[Task 4]
description: "Testing analysis"
prompt: "You are a test architect. Evaluate test coverage for src/api..."
subagent_type: general-purpose
run_in_background: true
```

## Example 3: Task-Based Parallelization

Implement multiple features simultaneously.

**User prompt:**
```
Implement user authentication with login, registration, and password reset
```

**Orchestrator spawns 3 parallel subagents (ONE message):**

```markdown
I'm launching 3 parallel implementers:

[Task 1]
description: "Implement login"
prompt: "Implement the login endpoint with JWT authentication..."
subagent_type: general-purpose
run_in_background: true

[Task 2]
description: "Implement registration"
prompt: "Implement the registration endpoint with validation..."
subagent_type: general-purpose
run_in_background: true

[Task 3]
description: "Implement password reset"
prompt: "Implement the password reset flow with email verification..."
subagent_type: general-purpose
run_in_background: true
```

## Example 4: Verification Parallelization

Run all verification checks simultaneously.

**User prompt:**
```
Verify my recent code changes are ready for merge
```

**Spawns 5 parallel verification subagents:**

```markdown
[Task 1] description: "Type checking", run_in_background: true
[Task 2] description: "Run tests", run_in_background: true
[Task 3] description: "Lint check", run_in_background: true
[Task 4] description: "Security scan", run_in_background: true
[Task 5] description: "Build validation", run_in_background: true
```

## Available Parallel Commands

The plugin provides these parallel execution commands:

| Command | Purpose |
|---------|---------|
| `/project-starter:parallel-review` | Review multiple directories in parallel |
| `/project-starter:parallel-analyze` | Multi-perspective analysis |
| `/project-starter:verify-changes` | Parallel verification checks |

## When to Use Parallel Execution

**Good candidates:**
- Multiple independent analyses
- Multi-file processing (different files)
- Multi-perspective reviews
- Verification checks
- Feature implementation (independent components)

**Avoid parallelization when:**
- Tasks depend on each other's output
- Tasks modify the same files
- Order matters for correctness
- Sequential workflow required (commit → push → PR)

## Critical Implementation Detail

**WRONG** - Tasks in separate messages (runs sequentially):
```
Message 1: Task 1 with run_in_background: true
Message 2: Task 2 with run_in_background: true
Message 3: Task 3 with run_in_background: true
```

**CORRECT** - All tasks in ONE message (runs in parallel):
```
Message 1:
  Task 1 with run_in_background: true
  Task 2 with run_in_background: true
  Task 3 with run_in_background: true
```

## TodoWrite Integration

For parallel execution, multiple tasks can be marked `in_progress` simultaneously:

```json
[
  { "content": "Task A", "status": "in_progress" },
  { "content": "Task B", "status": "in_progress" },
  { "content": "Task C", "status": "in_progress" },
  { "content": "Synthesize", "status": "pending" }
]
```

As each background subagent's result is delivered automatically (`TaskOutput` is deprecated), mark the corresponding task as `completed`.

## See Also

- [Parallel Execution Skill](../../../skills/parallel-execution/SKILL.md)
- [Orchestrator Agent](../../../agents/orchestrator.md)
- [Comprehensive Code Review (Sequential)](../comprehensive-code-review/)
